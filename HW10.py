import json
import os
import pyodbc
from datetime import datetime
from xml.etree import ElementTree as ET
from HW4_nt import normalized_text

class DatabaseManager:
    def __init__(self):
        self.connection = pyodbc.connect(
            'DRIVER={SQLite3 ODBC Driver};'
            'Direct=True;'
            'Database=generated_news.db;'
            'String Types=Unicode'
        )
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''create table if not exists News (
                               id integer primary key autoincrement,
                               text text not null,
                               city text,
                               date text default current_timestamp,
                               unique(text, city))
                               ''')

        self.cursor.execute('''create table if not exists PrivateAd (
                                       id integer primary key autoincrement,
                                       text text not null,
                                       expiration_date text,
                                       days_left integer text,
                                       unique(text, expiration_date))''')

        self.cursor.execute('''create table if not exists QuoteOfTheDay (
                                       id integer primary key autoincrement,
                                       text text not null,
                                       author text,
                                       unique(text, author))''')

        self.connection.commit()

    def record_exists(self, table, conditions, params):
        query = f"select 1 from {table} where {conditions}"
        self.cursor.execute(query, params)
        return self.cursor.fetchone() is not None
    def insert_news(self, text, city):
        if not self.record_exists("News", "text = ? and city = ?", (text, city)):
            self.cursor.execute('''insert into News (text, city)
                                   values(?, ?)''', (text, city))
            self.connection.commit()
            print("News successfully added.")
        else:
            print("Such news already exists.")

    def insert_private_ad(self, text, expiration_date):
        expiration_date_obj = datetime.strptime(expiration_date, "%Y-%m-%d").date()
        days_left = (expiration_date_obj - datetime.now().date()).days

        if not self.record_exists("PrivateAd", "text = ? and expiration_date = ?", (text, expiration_date)):
            self.cursor.execute('''insert into PrivateAd (text, expiration_date, days_left)
            values(?, ?, ?)''', (text, expiration_date, days_left))
            self.connection.commit()
            print("Private Ad successfully added.")
        else:
            print("Such private Ad already exists.")

    def insert_quote(self, text, author):
        if not self.record_exists("QuoteOfTheDay", "text = ? and author = ?", (text, author)):
            self.cursor.execute('''insert into QuoteOfTheDay (text, author)
                                   values(?, ?)''', (text, author))
            self.connection.commit()
            print("Quote successfully added.")
        else:
            print("Such quote already exists.")

    def close(self):
        self.connection.close()

class TextRecord:
    def __init__(self, text):
        self.text = normalized_text(text)

    def save_to_txt_file(self, content):
        with open("generated_news.txt", "a", encoding="utf-8") as file:
            file.write(content + "\n\n")

class News(TextRecord):
    def __init__(self, text, city, db_manager):
        super().__init__(text)
        self.city = city
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.db_manager = db_manager

    def publish(self):
        content = f"News -------------------------\n{self.text}\n{self.city}, {self.date}"
        self.save_to_txt_file(content)
        self.db_manager.insert_news(self.text, self.city)


class PrivateAd (TextRecord):
    def __init__(self, text, expiration_date, db_manager):
        super().__init__(text)
        self.expiration_date = datetime.strptime(expiration_date, "%Y-%m-%d").date()
        self.days_left = (self.expiration_date - datetime.now().date()).days
        self.db_manager = db_manager


    def publish(self):
        days_left = (self.expiration_date - datetime.now().date()).days
        content = f"Private Ad -------------------\n{self.text}\nActual until: {self.expiration_date.strftime('%Y-%m-%d')}, {self.days_left} days left"
        self.save_to_txt_file(content)
        self.db_manager.insert_private_ad(self.text, self.expiration_date.strftime('%Y-%m-%d'))


class QuoteOfTheDay(TextRecord):
    def __init__(self, text, author, db_manager):
        super().__init__(text)
        self.author = author
        self.db_manager = db_manager

    def publish(self):
        content = f"Quote of the day -------------\n{self.text}\nAuthor: {self.author}"
        self.save_to_txt_file(content)
        self.db_manager.insert_quote(self.text, self.author)


class NewsManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.choices = {
            "1": self.create_news,
            "2": self.create_private_ad,
            "3": self.create_quote
        }

    def user_menu(self):
        print("Please choose how you want to add new record: \n1 - Manually \n2 - From TXT file \n3 - From JSON file \n4 - From XML file")
        choice = input("Enter your choice: ")

        if choice == "1":
            self.manual_entry_menu()
        elif choice == "2":
            file_path = input("Enter TXT file path or leave empty to use default: ").strip()
            file_manager = FileRecordManager(self.db_manager, file_path if file_path else None)
            file_manager.process_file()
        elif choice == "3":
            file_path = input("Enter JSON file path or leave empty to use default: ").strip()
            json_manager = JSONRecordManager(self.db_manager, file_path if file_path else None)
            json_manager.process_file()
        elif choice == "4":
            file_path = input("Enter XML file path or leave empty to use default: ").strip()
            json_manager = XMLRecordManager(self.db_manager, file_path if file_path else None)
            json_manager.process_file()
        else:
            print("Invalid choice, please try again.")
            self.user_menu()

    def manual_entry_menu(self):
        print("Please choose what you want to add: \n1 - News \n2 - Private Ad \n3 - Quote of the day")
        choice = input("Enter your choice: ")
        action = self.choices.get(choice)
        if action:
            action()
        else:
            print("Invalid choice, please try again.")

    def create_news(self):
        text = input("Enter news text: ")
        city = input("Enter city: ")
        news = News(text, city, self.db_manager)
        news.publish()
        print("News added successfully to the txt file")

    def create_private_ad(self):
        text = input("Enter ad text: ")
        expiration_date = input("Enter expiration date (yyyy-mm-dd): ")
        private_ad = PrivateAd(text, expiration_date, self.db_manager)
        private_ad.publish()
        print("Private ad added successfully to the txt file")

    def create_quote(self):
        text = input("Enter quote text: ")
        author = input("Enter author: ")
        quote = QuoteOfTheDay(text, author, self.db_manager)
        quote.publish()
        print("Quote added successfully to the txt file")

class FileRecordManager:
    def __init__(self, db_manager, file_path=None):
        self.db_manager = db_manager
        self.file_path = file_path or "input_records_old.txt"

    def process_file(self):
        if not os.path.exists(self.file_path):
            print(f"TXT file not found here: '{self.file_path}'.")
            return
        with open(self.file_path, "r", encoding="utf-8") as file:
            for line in file:
                record_type, *data=line.strip().split(";")
                self.process_record(record_type, data)
        os.remove(self.file_path)
        print(f"File '{self.file_path}' removed after successful processing.")

    def process_record(self, record_type, data):
        if record_type == "News":
            text, city = data
            news = News(text, city, self.db_manager)
            news.publish()
        elif record_type == "PrivateAd":
            text, expiration_date = data
            ad = PrivateAd(text, expiration_date, self.db_manager)
            ad.publish()
        elif record_type == "Quote":
            text, author = data
            quote = QuoteOfTheDay(text, author, self.db_manager)
            quote.publish()
        else:
            print(f"Unexpected record_type: {record_type}")

class JSONRecordManager:
    def __init__(self, db_manager, file_path=None):
        self.db_manager = db_manager
        self.file_path = file_path or "input_records.json"

    def process_file(self):
        if not os.path.exists(self.file_path):
            print(f"JSON file not found here: '{self.file_path}'.")
            return
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                records = json.load(file)
            for record in records:
                self.process_record(record)

            os.remove(self.file_path)
            print(f"File '{self.file_path}' removed after successful processing.")
        except json.JSONDecodeError:
                print("Invalid JSON format.")

    def process_record(self, record):
        record_type = record.get("type")
        if record_type == "News":
            text = record.get("text")
            city = record.get("city")
            news = News(text, city, self.db_manager)
            news.publish()
        elif record_type == "PrivateAd":
            text = record.get("text")
            expiration_date = record.get("expiration_date")
            ad = PrivateAd(text, expiration_date, self.db_manager)
            ad.publish()
        elif record_type == "Quote":
            text = record.get("text")
            author = record.get("author")
            quote = QuoteOfTheDay(text, author, self.db_manager)
            quote.publish()
        else:
            print(f"Unexpected record_type: {record_type}")

class XMLRecordManager:
    def __init__(self, db_manager, file_path=None):
        self.db_manager = db_manager
        self.file_path = file_path or "input_records.xml"

    def process_file(self):
        if not os.path.exists(self.file_path):
            print(f"XML file not found here: '{self.file_path}'.")
            return
        try:
            tree = ET.parse(self.file_path)
            root = tree.getroot()
            for record in root.findall("record"):
                record_type = record.get("type")
                self.process_record(record_type, record)
            os.remove(self.file_path)
            print(f"File '{self.file_path}' removed after successful processing.")
        except ET.ParseError:
            print("Invalid XML format.")

    def process_record(self, record_type, record):
        if record_type == "News":
            text = record.find("text").text
            city = record.find("city").text
            news = News(text, city, self.db_manager)
            news.publish()
        elif record_type == "PrivateAd":
            text = record.find("text").text
            expiration_date = record.find("expiration_date").text
            ad = PrivateAd(text, expiration_date, self.db_manager)
            ad.publish()
        elif record_type == "Quote":
            text = record.find("text").text
            author = record.find("author").text
            quote = QuoteOfTheDay(text, author, self.db_manager)
            quote.publish()

if __name__ == "__main__":
    db_manager = DatabaseManager()
    manager = NewsManager(db_manager)

    file_manager = FileRecordManager(db_manager)
    json_manager = JSONRecordManager(db_manager)
    xml_manager = XMLRecordManager(db_manager)

    manager.user_menu()
    db_manager.close()