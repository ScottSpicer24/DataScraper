'''
CSV files from "Hockey-Reference.com" each contains all players from each team sorted by games played for each team.
creates a MySQL table refrenced to the NHLteams table based on the UNIQUE column of the team name.
table includes the player's: name, start year, end year, games played, goals, assist, points, +/-, penalty minutes
'''
# imports for connecting to MySQL & beautifulsoup4 
import mysql.connector
import csv
import re

def main():
    # connect to database
    db = mysql.connector.connect(host = "localhost", user= "root", passwd="Spicer99", database="scottnhl")
    # create db cursor
    cursor = db.cursor()
    
    # pullout all the team names
    cursor.execute('SELECT teamName FROM NHLteams;')
    teams = cursor.fetchall()

    #for each team
    for team in teams:
        break
        # replace space with _ to get the correct files 
        team = team[0].replace(" ", "_")
        '''print(team)'''
        
        # create the player table in the database based on the team name (same name as the file without the .csv)
        sql_player_table = f'CREATE TABLE {team}_player_data(teams_player_id INT AUTO_INCREMENT PRIMARY KEY, teamName VARCHAR(30), firstName VARCHAR(100), lastName VARCHAR(100), startYear INT, endYear INT, gamesPlayed INT, goals INT, assist INT, points INT, plusMinus INT, penaltyMinutes INT, FOREIGN KEY (teamName) REFERENCES NHLteams(teamName));'
        '''print(sql_player_table)'''
        #execute and commit sql statement
        cursor.execute(sql_player_table)
        db.commit()
        
        # get and open the CSV file 
        path = f"C:/Users/Owner/OneDrive/Documents/DataWebsite/csv_data/{team}_player_data.csv"
        '''print(path)'''
        
        # open file 
        with open(path, encoding="utf8") as f:
            #create reader to read through csv file
            reader = csv.reader(f)
            
            # read through the csv file line by line skipping the header
            for i in range(6):
                next(reader)
            i = 0
            for row in reader:
                # seperate first and last name
                try:
                    player_name = row[1]
                except IndexError:
                    break
                firstName, lastName = player_name.split(' ', 1) 
                # remove * from last name for HOF players NOTE: DECIDED TO KEEP * IN NAME
                # lastName = re.sub(r'[\*]','', lastName)
                # lastName = lastName.strip()
                '''print(lastName)'''
                # NOTE: In Hockey ref (and in db soon) it is Šťastný (BC it is UTF8 not ASCII), in wiki tables it is Stastny but still works! tested in test_foreign_names.py (not just for this one but others like it too)
                '''lastName = lastName.replace(' ', '_')'''
                startYear = row[2]
                if(startYear == ''):
                    startYear = "NULL"
                endYear = row[3]
                if(endYear == ''):
                    endYear = "NULL"
                gamesPlayed = row[5] # skip 4 because it is years played for team
                if(gamesPlayed == ''):
                    gamesPlayed = "NULL"
                goals = row[6]
                if(goals == ''):
                    goals = "NULL"
                assist = row[7]
                if(assist == ''):
                    assist = "NULL"
                points = row[8]
                if(points == ''):
                    points = "NULL"
                plusMinus = row[9]
                if(plusMinus == ''):
                    plusMinus = "NULL"
                penaltyMinutes = row[10]
                if(penaltyMinutes == ''):
                    penaltyMinutes = "NULL"
                # NOTE take out _ in name with spaces for team name col
                team_name_space = team.replace('_', " ")
                '''
                print(firstName, lastName, startYear, endYear, gamesPlayed, goals, assist, points, plusMinus, penaltyMinutes)
                print("---------------")
                '''
                sql_player_add = f'INSERT INTO {team}_player_data( teamName, firstName, lastName, startYear, endYear, gamesPlayed, goals, assist, points, plusMinus, penaltyMinutes) VALUES("{team_name_space}", "{firstName}", "{lastName}", {startYear}, {endYear}, {gamesPlayed}, {goals}, {assist}, {points}, {plusMinus}, {penaltyMinutes});'
                '''print(sql_player_add)
                print("---------------")'''
                #execute and commit sql statement
                cursor.execute(sql_player_add)
                db.commit()
        f.close()

if __name__ == "__main__":
    main()