import os
import json
from datetime import datetime
from HW4_nt import normalized_text

class TextRecord:
    def __init__(self, text):
        self.text = normalized_text(text)

    def save_to_txt_file(self, content):
        with open("generated_news.txt", "a", encoding="utf-8") as file:
            file.write(content + "\n\n")

class News(TextRecord):
    def __init__(self, text, city):
        super().__init__(text)
        self.city = city
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M")

    def publish(self):
        content = f"News -------------------------\n{self.text}\n{self.city}, {self.date}"
        self.save_to_txt_file(content)


class PrivateAd (TextRecord):
    def __init__(self, text, expiration_date):
        super().__init__(text)
        self.expiration_date = datetime.strptime(expiration_date, "%Y-%m-%d").date()
        self.days_left = (self.expiration_date - datetime.now().date()).days


    def publish(self):
        content = f"Private Ad -------------------\n{self.text}\nActual until: {self.expiration_date.strftime('%Y-%m-%d')}, {self.days_left} days left"
        self.save_to_txt_file(content)


class QuoteOfTheDay(TextRecord):
    def __init__(self, text, author):
        super().__init__(text)
        self.author = author

    def publish(self):
        content = f"Quote of the day -------------\n{self.text}\nAuthor: {self.author}"
        self.save_to_txt_file(content)


class NewsManager:
    def __init__(self):
        self.choices = {
            "1": self.create_news,
            "2": self.create_private_ad,
            "3": self.create_quote
        }

    def user_menu(self):
        print("Please choose how you want to add new record: \n1 - Manually \n2 - From TXT file \n3 - From JSON file")
        choice = input("Enter your choice: ")

        if choice == "1":
            self.manual_entry_menu()
        elif choice == "2":
            file_path = input("Enter TXT file path or leave empty to use default: ").strip()
            file_manager = FileRecordManager(file_path if file_path else None)
            file_manager.process_file()
        elif choice == "3":
            file_path = input("Enter JSON file path or leave empty to use default: ").strip()
            json_manager = JSONRecordManager(file_path if file_path else None)
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
        news = News(text, city)
        news.publish()
        print("News added successfully to the txt file")

    def create_private_ad(self):
        text = input("Enter ad text: ")
        expiration_date = input("Enter expiration date (yyyy-mm-dd): ")
        private_ad = PrivateAd(text, expiration_date)
        private_ad.publish()
        print("Private ad added successfully to the txt file")

    def create_quote(self):
        text = input("Enter quote text: ")
        author = input("Enter author: ")
        quote = QuoteOfTheDay(text, author)
        quote.publish()
        print("Quote added successfully to the txt file")

class FileRecordManager:
    def __init__(self, file_path=None):
        self.file_path = file_path or "input_records.txt"

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
            news = News(text, city)
            news.publish()
        elif record_type == "PrivateAd":
            text, expiration_date = data
            ad = PrivateAd(text, expiration_date)
            ad.publish()
        elif record_type == "Quote":
            text, author = data
            quote = QuoteOfTheDay(text, author)
            quote.publish()
        else:
            print(f"Unexpected record_type: {record_type}")

class JSONRecordManager:
    def __init__(self, file_path=None):
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
            news = News(text, city)
            news.publish()
        elif record_type == "PrivateAd":
            text = record.get("text")
            expiration_date = record.get("expiration_date")
            ad = PrivateAd(text, expiration_date)
            ad.publish()
        elif record_type == "Quote":
            text = record.get("text")
            author = record.get("author")
            quote = QuoteOfTheDay(text, author)
            quote.publish()
        else:
            print(f"Unexpected record_type: {record_type}")

if __name__ == "__main__":
    manager = NewsManager()
    manager.user_menu()