import sys
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


    with open("great_expectations/uncommitted/config_variables.yml", "r") as data:
        sql_alchemy_url = yaml.load(data)['mysql_db']['url']

        load_file_into_db(sql_alchemy_url, new_npi_file_path, table_name)
        data_asset_name_1 = "mysql_db/default/npi_import_raw"
        expectation_suite_name_1 = "warning"

if __name__=="__main__":
    __main__()