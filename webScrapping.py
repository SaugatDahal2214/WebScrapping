import requests
from bs4 import BeautifulSoup
import sqlite3


conn = sqlite3.connect('hospital.db')
c = conn.cursor()


c.execute("CREATE TABLE IF NOT EXISTS Doctors (id INTEGER PRIMARY KEY, Name TEXT, Designation TEXT, Description TEXT)")

url_one = "https://www.hospitaldirghayu.com/doctors?page={}"

def get_all_docs(pageNumber):
    url_two = url_one.format(pageNumber)
    response = requests.get(url_two)

    soup = BeautifulSoup(response.content, 'html.parser')

    docName = soup.find_all('h4', class_='doc-name')
    docDesg = soup.find_all('span', class_ = 'doc-designation')
    docDesc = soup.find_all('p', class_ = 'doc-description')

    doc_names = []
    for name in docName:
        doc_names.append(name.text) 
    
    doc_designation = []
    for desg in docDesg:
        doc_designation.append(desg.text) 
    
    doc_desc = []
    for dec in docDesc:
        doc_desc.append(dec.text) 
    

    return(doc_names, doc_designation, doc_desc)

all_doc_name = []
all_desg = []
all_desc = []

for i in range(1, 6):
    names, designations, descriptions = get_all_docs(i)
    all_doc_name.extend(names)
    all_desg.extend(designations)
    all_desc.extend(descriptions)


for name, desg, desc in zip(all_doc_name, all_desg, all_desc):
    c.execute("INSERT INTO Doctors (Name, Designation, Description) VALUES (?, ?, ?)", (name, desg, desc))
    print(f'Name: {name}, \n Designation: {desg}, \n Description: {desc} \n')
    print(' ')


conn.commit()
conn.close()

print("Operation successful")

