#!/usr/bin/python/
#
# This script will compare the arrival time of data to the ESB between
# the legacy system and the enterprise/new system.
#
import csv, psycopg2, time, collections
from datetime import datetime
from collections import Counter
from collections import OrderedDict 

# Define empty list to store data
date1 = []
date2 = []
wmoHeader1 = [] 
wmoHeader2 = [] 

print "Starting comparison..."
# Open the legacy CSV file 
with open('RG-merge-r2.csv', 'r')as csvfile:
    filereader = csv.reader(csvfile, delimiter=',')
    next(filereader, None) #skip header row
    print "Extracting data from legacy file..."
    for column in filereader:
        # Extract the datetime info as a datetime object to use in timedelta
        legacyDateString = datetime.strptime(column[8], '%m/%d/%Y %H:%M').strftime('%Y-%m-%d %H:%M') #reformat string to use dashes
        legacyDateObject = datetime.strptime(legacyDateString, '%Y-%m-%d %H:%M') #returns datetime object
        date1.append(legacyDateObject)
        # Extract WMO header info
        wmoHeaderLegacy = column[1] # TTAAii CCCC YYGGgg
        wmoHeaderNoSpace = wmoHeaderLegacy.replace(" ", "") #Remove whitespace
        # Remove datetime info (YYGGgg)
        wmoHeaderNoSpaceTrimmed = wmoHeaderNoSpace[0:10] # [0:13] if including day(YY)
        nnn = column[2][0:3]
        newColumn = wmoHeaderNoSpaceTrimmed + nnn #merge TTAAiiCCCC and NNN
        wmoHeader1.append(newColumn)

# Open the database query results file and write to a new file, after merging columns
# containing WMO header information 
with open('Database_Query.csv', 'r')as csvfile:
    filereader2 = csv.reader(csvfile, delimiter=',')
    next(filereader2, None)
    # Open new file to write to
    with open('Database_Query_merged.csv', 'w+') as mergedcsvfile:
        writer = csv.writer(mergedcsvfile)
        for row in filereader2:
            # Merge columns in database results file to form WMO header 
            new_row = ''.join([row[1], row[2]]) #merge ttaaii and cccc
            new_row_nnn = ''.join([new_row, row[3]]) #merge ttaaiicccc and nnn
            awips_row = ''.join([row[3], row[2][1:4]]) #merge nnn and trimmed cccc (to function as xxx)
            writer.writerow((row[0], new_row, new_row_nnn, awips_row, row[3]))

# Define module to parse dates queried from the database, having two formats - with and without milliseconds
# Takes a datetime object as an argument
def parse_dates(datetimeObject):
    for formats in ('%Y-%m-%d %H:%M:%S.%f','%Y-%m-%d %H:%M:%S'):
        try:
            return datetime.strptime(datetimeObject, formats)
        except ValueError:
            pass
    raise ValueError('No valid date format found.') # If format does not match those defined above

# Open merged file for reading to append WMO header info to empty list defined earlier
with open('Database_Query_merged.csv', 'r')as csvfile:
    filereader3 = csv.reader(csvfile, delimiter=',')
    print "Extracting data from database file..."
    for column in filereader3: 
        wmoHeaderOther = column[1]
        wmoHeaderWithNnn = column[2]
        awipsId = column[3]
        wmoHeader2.append(wmoHeaderWithNnn)
        # Extract datetime info
        parsedString = parse_dates(column[0]).replace(microsecond=0)
        timeString = datetime.strftime(parsedString, '%Y-%m-%d %H:%M:%S') # string
        timeObject = datetime.strptime(timeString, '%Y-%m-%d %H:%M:%S') # datetime object
        date2.append(timeObject)

# Zip the WMO header and datetimes into a dictionary
HeaderDates1 = dict(zip(wmoHeader1,date1))
HeaderDates2 = dict(zip(wmoHeader2,date2))

# Define dictionaries after wmo header and date lists
dict1 = HeaderDates1
dict2 = HeaderDates2

# Perform a 1 to 1 comparison. Match the header/awips ids in each 
# dictionary and take the difference between the datetimes
comparison = {x: dict1[x] - dict2[x] for x in dict1 if x in dict2}

# Open new file to write latency results to
print "Saving results..."
file1 = open('Latency.txt', 'w')
# Iterate dictionary
for key,value in comparison.iteritems():
    print >> file1, ('%s: %s' % (key,value)) #format output string: string
file1.close()

# Count products and sort keys alphabetically
legacyProductCount = Counter(wmoHeader1) #Counter (dictionary subclass)
newProductCount = Counter(wmoHeader2)
legacyCountOrdered = OrderedDict(sorted(legacyProductCount.items(), key=lambda t: t[0])) #Ordered Dictionary 
newCountOrdered = OrderedDict(sorted(newProductCount.items(), key=lambda t: t[0]))

print("Legacy product count: " + str(len(wmoHeader1)))
print("Enterprise product count: " + str(len(wmoHeader2)))

# Save ouput to file
file2 = open('Legacy_Products_Count.txt', 'w')
for key, value in legacyCountOrdered.items():
    count = (key, value)
    print >> file2, count
file2.close()

file3 = open('New_Products_Count.txt', 'w')
for key, value in newCountOrdered.items():
    count = (key, value)
    print >> file3, count
file3.close()

# End of script 
