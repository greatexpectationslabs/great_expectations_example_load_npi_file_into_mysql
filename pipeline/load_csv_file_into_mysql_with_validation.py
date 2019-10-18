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

def load_file_into_db(sql_alchemy_url, file_path, table_name):

    engine = create_engine(sql_alchemy_url)

    load_data_sql_str = """
    load data local infile
    '{0:s}'
    into table {1:s}
    fields terminated by ',' lines terminated by '\n' ignore 1 lines""".format(file_path, table_name)

    with engine.connect() as con:

        rs = con.execute(load_data_sql_str)

def __main__():
    if len(sys.argv) <= 2:
        print("Please specify a filepath a table name.")
        return

    new_npi_file_path = sys.argv[1]
    table_name = sys.argv[2]


    context = ge.data_context.DataContext()

    # Generate a run id - a pipeline run id, a timestamp or any other string that is meaningful to you
    # and will help you refer to validation results. We recommend they be chronologically sortable.
    run_id = datetime.utcnow().isoformat().replace(":", "") + "Z"

    data_asset_name_0 = "npi_data__dir/default/npi_files"
    expectation_suite_name_0 = "warning"

    df = pd.read_csv(new_npi_file_path)
    batch0 = context.get_batch(data_asset_name_0, expectation_suite_name_0, BatchKwargs(df=df))

    results = context.run_validation_operator(
        assets_to_validate=[batch0],
        run_identifier=run_id,
        validation_operator_name="action_list_operator",
    )

    if not results["success"]:
        print("Failure: the NPI file is not valid")
    else:
        with open("great_expectations/uncommitted/config_variables.yml", "r") as data:
            sql_alchemy_url = yaml.load(data)['mysql_db']['url']

        load_file_into_db(sql_alchemy_url, new_npi_file_path, table_name)
        data_asset_name_1 = "mysql_db/default/npi_import_raw"
        expectation_suite_name_1 = "warning"
    results = context.run_validation_operator(
        assets_to_validate=[(data_asset_name_1, expectation_suite_name_1, BatchKwargs(table=table_name))],
        run_identifier=run_id,
        validation_operator_name="action_list_operator",
    )

    if not results["success"]:
        print("Failure: the data loaded from the file into the table is not valid.")
    else:
        print("Success: the data loaded from the file into the table is valid.")

if __name__=="__main__":
    __main__()