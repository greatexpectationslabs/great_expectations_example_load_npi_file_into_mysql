# Great Expectations Example
NPI A toy data project based on the collected works of Charles Dickens.


### Installation


1. We recommend you create a fresh new Python virtual environment
2. Install Great Expectations in this e
3. Clone this repo

mysql_db:
  url: mysql://user:password@host/database    


`python aux_scripts/create_table_from_npi_file.py npi_import_raw` 
    
`./pipeline/data_pipeline.sh npi_data/npi_files/npidata_pfile_20050523-20190908_0.csv npi_import_raw`

`./pipeline/data_pipeline.sh new_data/npidata_pfile_20050523-20191001_1.csv npi_import_raw`