#### Description

    {
        "name": "Flatten None Unique CSV",
        "image": "platonam/lopco-flatten-non-unique-csv-worker:latest",
        "data_cache_path": "/data_cache",
        "description": "Flatten a Comma-Separated Values file with multiple unique lines per timestamp.",
        "configs": {
            "delimiter": null,
            "unique_column": null,
            "time_column": null,
            "name_pattern": null,
            "sub_table_delimiters": null
        },
        "input": {
            "type": "single",
            "fields": [
                {
                    "name": "source_csv",
                    "media_type": "text/csv",
                    "is_file": true
                }
            ]
        },
        "output": {
            "type": "single",
            "fields": [
                {
                    "name": "sub_table_header",
                    "media_type": "text/plain",
                    "is_file": false
                },
                {
                    "name": "output_file",
                    "media_type": "text/csv",
                    "is_file": true
                }
            ]
        }
    }

For the timestamp format as required by `time_format` please use these [format codes](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes).

----

The `name_pattern` config option defines how the names for new columns are generated and requires the following placeholder:

- `unique_item`

If the optional `unique_column` placeholder is provided the value of the `unique_column` config option will be added to the generated column names.

Examples:

`name_pattern` = `{unique_column}_{unique_item}_processdata`

    time,module,station,process,errorcode
    2021-02-01T05:03:37.526Z,1,3,1,0
    2021-02-01T05:03:43.353Z,2,24,1,0
    2021-02-01T05:03:43.353Z,2,3,1,0

result:

    time,module_2_processdata,module_1_processdata
    2021-02-01T05:03:37.526Z,,3;1;0
    2021-02-01T05:03:43.353Z,24;1;0?3;1;0,
    

`name_pattern` = `{unique_item}_processdata`

    time,module,station,process,errorcode
    2021-02-01T05:03:37.526Z,1,3,1,0
    2021-02-01T05:03:43.353Z,2,24,1,0
    2021-02-01T05:03:43.353Z,2,3,1,0

result:

    time,2_processdata,1_processdata
    2021-02-01T05:03:37.526Z,,3;1;0
    2021-02-01T05:03:43.353Z,24;1;0?3;1;0,

----

The `sub_table_delimiters` config option takes two comma separated values:

Examples:

`sub_table_delimiters` = `;,?`

    time,module,station,process,errorcode
    2021-02-01T05:03:43.353Z,2,24,1,0
    2021-02-01T05:03:43.353Z,2,3,1,0

result:

    time,module_2_processdata,module_1_processdata
    2021-02-01T05:03:43.353Z,24;1;0?3;1;0,

`sub_table_delimiters` = `#,$`

    time,module,station,process,errorcode
    2021-02-01T05:03:43.353Z,2,24,1,0
    2021-02-01T05:03:43.353Z,2,3,1,0

result:

    time,module_2_processdata,module_1_processdata
    2021-02-01T05:03:43.353Z,24#1#0$3#1#0,