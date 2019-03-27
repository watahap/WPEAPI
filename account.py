#!/usr/bin/env python

import re
import requests
import json

from pprint import pprint

# Setting Credentials, defining API auth string.

try:
    input = raw_input
except NameError:
    pass
user = 'f1dd77ca-e62b-42d3-b7e8-5c8e1c7f57b7'
password = 'yoFYe9LYxRpAlgVmGXKP5A=='
#user = input("What is your API Username?: ")
#password = input("What is your API Pasword?: ")

creds = ("{u}:{p}".format(u=user, p=password))
account_url = "https://api.wpengineapi.com/v0/accounts?limit=100&offset=0"
sites_url = "https://api.wpengineapi.com/v1/sites"
installs_url = "https://api.wpengineapi.com/v1/installs"

# sites_data = requests.get(sites_url, auth=(user, password)).json()
# data_results = sites_data["results"]
# pprint(data_results)

payload =  {'accept': 'application/json',
            'Content-Type': 'application/json',
            'name': 'littkebdrprd',
            'account_id': '0a7ff389-96c8-404b-922d-73fd855766f8',
            'site_id': '2779b60a-a615-4346-a969-7378a0f5ab16',
            'environment': 'production'
            }

payload_json = json.dumps(payload)
test_response = requests.post(installs_url, auth = (user, password), data=payload_json)
pprint(test_response.json()["errors"][0]["message"][5::])
# if test_response.status_code == 400:
#     #print(type(test_response.json()))
#     print(test_response.json()["errors"][0]["message"])


# pprint(test_response)
# pprint(test_response.json())


# for i in data_results:
#     install_id = i['id']
#     pprint(install_id)



    # for d in data_results:
    #     pprint((d.items()[2])[1])
    # for d in data_results:
    #     for k, v in d.items():
    #         pprint(d.items()[0])
    # this will give you the "installs" list

    # domain_list = []
# account_r = requests.get(sites_url, auth=(user, password))
# results = account_r.json()

# install_name = results["results"][0]["installs"][0]["name"]
# install_environment = results["results"][0]["installs"][0]["environment"]
# install_id = results["results"][0]["installs"][0]["id"]
# site_id = results ["results"][0]["id"]
# site_name = results["results"][0]["name"]



# pprint(results)
#
# account_id_string = results["results"][0]["id"]
#
# #pprint(account_id_string)
# #Reading domains file as list, then formatting special characters out of that list to accommodate install creation.
#
# with open('domains.txt', 'r') as f:
#
# 	domains = f.readlines()
#
# for line in domains:
#      line = re.sub('\n','', line)
#      stripped_line = re.sub('(https?:\/\/)?(www\.)?', '', line)
#      if line:
#          domain_list.append(stripped_line)
#
#
#
#
# # Making POST requests to the WPE API to build site environments nammed after the domains.  ALL THIS WORKS
#
# #data = {'accept': 'application/json',
# #        'Content-Type': 'application/json',
# #        'name': '',
# #        'account_id': account_id_string
# #    }
#
# #for line in domain_list:
# #    data["name"] = line
# #    data_json = json.dumps(data)
# #    r = requests.post(sites_url, auth=(user, password), data = data_json)
