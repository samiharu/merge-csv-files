import csv
from urllib.parse import urlparse

#Titles and path for input files
generalFile = "files/all-contacts.csv"
emailsFile = "files/emails.csv"

#Titles and path for output files
resultFileEmails = "files/result.csv"
resultFileLinkedin = "files/neresult.csv"

#Function to normalize first names and last names
def namesUtility(name):
    return name.lower().replace('.','').replace(',','').strip()

#Function to normalize urls of companies websites
def urlUtility(urlOriginal):
    if not urlOriginal.lower().startswith("http"):
        urlOriginal = "https://" + urlOriginal
    urlFinal = urlparse(urlOriginal).netloc
    urlFinal = urlFinal.strip("www.")
    urlFinal = urlFinal.strip().lower()

    return urlFinal

#Function to read from CSV files
def fileReadUtility(fileName, titles, dataArray):
    with open(fileName, 'r') as csvfile:
        csvReader = csv.reader(csvfile)

        titles.extend(next(csvReader))

        for row in csvReader:
            dataArray.append(row)

#Determine data storage varibles for all contacts data
titlesGeneral = []
rowsGeneral = []

#Determine data storage varibles for emails data
titlesEmails = []
rowsEmails = []

#Read from csv files
fileReadUtility(generalFile, titlesGeneral, rowsGeneral)
fileReadUtility(emailsFile, titlesEmails, rowsEmails)

print(titlesGeneral)
print(titlesEmails)

#Compare each line with each in two files. If first name, last name and company website url match field with email from second file will be append to general dataset
for currentRowGeneral in rowsGeneral:
    emailFound = False
    for currentRowEmail in rowsEmails:
        if namesUtility(currentRowGeneral[0]) == namesUtility(currentRowEmail[2]) and namesUtility(currentRowGeneral[1]) == namesUtility(currentRowEmail[3]) and urlUtility(currentRowGeneral[4]) == urlUtility(currentRowEmail[4]):
            currentRowGeneral.append(currentRowEmail[0])
            emailFound = True
    if emailFound == False:
        currentRowGeneral.append('')

#Write general dataset to new files depend on email existing
with open(resultFileEmails, 'w') as csvEmailsResults:
    with open(resultFileLinkedin, 'w') as csvLinkedInResults:
        csvWriterEmails = csv.writer(csvEmailsResults)
        csvWriterLinkedIn = csv.writer(csvLinkedInResults)

        csvWriterEmails.writerow(titlesGeneral)
        csvWriterLinkedIn.writerow(titlesGeneral)

        for rows in rowsGeneral:
            if rows[7] != '':
                csvWriterEmails.writerow(rows)
            else:
                csvWriterLinkedIn.writerow(rows)

print("Done+")