# MSSQL CSV Bulk Import to MySQL

This script automates the process of importing multiple CSV files exported from MSSQL bulk export into a MySQL database. It reads all CSV files from a specified folder, processes their names to match table names in MySQL, and imports the data using `LOAD DATA LOCAL INFILE`. This script I personally developed to process MSSQL CSV files but general CSV files can work with this script.

## Features

-   Automatically detects CSV files in a specified folder.
-   Processes CSV files exported from MSSQL bulk export, removing `_dbo___` prefix and `_` suffix from filenames and converting them to lowercase for table names.
-   Supports general CSV imports as well.
-   Uses `LOAD DATA LOCAL INFILE` for efficient bulk insertion.
-   Supports error logging to track import failures.
-   Handles Windows file path compatibility for MySQL.

## Prerequisites

-   Python 3.x installed
-   MySQL Server installed
-   MySQL Connector for Python: `pip install mysql-connector-python`
-   Ensure MySQL has `local_infile` enabled:
    
    ```sql
    SET GLOBAL local_infile = 1;
    
    ```
    

## Installation

1.  Clone the repository:
    
    ```sh
    git clone https://github.com/yourusername/mssql_csv_bulk_import_to_mysql.git
    cd mssql_csv_bulk_import_to_mysql
    
    ```
    
2.  Install dependencies:
    
    ```sh
    pip install mysql-connector-python
    
    ```
    

## Configuration

Edit `main.py` to match your MySQL credentials and CSV folder path:

```python
DB_NAME = "database_name"
DB_USER = "database_user"
DB_PASS = "database_password"
CSV_FOLDER = r"D:\CSV_FOLDER"
LOG_FILE = r"D:\CSV_FOLDER \error_log.txt"

```

## Usage

Run the script:

```sh
python main.py

```

The script will:

-   Process all `.csv` files in `CSV_FOLDER`
-   Convert filenames into proper table names
-   Attempt to import the data
-   Log errors in `error_log.txt`

## Error Handling

-   Errors during import will be logged in `error_log.txt`.
-   If a file is missing, ensure the correct `CSV_FOLDER` is set.
-   If MySQL reports a file not found error, verify that `local_infile` is enabled.

## License

This project is open-source under the MIT License.

## Contributing

Feel free to modify this script if you need more precise output. Contributions and improvements are welcome!
