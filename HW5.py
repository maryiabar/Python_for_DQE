from datetime import datetime

class TextRecord:
    def __init__(self, text):
        self.text = text

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

if __name__ == "__main__":
    manager = NewsManager()
    manager.user_menu()