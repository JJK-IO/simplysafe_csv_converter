from utils import *

if __name__ == "__main__":
    export_file_location = "files/robinhood"

    # Convert SS Exported CSV to Importable CSV
    # convert_export_to_import(export_file_location)

    # Pull Assets from Robinhood
    pull_from_rh(export_directory=export_file_location)
