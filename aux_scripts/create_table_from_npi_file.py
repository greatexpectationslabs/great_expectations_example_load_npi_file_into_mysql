import sys
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
from ruamel.yaml import YAML, YAMLError
yaml = YAML()
yaml.indent(mapping=2, sequence=4, offset=2)
yaml.default_flow_style = False


def create_create_table_sql_str(df, table_name):
    create_table_sql_str = "CREATE TABLE IF NOT EXISTS {0:s} (\n".format(table_name)
    for idx, column_name in enumerate(df.columns):
        if df[column_name].str.len().max() > 0:
            create_table_sql_str += "`{0:s}` VARCHAR({1:d}) NULL".format(column_name[:64],
                                                                         int(df[column_name].str.len().max()))
        else:
            create_table_sql_str += "`{0:s}` VARCHAR(2)".format(column_name[:64])
        if idx < (len(df.columns) - 1):
            create_table_sql_str += ",\n"
    create_table_sql_str += ")  ENGINE=INNODB"

    return create_table_sql_str

def __main__():
    if len(sys.argv) <= 1:
        print("Please specify the name of the table to create.")
        return

    table_name = sys.argv[1]


    df = pd.read_csv('npi_data/npi_files/npidata_pfile_20050523-20190908_0.csv', sep=",", dtype=object)


    with open("great_expectations/uncommitted/config_variables.yml", "r") as data:
        config_dict = yaml.load(data)

        engine = create_engine(config_dict['mysql_db']['url'])

        create_table_sql_str = create_create_table_sql_str(df, table_name)
        with engine.connect() as con:
            rs = con.execute(create_table_sql_str)

            print("Success - create table " + table_name)

if __name__=="__main__":
    __main__()