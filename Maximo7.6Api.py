import csv
import requests
import os
import shutil
import json
from pprint import pprint
# Get the subarea input from the user
subarea = input("Enter in a Subarea:")

# Set the URL of the Maximo API endpoint.
url = "http://ocudrhmxdvap01/maxrest/rest/mbo/locations/"

# setting the headers for the request to be made.
headers = {
    'Content-Type': "application/json",
    # the authoization is username:password in base64
    # use https://www.base64encode.org/ to format the username and password to base64
    'MAXAUTH': "MTM2MDQ4Om1heGltbw==",
    'cache-control': "no-cache"
}

# Set the query parameters for the API request.
params = {
    '_format': 'json',
    'compact': 1,
    'location': '~sw~%s' % subarea,
    'PLUSSFEATURECLASS': 'GISSEWERGRAVITYMAIN',
    'orderby': 'location',
    'status': 'operating,planned'
}

# Make the API call and get the JSON response
response = requests.get(url, headers=headers, params=params, verify = False)

print(response.json)
# Check the status code of the response to make sure it was successful
if response.status_code == 200:

    # Extract the data from the response
    data = response.json()

    #pprint(data)
    # Parse the data into a list of tuple
    # The ["Attributes"]["LOCATION"]["content"] is the first section that is recognized to hold values.
    # The ["Attributes"]["DESCRIPTION"]["content"] is the second section that is recognized to hold values. 
    # Location and Description are the same thing just under two different names. So it must be specified that you're searching for both so no data is lost.
    # The ['LOCATIONSMboSet']["LOCATIONS"] is the specified location where we are pulling the data from. It's split up into different sections number 0-infinity;
    # You can add different values to look for a specified section, but to have all the sections don't specify a number.
    ourdata = ((item["Attributes"]["LOCATION"]["content"], item["Attributes"]["DESCRIPTION"]["content"]) for item in data['LOCATIONSMboSet']["LOCATIONS"])
    
    # Below is the original ourdata above which experimented with the specified sections. This is a incomplete design of the ourdata above.
    # This line shows what is happening in the background of the API call.
    #ourdata = (data['LOCATIONSMboSet']["LOCATIONS"][0]["Attributes"]['LOCATION']['content'])
else:
    # Incase the API fails it lets the user know what is going on within the code above.
    # This changes the value of ourdata to hold an empty list.
    print("API request failed with status code:", response.status_code)
    ourdata = []

    print(ourdata)


# Set the header row for the CSV file
csvheader = ['Attributes', 'LOCATION', 'content']

# Define the path for the CSV file
path = 'C:\\Users\\136048\Desktop\\dev\\%s_Matching.csv' % subarea

# Define the destination for the copied file
# Path can be changed to a different destination just incase dev folder is corrupted.
copy_name = 'C:\\Users\\136048\Desktop\\dev\\%s_Matching_Copy.csv' % subarea

# Check if the path exists
if os.path.exists(path):
    # Copy the CSV file to a new location
    shutil.copy(path, copy_name)
else:
    print("The file does not exist at the specified path.")

# Open the CSV file for writing and write the data to it
with open(path, 'w', encoding='UTF8', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(csvheader) #writes the csv headers such as ['Attributes', 'LOCATION', 'content']
    writer.writerows(ourdata) # writes the data that is beig extracted from the json file.

# Close the CSV file to make sure file doesn't get corrupted or get extra values inputted.
file.close()

# Copy the CSV file to a new location
copy_name = path
if os.path.exists(path):
    shutil.copy(path, copy_name)


print("done")


