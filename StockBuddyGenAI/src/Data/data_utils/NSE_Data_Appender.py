import os
import bhavcopy as bv
import pandas as pd
import sqlite3
from datetime import datetime, timedelta


def download_bhavcopy(start_date,end_date):
    # Storing the current working directory
    src_path = os.getcwd()

    remaining_path = "src/Data"
    data_storage = os.path.join(src_path, remaining_path)

    wait_time = [1, 2]
    nse = bv.bhavcopy("equities", start_date,end_date, data_storage, wait_time)
    nse.get_data()


    """ Bringing back the control to Original working Directory
    Since Bhavcopy module changes it to somewhere else"""
    os.chdir(src_path)

def integrate():
    csv_file_path = "src/Data/Filtered_stock_data.csv"

    database_file_path = "src/Data/NSE_Yahoo_9_FEB_24.sqlite"


    # Define the name of the SQLite table to store the data
    table_name = 'NSE'

    # Read the CSV file into a pandas DataFrame
    data = pd.read_csv(csv_file_path)

    # Create the 'id' column in the DataFrame by concatenating 'Date' and 'ticker' columns
    data['id'] = data['Date'] + '_' + data['ticker']

    # Create a connection to the SQLite database
    conn = sqlite3.connect(database_file_path)

    # Append data from the DataFrame to the existing SQLite table
    # We use 'append' to add the data to the existing table
    data.to_sql(table_name, conn, if_exists='append', index=False)

    # Commit the changes and close the database connection
    conn.commit()
    conn.close()

    print(f"Data from {csv_file_path} has been integrated into the SQLite table '{table_name}' in {database_file_path}.")

    # Clear the data in the CSV file while preserving column headers
    # Retrieve the column headers from the data DataFrame
    columns = data.columns

    # Open the CSV file in write mode
    with open(csv_file_path, 'w') as csv_file:
        # Write the column headers to the CSV file
        csv_file.write(','.join(columns) + '\n')

def filtering():
    
    # Define file paths
    input_file_path = "src/Data/equities.csv"
   
    output_file_path = "src/Data/Filtered_stock_data.csv"


    # Read the input CSV file into a pandas DataFrame
    #df = pd.read_csv(input_file_path)
    df = pd.read_csv(input_file_path, on_bad_lines='skip')


    # Filter the rows where SERIES is equal to 'EQ'
    df_filtered = df[df['SERIES'] == 'EQ']

    # Create a new DataFrame with the desired columns and transformed data
    output_df = pd.DataFrame({
        'Date': df_filtered['TIMESTAMP'],  # Copy Date (Timestamp) from input file
        'Open': df_filtered['OPEN'],  # Copy Open from input file
        'high': df_filtered['HIGH'],  # Copy High from input file
        'low': df_filtered['LOW'],  # Copy Low from input file
        'close': df_filtered['LAST'],  # Set Close to LAST from input file
        'Adj_Close': df_filtered['CLOSE'],  # Set Adj_Close to CLOSE from input file
        'Volume': df_filtered['TOTTRDQTY'],  # Set Volume to TOTTRDQTY from input file
        'ticker': df_filtered['SYMBOL'] + '.NS'  # Append '.NS' to SYMBOL to form ticker
    })

    # Write the output DataFrame to a CSV file
    output_df.to_csv(output_file_path, index=False)

    print(f"Data successfully written to {output_file_path}.")

    # Clear the data in the CSV file while preserving column headers
    # Retrieve the column headers from the data DataFrame
    columns = df.columns

    # Open the CSV file in write mode
    with open(input_file_path, 'w') as csv_file:
        # Write the column headers to the CSV file
        csv_file.write(','.join(columns) + '\n')

   
def get_last_appended_date():
        
    db_path = 'src/Data/NSE_Yahoo_9_FEB_24.sqlite'  # Replace with your database path
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Calculate today's date
    today_date = datetime.today().strftime('%Y-%m-%d')

    # Query to find the latest date in the SQLite table
    # Replace 'your_table_name' with the name of your SQLite table
    cursor.execute("SELECT MAX(Date) FROM NSE")  # Replace 'Date' with the name of the date column in your table
    latest_date = cursor.fetchone()[0]

    # Convert the latest date to a datetime object
    if latest_date is not None:
        latest_date_dt = datetime.strptime(latest_date, '%Y-%m-%d')
    else:
        # If there's no latest date, you can handle it as needed (e.g., set it to a default date)
        latest_date_dt = None

    # Calculate start date
    # If there is a latest date, set the start date to one day after the latest date
    # Otherwise, start date could be a specific default date depending on your application
    if latest_date_dt:
        start_date_dt = latest_date_dt + timedelta(days=1)
    else:
        start_date_dt = datetime.strptime('default_start_date', '%Y-%m-%d')  # Replace 'default_start_date' with your preferred start date

    # Convert start and end dates back to strings in the desired format
    start_date = start_date_dt.strftime('%Y-%m-%d')
    end_date = today_date
    # Close the database connection
    cursor.close()
    conn.close()

    return start_date,end_date