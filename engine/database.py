import csv
import sqlite3

#the main file that was used to handle and manage the database for the working of the virtual assistant,

#connect database

dataobj = sqlite3.connect("nova.db")
cursor = dataobj.cursor()






#these commands are used to maintain and manage the table sys_command for opening of softwares installed on pc

#sys_command
query = "CREATE TABLE IF NOT EXISTS sys_command(id integer primary key, name VARCHAR(100),path VARCHAR(1000))"
cursor.execute(query)

#inserting into sys_command
query = "INSERT INTO sys_command VALUES (null,'alan wake 2', 'D:\\Games\\Alan Wake 2\\AlanWake2.exe')"
cursor.execute(query)
dataobj.commit()

#for deleting accidental insertions in sys_command
""" query = "DELETE FROM sys_command WHERE id = 2"
cursor.execute(query)
dataobj.commit() """









#these commands are used to maintain and manage the table sys_command for opening of websites

#web_command
query = "CREATE TABLE IF NOT EXISTS web_command(id integer primary key, name VARCHAR(100), path VARCHAR(1000))"
cursor.execute(query)

#inserting into web_command
""" query = "INSERT INTO web_command VALUES (null,'pornhub', 'https://www.pornhub.com/')"
cursor.execute(query)
dataobj.commit()
 """
#deleting accidental insertions in web_command
'''query = "DELETE FROM web_command WHERE id = 5"
cursor.execute(query)
dataobj.commit()'''







#used for maintaining contacts and whatsapp automation

#Contacts
cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (id integer primary key, name VARCHAR(200), mobile_no VARCHAR(255), email VARCHAR(255) NULL)''')


#used to read and import info from a csv file exported from google contacts to add contact info swiftly to the database
#reading contacts from csv file
""" desired_columns_indices = [0, 20]

# Read data from CSV and insert into SQLite table for the desired columns
with open('contacts.csv', 'r', encoding='utf-8') as csvfile:
    read = csv.reader(csvfile)
    for row in read:
        selected_data = [row[i] for i in desired_columns_indices]
        cursor.execute(''' INSERT INTO contacts (id, 'name', 'mobile_no') VALUES (null, ?, ?);''', tuple(selected_data))

# Commit changes and close connection
dataobj.commit()
dataobj.close() """

#inserting single contacts

""" query = "INSERT INTO contacts VALUES (null,'contact_name', 'Mobile_No', 'null')"
cursor.execute(query)
dataobj.commit() """


#searching contact from database
""" query = 'Sumit'
query = query.strip().lower()

cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
results = cursor.fetchall()
print(results[0][0]) """

#delete accidental data from contacts table
""" query = "DELETE FROM contacts WHERE id = 2"
cursor.execute(query)
dataobj.commit() """


#work in progress, used for discord automation

#discord automation

cursor.execute("CREATE TABLE IF NOT EXISTS discordUrls (id integer primary key, name VARCHAR(100), url VARCHAR(1000))")


#delete from discord table
""" cursor.execute("DELETE FROM discordUrls WHERE id = 1")
dataobj.commit() """

#insert into discord table
""" query = "INSERT INTO discordUrls VALUES (null,'valo vc','1254047945918119950')"
cursor.execute(query)
dataobj.commit() """

