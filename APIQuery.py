import csv
import requests
import os
import shutil
import json

# Get the subarea input from the user
#subarea = input("Enter in a Subarea:")

# Set the query parameter
query = "(status like '%DONE%' and (woclass = 'WORKORDER' or woclass = 'ACTIVITY') and historyflag = 0 and istask = 0 and siteid = 'UTILITY' and worktype like '%CM%')"

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
    'location': '~sw~%s' % query,
    'PLUSSFEATURECLASS': 'GISSEWERGRAVITYMAIN',
    'orderby': 'location',
    'status': 'operating,planned'
}

# Make the API call and get the JSON response
response = requests.get(url, headers=headers, params=params, verify = False)

# Check the status code of the response to make sure it was successful
if response.status_code == 200:

    # Extract the data from the response
    data = response.json()

    # Parse the data into a list of tuple
    # The ["Attributes"]["LOCATION"]["content"] is the first section that is recognized to hold values.
    # The ["Attributes"]["DESCRIPTION"]["content"] is the second section that is recognized to hold values. 
    # Location and Description are the same thing just under two different names. So it must be specified that you're searching for both so no data is lost.
    # The ['LOCATIONSMboSet']["LOCATIONS"] is the specified location where we are pulling the data from. It's split up into different sections number 0-infinity;
    # You can add different values to look for a specified section, but to have all the sections don't specify a number.
    ourdata = ((item["Attributes"]["LOCATION"]["content"], item["Attributes"]["DESCRIPTION"]["content"]) for item in data['LOCATIONSMboSet']["LOCATIONS"])
    
    # Convert the generator object 'ourdata' to a list object
    ourdata_list = list(ourdata)

    # Calculate the number of matching records using the ourdata_list variable
    num_records_ourdata = len(ourdata_list)

    # Print the number of matching records
    print("Number of matching records using ourdata_list:", num_records_ourdata)
else:
    # Incase the API fails it lets the user know what is going on within the code above.
    # This changes the value of ourdata to hold an empty list.
    print("API request failed with status code:", response.status_code)
    ourdata = []
