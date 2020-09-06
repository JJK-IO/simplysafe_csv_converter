# SimplySafe CSV Converter

## Initial Setup
Make sure you run `pip install requirements.txt`

## Convert a SimplySafe exported Spreadsheet to an importable spreadsheet

1. Modify `script.py` with the location of the exported spreadsheet.
1. Run `python script.py`
1. The export should be named `converted-[original file name].csv`

## Pull your Robinhood securities

1. Make a copy of `.sample.env` and name it `.env`
1. Fill in the credentials for Robinhood in the `.env` file.
    - 2FA with QR Generator Code Recommended.
    - QR code tha will be used to generate mfa_code (optional but recommended) To get QR code, set up 2FA in Security, get Authentication App, and click "Can't Scan It?"
1. Uncomment `pull_from_rh()` and comment the `convert_export_to_import()` line 
1. Run `python script.py`
1. The exported file should be named `rh_export.csv`