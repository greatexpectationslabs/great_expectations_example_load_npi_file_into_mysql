# Great Expectations Example - NPI Files to MySQL With Validation


[Great Expectations](https://greatexpectations.io/) is an open source tool that data teams use to validate, profile an document data to ensure the integrity of their pipelines. 


This repo demonstrates a common pattern of deploying Great Expectations in a data pipeline.

![](images/pipeline_diagram.png)

The pipeline loads an NPI CSV file into a table in MySQL database.
 
The NPI (National Provider Identifier) dataset contains publicly available information about all healthcare providers in the US. The dataset is maintained by the Center for Medicare & Medicaid Services which publishes periodic updates as [CSV files](http://download.cms.gov/nppes/NPI_Files.html).

This example demonstrates how you can use Great Expectations to protect the node against unexpected input data and to test the node's output before additional nodes downstream use this data. In a real deployment our pipeline would be a node in a larger pipeline that would transform the loaded data into some data product. 

Video: 


### What does it show 



### Prerequisites 

1. Python installed (Great Expectations supports both Python 2 and 3, but this example was tested only on Python 3)
2. A MySQL server 


### Installation

1. Create a fresh Python virtual environment (recommended)
2. Install Great Expectations in this environment
3. Clone this repo and cd into it
4. Create `great_expectations/uncommitted/config_variables.yml` file with the following content:
```
mysql_db:
  url: mysql://user:password@host/database (TODO: replace with real credentials) 
validation_notification_slack_webhook: (TODO: Slack webhook URL for notifications)  
```

See https://docs.greatexpectations.io/en/latest/getting_started/cli_init.html#configuring-slack-notifications
5. Create the table in your MySQL database: `python aux_scripts/create_table_from_npi_file.py npi_import_raw` 
6. Build the local Data Docs website: `great_expectations build-docs`

### Running the example

After each run go to `great_expectations/uncommitted/data_docs/local_site/index.html` in your web browser.

1. Run the pipeline on a good file:    
`./pipeline/data_pipeline.sh npi_data/npi_files/npidata_pfile_20050523-20190908_0.csv npi_import_raw`
Validation will be successful.
2. Run the pipeline on a good file again:    
`./pipeline/data_pipeline.sh npi_data/npi_files/npidata_pfile_20050523-20190908_0.csv npi_import_raw`
 Validation will fail, because we did not truncate the table and the row count in the table is greater than the row count in the file.
3. Run the pipeline on a "bad file":    
`./pipeline/data_pipeline.sh new_data/npidata_pfile_20050523-20191001_1.csv npi_import_raw`
The first validation step (validating the file) will fail.
