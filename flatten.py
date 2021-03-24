"""
   Copyright 2021 InfAI (CC SES)

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""


import os
import uuid
import requests


dep_instance = os.getenv("DEP_INSTANCE")
job_callback_url = os.getenv("JOB_CALLBACK_URL")
input_file = os.getenv("source_csv")
delimiter = os.getenv("delimiter")
unique_col = os.getenv("unique_column")
time_col = os.getenv("time_column")
name_pattern = os.getenv("name_pattern")
sub_tab_delimiters = os.getenv("sub_table_delimiters").split(",")
data_cache_path = "/data_cache"


def remove_trailing_delimiter(unique_items, ui_range, merge_line, new_first_line_map):
    for x in ui_range:
        if "unique_column" in name_pattern:
            col_name = name_pattern.format(unique_column=unique_col, unique_item=unique_items[x])
        else:
            col_name = name_pattern.format(unique_item=unique_items[x])
        if merge_line[new_first_line_map[col_name]]:
            merge_line[new_first_line_map[col_name]] = merge_line[new_first_line_map[col_name]][:-1]


with open("{}/{}".format(data_cache_path, input_file), "r") as file:
    old_first_line = file.readline().strip().split(delimiter)
    time_col_num = old_first_line.index(time_col)
    unique_col_num = old_first_line.index(unique_col)
    unique_items = set()
    for line in file:
        line = line.split(delimiter)
        if line[unique_col_num] not in unique_items:
            unique_items.add(line[unique_col_num])
    unique_items = sorted(unique_items)
unique_items_range = range(len(unique_items))

new_first_line = [time_col]
new_first_line_map = {time_col: 0}
for x in unique_items_range:
    if "unique_column" in name_pattern:
        col_name = name_pattern.format(unique_column=unique_col, unique_item=unique_items[x])
    else:
        col_name = name_pattern.format(unique_item=unique_items[x])
    new_first_line.append(col_name)
    new_first_line_map[col_name] = x + 1
new_first_line_len = len(new_first_line)

reserved_pos = {time_col_num, unique_col_num}

sub_tab_header = list()
for x in range(len(old_first_line)):
    if x not in reserved_pos:
        sub_tab_header.append(old_first_line[x])
sub_tab_header = delimiter.join(sub_tab_header)

output_file = uuid.uuid4().hex

print("flattening ...")
with open("{}/{}".format(data_cache_path, input_file), "r") as in_file:
    with open("{}/{}".format(data_cache_path, output_file), "w") as out_file:
        line = in_file.readline().strip().split(delimiter)
        line_len = len(line)
        line_range = range(line_len)
        out_file.write(delimiter.join(new_first_line) + "\n")
        current_timestamp = None
        line_count = 1
        for line in in_file:
            line = line.strip().split(delimiter)
            if line[time_col_num] != current_timestamp:
                try:
                    remove_trailing_delimiter(unique_items, unique_items_range, merge_line, new_first_line_map)
                    out_file.write("{}\n".format(delimiter.join(merge_line)))
                    line_count += 1
                except NameError:
                    pass
                merge_line = [str()] * new_first_line_len
                merge_line[0] = line[time_col_num]
                current_timestamp = line[time_col_num]
            sub_table = str()
            for pos in line_range:
                if pos not in reserved_pos:
                    if pos < line_len - 1:
                        sub_table += line[pos] + sub_tab_delimiters[0]
                    else:
                        sub_table += line[pos]
            if "unique_column" in name_pattern:
                merge_line[new_first_line_map[name_pattern.format(unique_column=unique_col, unique_item=line[unique_col_num])]] += sub_table + sub_tab_delimiters[1]
            else:
                merge_line[new_first_line_map[name_pattern.format(unique_item=line[unique_col_num])]] += sub_table + sub_tab_delimiters[1]
        remove_trailing_delimiter(unique_items, unique_items_range, merge_line, new_first_line_map)
        out_file.write(delimiter.join(merge_line) + "\n")
        line_count += 1

with open("{}/{}".format(data_cache_path, output_file), "r") as file:
    for x in range(5):
        print(file.readline().strip())
print("total number of lines written: {}".format(line_count))

try:
    resp = requests.post(
        job_callback_url,
        json={dep_instance: {"sub_table_header": sub_tab_header, "output_file": output_file}}
    )
    if not resp.ok:
        raise RuntimeError(resp.status_code)
except Exception as ex:
    try:
        os.remove("{}/{}".format(data_cache_path, output_file))
    except Exception:
        pass
    raise ex
