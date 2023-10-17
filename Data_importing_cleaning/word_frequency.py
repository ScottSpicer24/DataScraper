'''
scrapes the page for all the words removing common words like then, and, went, ect... (stop words)
counts them, makes a data table (relational to the NHLteams table based on wikiLink), and stores it in the table
'''
# imports for connecting to MySQL & beautifulsoup4 
import mysql.connector
from bs4 import BeautifulSoup
import requests
import re
import pprint

def main():
    # connect to database
    db = mysql.connector.connect(host = "localhost", user= "root", passwd="Spicer99", database="scottnhl")
    # create coursor
    cursor = db.cursor()
    # get wiki link (start with a single one while testing)
    cursor.execute('SELECT wikiLink, teamName FROM NHLteams;')
    wiki_links = cursor.fetchall()

    for team_data in wiki_links:
        break
        # connect to beautifulsoup to scrape data, LXML as the parser
        html_text = requests.get(team_data[0]).text
        soup = BeautifulSoup(html_text, 'lxml')
        # get all of the main text without the tags and all lowercase
        page_text = soup.find('div', id='mw-content-text')
        main_text = page_text.find('div', class_ = 'mw-parser-output').get_text(separator=' ')
        # remove puncuation
        main_text = re.sub(r'[^\w\s]','', main_text) 
        # split by whtespace to seperate into words
        main_text = main_text.split()
        
        # load in stop words
        path = "C:/Users/Owner/OneDrive/Documents/DataWebsite/terrier-stop.txt"
        with open(path) as f:
            stop_words = set(f.read().splitlines())  # splitlines will remove the '\n' in the end and return a list of words
        f.close()

        # create MySQL table to hold the words and their count
        teamName = team_data[1].lower().replace(' ', "_")
        sql_table_create = f'CREATE TABLE {teamName}WikiWords (word_id INT AUTO_INCREMENT PRIMARY KEY, wikiLink VARCHAR(255), word VARCHAR(100), count INT, FOREIGN KEY (wikiLink) REFERENCES NHLteams(wikiLink));'
        words_table = f'{teamName}WikiWords'
        cursor.execute(sql_table_create)
        #db.commit them
        db.commit()

        # create dictionary to hold words
        dict = {}
        # loop through words
        for word in main_text:
            # O(1) check if the the word is not in the stop_words list
            if word not in stop_words:
                # if in the dict increment by one if not add it and set it to 1
                if word in dict:
                    dict[word] += 1
                else:
                    dict[word] = 1
        # remove words that are seen 1 or 2 times
        for key in list(dict.keys()):
            if(dict[key] < 3):
                del dict[key]
            else:
                val = dict[key]
                sql_word_add = f'INSERT INTO {words_table}(wikiLink, word, count) VALUES("{team_data[0]}", "{key}", {val});'
                cursor.execute(sql_word_add)
                #db.commit them
                db.commit()

        

if __name__ == "__main__":
    main()