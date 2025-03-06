import os
import mysql.connector
import logging
import traceback

# MySQL Configuration
DB_NAME = "database_name"
DB_USER = "database_user"
DB_PASS = "database_password"
CSV_FOLDER = r"D:\CSV_FOLDER"
LOG_FILE = r"D:\CSV_FOLDER\error_log.txt"

# Set up logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(message)s")

def convert_to_table_name(filename):
    """Removes '_dbo___' prefix, '_' suffix, and converts to lowercase."""
    if filename.startswith("_dbo___"):
        filename = filename[len("_dbo___"):]  # Remove the prefix

    if filename.endswith("_"):
        filename = filename[:-1]  # Remove the suffix

    return filename.lower()  # Convert to lowercase

def import_csv_to_mysql(csv_file, table_name):
    """Executes MySQL LOAD DATA command to import CSV into the specified table."""
    try:
        # Convert Windows backslashes to forward slashes for MySQL compatibility
        csv_file = csv_file.replace("\\", "/")

        connection = mysql.connector.connect(
            host="localhost", user=DB_USER, password=DB_PASS, database=DB_NAME, allow_local_infile=True
        )
        cursor = connection.cursor()

        load_query = f"""
        LOAD DATA LOCAL INFILE '{csv_file}'
        INTO TABLE `{table_name}`
        FIELDS TERMINATED BY ',' 
        ENCLOSED BY '"'
        LINES TERMINATED BY '\r\n'
        IGNORE 1 ROWS;
        """

        cursor.execute("SET GLOBAL local_infile = 1;")  # Enable LOCAL INFILE
        cursor.execute(load_query)
        connection.commit()

        msg = f"✅ Successfully imported {csv_file} into `{table_name}`"
        print(msg)
        logging.info(msg)

    except mysql.connector.Error as err:
        error_message = f"❌ ERROR importing {csv_file} into `{table_name}`: {err}"
        print(error_message)
        logging.error(error_message)
        logging.error(traceback.format_exc())  # Logs the full error traceback

    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    print("🔄 Starting CSV Import Process...\n")

    if not os.path.exists(CSV_FOLDER):
        error_msg = f"❌ Error: Folder {CSV_FOLDER} not found!"
        print(error_msg)
        logging.error(error_msg)
        exit(1)

    csv_files = [f for f in os.listdir(CSV_FOLDER) if f.endswith(".csv")]

    if not csv_files:
        print("ℹ️ No CSV files found for import.")
        exit(0)

    for file in csv_files:
        csv_path = os.path.join(CSV_FOLDER, file)
        csv_path = csv_path.replace("\\", "/")  # Convert Windows paths for MySQL
        table_name = convert_to_table_name(os.path.splitext(file)[0])
        print(f"📤 Importing `{csv_path}` into table `{table_name}`...")
        import_csv_to_mysql(csv_path, table_name)

    print("\n✅ All CSV files processed! Check the log file for details.")
