import json
import tkinter as tk
import threading
import mysql.connector
import pymysql
from apscheduler.schedulers.background import BackgroundScheduler
import os
from Database_.main import archive_data
from Database_.Extra import process_json_data
from Database_.Video import process_data
from analyser import Query
from emai import send_mail
ua = []
stop_event = threading.Event()
scheduler = None

# Database_ configuration
'''db_config = {
    "host": "localhost",
    "user": "root",
    "password": "@Krsnaisthebest1",
    "database": "Crawler"
    
}'''



def save_to_directory(path, files):
    cnt = 1
    for y in files:
        tmp_path = open(os.path.join(path, str(cnt) + ".json"), "w")
        json.dump(y, tmp_path)
        cnt += 1


def fetch_give():
    global ua
    try:
        conn = pymysql.connect(host='localhost', port=3306, user='root', password='@Krsnaisthebest1',
                               database='Crawler', charset="utf8mb4")

        if conn.open:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM urls")

            data = cursor.fetchall()
            ua = [item[0] for item in data]
    except mysql.connector.Error as e:
        print(f"Error fetching data from the database: {e}")
    finally:
        cursor.close()
        conn.close()

    generic, extra = Query(ua, True, 0, False).get_json_file()
    save_to_directory("cache", [generic, extra])
    #process_and_store_json("cache")
    archive_data("cache")
    process_json_data("cache")
    #send_mail()
    return ua
    # for u in ua:   # return ua. it consists of extra links in array
    #     print(u)


def get_url_and_process():
    data_to_insert = [(url_entry.get(),)]

    try:
        conn = pymysql.connect(host='localhost', port=3306, user='root', password='@Krsnaisthebest1',
                               database='Crawler', charset="utf8mb4")

        if conn.open:  # previous code: conn.is_connected()
            cursor = conn.cursor()
            insert_query = "INSERT INTO urls (url) VALUES (%s)"
            cursor.executemany(insert_query, data_to_insert)
            conn.commit()
            print("Data inserted successfully.")
    except Exception as e:
        print(f"Error inserting data into the database: {e}")
    finally:
        cursor.close()
        conn.close()


def send_to_ai():
    # fix-1 addition of video and website link separator
    global scheduler
    while not stop_event.is_set():
        if scheduler is not None:
            scheduler.shutdown()

        scheduler = BackgroundScheduler(timezone='Asia/Kolkata')
        scheduler.add_job(fetch_give, 'interval', hours=3)
        scheduler.start()

        try:
            while True:
                pass
        except (KeyboardInterrupt, SystemExit):
            pass


def start_processing():
    global stop_event
    fetch_give()
    stop_event.clear()
    threading.Thread(target=send_to_ai).start()


def stop_processing():
    global stop_event, scheduler
    stop_event.set()
    if scheduler is not None:
        scheduler.shutdown()


def delete_url_from_database(url_to_delete):
    try:
        conn = pymysql.connect(host='localhost', port=3306, user='root', password='@Krsnaisthebest1',
                               database='Crawler', charset="utf8mb4")

        if conn.open:
            cursor = conn.cursor()
            delete_query = "DELETE FROM urls WHERE url = %s"
            cursor.execute(delete_query, (url_to_delete,))
            conn.commit()
            print("URL deleted successfully.")
    except Exception as e:
        print(f"Error deleting URL from the database: {e}")
    finally:
        cursor.close()
        conn.close()


def load_urls_into_listbox():
    try:
        conn = pymysql.connect(host='localhost', port=3306, user='root', password='@Krsnaisthebest1',
                               database='Crawler', charset="utf8mb4")

        if conn.open:
            cursor = conn.cursor()
            select_query = "SELECT url FROM urls"
            cursor.execute(select_query)
            data = cursor.fetchall()
            url_listbox.delete(0, tk.END)

            for row in data:
                url_listbox.insert(tk.END, row[0])
    except Exception as e:
        print(f"Error fetching URLs from the database: {e}")
    finally:
        cursor.close()
        conn.close()


def delete_selected_url():
    selected_index = url_listbox.curselection()
    if selected_index:
        selected_url = url_listbox.get(selected_index)
        delete_url_from_database(selected_url)
        load_urls_into_listbox()


root = tk.Tk()
root.title("AI Model Data Collector")

url_label = tk.Label(root, text="Enter URL:")
url_label.pack()

url_entry = tk.Entry(root, width=50)
url_entry.pack()

add_button = tk.Button(root, text="Add URL", command=get_url_and_process)
add_button.pack()

url_listbox = tk.Listbox(root, selectmode=tk.SINGLE)
url_listbox.pack()

load_urls_button = tk.Button(root, text="Load URLs", command=load_urls_into_listbox)
load_urls_button.pack()

delete_button = tk.Button(root, text="Delete URL", command=delete_selected_url)
delete_button.pack()

start_button = tk.Button(root, text="Start Processing", command=start_processing)
start_button.pack()

stop_button = tk.Button(root, text="Stop Processing", command=stop_processing)
stop_button.pack()

status_label = tk.Label(root, text="")
status_label.pack()

root.mainloop()
