## lopco-flatten-non-unique-csv-worker

Flattens a CSV file with multiple lines per timestamp by creating nested sub tables.

### Configuration

`delimiter`: Delimiter used in the CSV file.

`time_column`: Column containing timestamps.

`name_pattern`: Defines how the names for new columns are generated and requires the `unique_item` placeholder.

`unique_column`: If provided, the given value is added to the names of newly generated columns.

    Examples:
    
    name_pattern = {unique_column}_{unique_item}_processdata
    
        time,module,station,process,errorcode
        2021-02-01T05:03:37.526Z,1,3,1,0
        2021-02-01T05:03:43.353Z,2,24,1,0
        2021-02-01T05:03:43.353Z,2,3,1,0
    
    result:
    
        time,module_2_processdata,module_1_processdata
        2021-02-01T05:03:37.526Z,,3;1;0
        2021-02-01T05:03:43.353Z,24;1;0?3;1;0,
        
    ----------------------------------------------------------
    
    name_pattern = {unique_item}_processdata
    
        time,module,station,process,errorcode
        2021-02-01T05:03:37.526Z,1,3,1,0
        2021-02-01T05:03:43.353Z,2,24,1,0
        2021-02-01T05:03:43.353Z,2,3,1,0
    
    result:
    
        time,2_processdata,1_processdata
        2021-02-01T05:03:37.526Z,,3;1;0
        2021-02-01T05:03:43.353Z,24;1;0?3;1;0,

`sub_table_delimiters`: Takes two comma separated values and controls how sub tables are delimited.

    Examples:
    
    sub_table_delimiters = ;,?
    
        time,module,station,process,errorcode
        2021-02-01T05:03:43.353Z,2,24,1,0
        2021-02-01T05:03:43.353Z,2,3,1,0
    
    result:
    
        time,module_2_processdata,module_1_processdata
        2021-02-01T05:03:43.353Z,24;1;0?3;1;0,
    
    ----------------------------------------------------------

    sub_table_delimiters = #,$
    
        time,module,station,process,errorcode
        2021-02-01T05:03:43.353Z,2,24,1,0
        2021-02-01T05:03:43.353Z,2,3,1,0
    
    result:
    
        time,module_2_processdata,module_1_processdata
        2021-02-01T05:03:43.353Z,24#1#0$3#1#0,

### Inputs

Type: single

`source_csv`: CSV file to flatten.

### Outputs

Type: single

`output_file`: Result CSV file with sub tables.

`sub_table_header`: Generated header for sub tables.

### Description

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
                    "name": "sub_table_map",
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
