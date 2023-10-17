
'''
gets the team name and location from the database. 
makes that into a wikipedia link and adds that wiki link to the database.
now those wiki links can be used to scrape data from. 
'''

import mysql.connector

db = mysql.connector.connect(host = "localhost", user= "root", passwd="Spicer99", database="scottnhl")

cursor = db.cursor()

# get team location and name from database
cursor.execute('SELECT location, teamName FROM NHLteams;')
team_data = cursor.fetchall()

# loop through database length
for team in team_data:
    # store the name and city of teams in variable and strip them
    city_with_spaces = team[0].strip()
    name_with_spaces = team[1].strip()
    # change spaces with _
    city = city_with_spaces.replace(" ", "_")
    name = name_with_spaces.replace(" ", "_")
    # combine with location seperate with an _
    whole_name = city + "_" + name
    # add that to the end of https://en.wikipedia.org/wiki/
    wikiLink = "https://en.wikipedia.org/wiki/" + whole_name
    # add to the db under the wikiLink col 
    sql_line = f'UPDATE NHLteams SET wikiLink = "{wikiLink}" WHERE teamName = "{name_with_spaces}";'
    cursor.execute(sql_line)
    #db.commit them
    db.commit()

cursor.close()
db.close()
