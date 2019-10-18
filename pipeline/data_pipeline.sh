#!/bin/bash

# Data Pipeline

# $1: the path of the NPI file that the pipeline should process
# $2: the name of the table in the MySQL db to the file's data should be loaded into

# Generate a run id - a pipeline run id, a timestamp or any other string that is meaningful to you
# and will help you refer to validation results. We recommend they be chronologically sortable.
RUNID=$(date +"%Y-%d-%m_%H:%M:%S")

echo "Validating the NPPES file using Great Expectations..."
if python pipeline/validate_nppes_file_expectations.py $1 $RUNID; then
  echo "The NPPES file meets critical expectations"
  echo "Loading the NPPES file into MySQL..."
  if python pipeline/load_csv_file_into_mysql.py $1 $2; then
    echo "Loaded the NPPES file into MySQL"
    echo "Validating the loaded NPPES data in MySQL using Great Expectations..."
    if python pipeline/validate_nppes_database_expectations.py $1 $2 $RUNID; then
      echo "Loaded NPPES data in MySQL meets critical expectations."
    else
      echo "Loaded NPPES data in MySQL failed to meet critical expectations. See great_expectations/uncommitted/data_docs/local_site/index.html"
    fi
  else
      echo "Failed to load the NPPES file into MySQL!!!"
  fi
else
  echo "The NPPES failed to meet critical expectations. See great_expectations/uncommitted/data_docs/local_site/index.html"
fi