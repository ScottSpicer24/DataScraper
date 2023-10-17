'''
Adds the number of stanley cups and the year formed
NOTE: Because the Vancouver Canucks have 2 dates (1 for when formed and 1 for when they joined)...
they have an if statement for their special case
'''


# imports for connecting to MySQL & beautifulsoup4 
import mysql.connector
from bs4 import BeautifulSoup
import requests
import re

def main():
    # connect to database
    db = mysql.connector.connect(host = "localhost", user= "root", passwd="Spicer99", database="scottnhl")
    # create coursor
    cursor = db.cursor()

    # get team wikipedia link and name from database
    cursor.execute('SELECT wikiLink, teamName FROM NHLteams;')
    wiki_links = cursor.fetchall()

    # for all the teams 
    for link in wiki_links:
        # connect to beautifulsoup to scrape data, LXML as the parser
        html_text = requests.get(link[0].strip()).text
        soup = BeautifulSoup(html_text, 'lxml')

        # get just the main text on the page
        page_text = soup.find('div', id='mw-content-text')
        main_text = page_text.find('div', class_ = 'mw-parser-output')

        # get the infobox with stanley cup wins in it then get the body of that table to get acess to the rows
        infobox = page_text.find('table', class_ = 'infobox').find('tbody')
        # get all the rows and loop through them
        infobox_rows = infobox.find_all('tr')

        for row in infobox_rows:
            # when you find the stanley cups row
            if(re.match(r"Stanley Cups", row.text)):
                # the number of cups theve won is in the b tag
                num_cups = row.find('b').text.strip()
                # create the SQL command using a f-string so we can include python variabes
                sql_line = f'UPDATE NHLteams SET cupsWon = "{num_cups}" WHERE teamName = "{link[1].strip()}";'
                cursor.execute(sql_line)
                #db.commit them
                db.commit()

            # if you get to the row with the year the team was founded
            if(re.match(r"Founded", row.text)):
                # store the year in a variable
                yearFormed = row.find('td', class_ = 'infobox-data').text.strip()
                # exception for vancover 
                if(link[1].strip() == 'Canucks'):
                    yearFormed = 1945
                # create the SQL command using a f-string so we can include python variabes
                sql_line = f'UPDATE NHLteams SET yearFormed = "{yearFormed}" WHERE teamName = "{link[1].strip()}";'
                cursor.execute(sql_line)
                #db.commit them
                db.commit()

if __name__ == "__main__":
    main()