'''
Script that was used to practice scraping data from a wikipedia page
'''

from bs4 import BeautifulSoup
import requests
import re


'''
Scrapes all the text from a given wikipedia page
'''
def main():
    # using requests lib get the html from the link, 
    # '.text' to get the text of the html code as opposed to the response code 'Response [200]'
    link = "https://en.wikipedia.org/wiki/Tampa_Bay_Lightning"
    html_text = requests.get(link).text 

    # create a beautiful soup instance 
    # lxml as the parser
    soup = BeautifulSoup(html_text, 'lxml')

    # get all the text in the page
    page_text = soup.find('div', class_='mw-parser-output') 

    # get all the main section headings and their sub-headings
    sections = page_text.find_all(['h2', 'h3', 'h4'])

    # for each one grab just the text portion of the heading and print them out
    for heading in sections:
        if(heading.name == 'h2'):
            main_section = heading.text
            print("")
            print(main_section)
        if(heading.name == 'h3'):
            sub_section = heading.text
            print(f"-{sub_section}")
        if(heading.name == 'h4'):
            micro_section = heading.text
            print(f"->{micro_section}")
        # could also do: section = heading.find("span", class_ = "mw-headline") instead of heading.text

    # ask for what player they want to search for (not including refrences or headings)
    print("What player do you want to search for")
    player = input("last name: ").lower()

    # get the text on the page from paragraphs, picture captions, and list
    # note 'div' tag is a table of multiple tables, class_ = wikitable gets them only once 
    html_text = page_text.find_all(['p', 'figcaption', 'ul']) # paragraphs, pictures, list
    
    # get the text from table
    # some tables are tables in tables (specifically ones in 'div' tags) 
    # and if you put it in the html_text you cant do the class section of the find_all
    table_text = page_text.find_all('table', {'class':['wikitable', 'infobox']})
    
    # counter var to hold number times something is on page
    counter = 0

    # go through each tag that has text and get that text
    for paragraph in html_text:
        if(paragraph.name == 'p'):
            text = paragraph.text.strip().lower()
            counter += count_string(text, player)
        elif(paragraph.name == 'figcaption'):
            text = paragraph.text.strip().lower()
            counter += count_string(text, player)   
        elif(paragraph.name == 'ul'):
            text = paragraph.text.strip().lower()
            counter += count_string(text, player)
    for table in table_text:
        text = table.text.strip().lower()
        counter += count_string(text, player)

    print(f"{player} is listed {counter} times.")

def count_string(text, string):
    leng = len(re.findall(rf'{string}', text))
    '''if(leng != 0):
        print(text)
        print(re.findall(rf'{string}', text))
        print("")'''
    return leng





if __name__ == "__main__":
    main()