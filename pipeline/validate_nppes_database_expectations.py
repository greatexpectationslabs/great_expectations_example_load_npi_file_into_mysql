import sys
import pandas as pd
import json
import great_expectations as ge
from great_expectations.datasource.types import BatchKwargs
from datetime import datetime
import sqlalchemy
from sqlalchemy import create_engine
from ruamel.yaml import YAML, YAMLError
yaml = YAML()
yaml.indent(mapping=2, sequence=4, offset=2)
yaml.default_flow_style = False

def __main__():
    if len(sys.argv) <= 2:
        print("Please specify a filepath, table name and run id")
        sys.exit(2)

    new_npi_file_path = sys.argv[1]
    table_name = sys.argv[2]
    run_id = sys.argv[3]


    context = ge.data_context.DataContext()


    data_asset_name_0 = "npi_data__dir/default/npi_files"
    expectation_suite_name_0 = "warning"

    batch0 = context.get_batch(data_asset_name_0, expectation_suite_name_0, BatchKwargs(path=new_npi_file_path))

    results = context.run_validation_operator(
        assets_to_validate=[batch0],
        run_id=run_id,
        validation_operator_name="action_list_operator",
    )

    with open("great_expectations/uncommitted/config_variables.yml", "r") as data:
        sql_alchemy_url = yaml.load(data)['mysql_db']['url']

        data_asset_name_1 = "mysql_db/default/npi_import_raw"
        expectation_suite_name_1 = "warning"
    results = context.run_validation_operator(
        assets_to_validate=[(data_asset_name_1, expectation_suite_name_1, BatchKwargs(table=table_name))],
        run_id=run_id,
        validation_operator_name="action_list_operator",
    )

    if not results["success"]:
        # print("Failure: the data loaded from the file into the table is not valid.")
        sys.exit(1)
    else:
        # print("Success: the data loaded from the file into the table is valid.")
        sys.exit(0)

if __name__=="__main__":
    __main__()