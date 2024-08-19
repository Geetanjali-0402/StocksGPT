import time
import threading
import sqlite3
from datetime import datetime, timedelta
from src.Data.data_utils import NSE_Data_Appender as nda

# res=0

def background_task():
    # global res
    update_table()
    # print(res)
    # res+=1
    while True:
        # Get the current time
        now = time.localtime()
        # Check if it's 3 PM
        if now.tm_hour == 15 and now.tm_min == 0:
            # Execute your task here
            print("Executing task at 3 PM")

            # update_thread = threading.Thread(target=update_table)
            # update_thread.start()
            # update_thread.join()

            update_table()
            
            # Sleep for 1 minute to avoid repeated execution within the same minute
            time.sleep(60)
            # Calculate the time until 2:55 PM of the next day
            tomorrow = (now.tm_wday + 1) % 7  # Get the day of the week for tomorrow
            seconds_until_2_55_pm = (24 * 3600) - (now.tm_hour * 3600 + now.tm_min * 60 + now.tm_sec) + (2 * 3600 + 55 * 60)
            time.sleep(seconds_until_2_55_pm)  # Sleep until 2:55 PM of the next day
        else:
            # Sleep for a short duration to avoid consuming too much CPU
            time.sleep(1)

def update_table():
    print("Updating table")

    start_date,end_date = nda.get_last_appended_date()
    print("date range found",start_date,end_date)
    time.sleep(1)

    nda.download_bhavcopy(start_date,end_date)
    print("bhavcopy downloaded")
    time.sleep(1)

    c = sqlite3.connect('src/Data/StockBuddyDB.db')
    c.close()

    nda.filtering()
    print("data filtered")
    time.sleep(1)

    nda.integrate()
    print("data integrated with sqlite table")


    # sqlite3.Connection(None).close()
    
    print("All operations completed")


# Start the background task when the server starts
# background_thread = threading.Thread(target=background_task)
# background_thread.daemon = True  # Daemonize the thread so it automatically stops when the main thread stops
# background_thread.start()

# background_thread = threading.Thread(target=background_task)
# background_thread.daemon = True  # Daemonize the thread so it automatically stops when the main thread stops
# background_thread.start()