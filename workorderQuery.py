import requests
import json
import csv
import os
import shutil
from pprint import pprint

#work order to test it 15706973
workordernum = input("Enter a workorder:")

# connects to maximo server to make api calls
api_url = "http://ocudrhmxdvap01/maxrest/rest/os/mxwo?"

# Build query URL
query_url = f"{api_url}wonum={workordernum}"
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
    'workorder': '~sw~%s' % workordernum
}

# Make API request
try:
    response = requests.get(query_url, headers=headers, params=params, verify=False)
    #print(response.json)
except requests.exceptions.RequestException as e:
    # An error occurred while making the request
        print(f"An error occurred while making the request: {e}")
        ourdata = []
else:
    # Check the status code of the response
    if response.status_code != 200:
        # The request failed
        print(f"The request failed with status code {response.status_code}")
        ourdata = []
    else:
        # Parse response
        try:
            data = response.json()
            #pprint(data)
            ourdata = ((item["Attributes"]["workorder"]["content"], item["Attributes"]["DESCRIPTION"]["content"]) for item in data['QueryMXWOResponse']["MXWOSet"]["WORKORDER"])
            print(ourdata)
        except json.decoder.JSONDecodeError as e:
            # An error occurred while parsing the response
            print(f"An error occurred while parsing the response: {e}")
            ourdata = []


# Set the header row for the CSV file
csvheader = ['Attributes', 'WORKORDER', 'content']

# Define the path for the CSV file
path = 'C:/Users/136048/Desktop/dev/%s_workorder.csv' % workordernum


# Define the destination for the copied file
# Path can be changed to a different destination just incase dev folder is corrupted.
copy_name = 'C:/Users/136048/Desktop/dev/%s_workorder.csv' % workordernum

# Check if the path exists
if os.path.exists(path):
    # Copy the CSV file to a new location
    shutil.copy(path, copy_name)
else:
    print("The file does not exist at the specified path.")

# Open a CSV file for writing
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

print(f"Successfully wrote {len(ourdata)} work orders to 'workorders.csv'.")

