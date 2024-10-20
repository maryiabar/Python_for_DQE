import csv
import os
from collections import Counter

# read file with news
def read_news_file(file_path):
    with open(file_path, "r", encoding="utf-8") as news_file:
        news = news_file.read()
    return news

# calculate news' row count
def count_rows_in_file(file_path):
    with open(file_path, "r", encoding="utf-8") as news_file:
        lines = [line for line in news_file if line.strip()]
    return len(lines)

# Task 1 Create csv with word-count
# program to calculate words' count
def create_csv_words_count(text, file_path):
    # all words are preprocessed in lowercase
    words = text.lower().split()
    # count words
    word_count = Counter(words)
    # write words' count to csv file
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for word, count in word_count.items():
            writer.writerow([word, count])

# Task 2 Create csv with letter-count
# program to calculate letters' count
def create_csv_letters_count(text, file_path):
    # find letters only
    letters = [ch for ch in text if ch.isalpha()]
    # find upper case letters only
    upper_case_letters = [ch for ch in text if ch.isupper()]
    # calculate common values:
    all_letters_count = len(letters)
    upper_case_letters_count = len(upper_case_letters)
    lower_case_letters_count = all_letters_count - upper_case_letters_count
    # calculate letters' count
    letters_count = Counter(letters)
    # write words' count to csv file
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        # add header
        headers = ['letter', 'count', 'common_count', 'percentage']
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        for letter, count in letters_count.items():
            if letter.isupper():
                # if letter in Uppercase, use uppercase letters' count for percentage calculation
                writer.writerow({'letter': letter,
                                 'count': count,
                                 'common_count': upper_case_letters_count,
                                 'percentage': round(count/upper_case_letters_count * 100, 2)})
            else:
                # else use lowercase letters' count for percentage calculation
                writer.writerow({'letter': letter,
                                        'count': count,
                                        'common_count': lower_case_letters_count,
                                        'percentage': round(count/lower_case_letters_count * 100, 2)})
# delete csv files
def delete_csv_files(*csv_paths):
    for csv_path in csv_paths:
        if os.path.exists(csv_path):
            os.remove(csv_path)

def main():
    news_file_path = 'generated_news.txt'
    rows_file_path = 'news_row_count.txt'
    words_file_path = 'csv_1_words_count.csv'
    letters_file_path = 'csv_2_letters_count.csv'

    # calculate row number:
    current_row_count = count_rows_in_file(news_file_path)

    # check if row number changed
    if os.path.exists(rows_file_path):
        with open(rows_file_path, 'r') as f:
            previous_row_count = int(f.read())
    else:
        previous_row_count = 0

    if current_row_count != previous_row_count:
        print("Row count changed. CSVs should be recreated.")
        # delete existing csv
        delete_csv_files(words_file_path, letters_file_path)
        # read text from news file:
        text = read_news_file(news_file_path)
        # create new csv
        create_csv_words_count(text, words_file_path)
        create_csv_letters_count(text, letters_file_path)
        # update row count
        with open (rows_file_path, 'w') as f:
            f.write(str(current_row_count))

if __name__ == '__main__':
    main()

