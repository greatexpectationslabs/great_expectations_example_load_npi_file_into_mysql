import sys
import pandas as pd
import great_expectations as ge
from great_expectations.datasource.types import BatchKwargs

def __main__():
    if len(sys.argv) <= 2:
        print("Please specify a filepath and run id")
        sys.exit(2)

    new_npi_file_path = sys.argv[1]
    run_id = sys.argv[2]

    print("file : {0:s}, run_id: {1:s}".format(new_npi_file_path, run_id))

    context = ge.data_context.DataContext()

    data_asset_name_0 = "npi_data__dir/default/npi_files"
    expectation_suite_name_0 = "warning"

    batch0 = context.get_batch(data_asset_name_0, expectation_suite_name_0, BatchKwargs(path=new_npi_file_path))

    results = context.run_validation_operator(
        assets_to_validate=[batch0],
        run_id=run_id,
        validation_operator_name="action_list_operator",
    )

    if not results["success"]:
        # print("Failure: the NPI file is not valid")
        sys.exit(1)
    else:
        # print("Success: the NPI file is valid")
        sys.exit(0)

if __name__=="__main__":
    __main__()