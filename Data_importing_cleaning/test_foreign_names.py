'''
Script to check if names like Šťastný will have the same count as Stastny. 
'''

import mysql.connector
# connect to database
db = mysql.connector.connect(host = "localhost", user= "root", passwd="Spicer99", database="scottnhl")
# create db cursor
cursor = db.cursor()
# pullout all the team names
cursor.execute('SELECT count FROM Avalanchewikiwords WHERE word = "Šťastný";')
count = cursor.fetchall()
# should be 17, for Stastny it is 17
print(count)