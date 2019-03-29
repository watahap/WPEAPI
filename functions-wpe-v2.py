#!/usr/bin/env python

import re
import requests
import json
import time

from pprint import pprint


class WpeAccount:
    def __init__(self):
        self.user = None
        self.password = None
        self.account_api = "https://api.wpengineapi.com/v0/accounts?limit=100&offset=0"
        self.sites_api = "https://api.wpengineapi.com/v1/sites"
        self.installs_api = "https://api.wpengineapi.com/v1/installs"
        self.sites_results = None
        self.install_results = None

    def get_creds(self):
        if self.user is None or self.password is None:

            try:
                input = raw_input
            except NameError:
                pass

            self.user = input("What is your API Username?: ")
            self.password = input("What is your API Pasword?: ")

        return self.user, self.password

    def get_cleaned_domains(self):
        domain_list = []

        with open('domains.txt', 'r') as f:

            domains = f.read().splitlines()

        for line in domains:
            stripped_line = re.sub('(https?://)?(www.)?', '', line)
            # Checking for blank lines
            if line:
                domain_list.append(stripped_line)

        return domain_list
        # Put Error checking here for duplicate domain names, or domains that are larger than 40 characters, or ones that start with numeric characters.

    def get_account_data(self):
        account_r = requests.get(self.account_api, auth=(self.user, self.password))
        return account_r.json()

    def create_site_experience(self, domain_list):
        account_id_string = self.get_account_data()["results"][0]["id"]
        data = {'accept': 'application/json',
                'Content-Type': 'application/json',
                'name': '',
                'account_id': account_id_string
                }

        for line in domain_list:
            data["name"] = line
            data_json = json.dumps(data)

            print('Creating site experience for', line)
            sites_results = requests.post(self.sites_api, auth=(self.user, self.password), data=data_json)
            if sites_results.status_code == 400:
                error_message = '{}, {}'.format(line, sites_result.json()["errors"][0]["message"])
                print(error_message)
            else:
                #print(sites_results.json())
                print(line, 'created!')

            #time.sleep(150)

    def get_sites_data(self):
        if self.sites_results is None:
            self.sites_results = requests.get(self.sites_api, auth=(self.user, self.password))

        return self.sites_results.json()

    def create_installs(self):
        data_results = self.get_sites_data()["results"]
        for d in data_results:
            account_id_string = self.get_account_data()["results"][0]["id"]
            site_id = d['id']
            site_name = d['name']
            new_name = '{}{}'.format(site_name[0:12:1], 'prd')
            data = {'accept': 'application/json',
                    'Content-Type': 'application/json',
                    'name': new_name,
                    'account_id': account_id_string,
                    'site_id': site_id,
                    'environment': 'production'
                    }
            data_json = json.dumps(data)


            print('Creating install for', new_name)
            installs_results = requests.post(self.installs_api, auth=(self.user, self.password), data=data_json)
            if installs_results.status_code == 400:
                error_message = '{}, {}'.format(new_name, installs_results.json()["errors"][0]["message"][5::])
                print(error_message)


                print('Trying with shorter install name...')
                newer_name = '{}{}'.format(site_name[0:11:1], 'prd')
                new_data = {'accept': 'application/json',
                            'Content-Type': 'application/json',
                            'name': newer_name,
                            'account_id': account_id_string,
                            'site_id': site_id,
                            'environment': 'production'
                            }
                new_data_json = json.dumps(new_data)
                retry_results = requests.post(self.installs_api, auth=(self.user, self.password), data=new_data_json)
                if retry_results.status.code == 400:
                    new_error_message = '{}, {}'.format(newer_name, retry_results.json()["errors"][0]["message"][5::])
                    print(new_error_message)


                    print('Trying with even shorter install name...')
                    last_name = '{}{}'.format(site_name[0:10:1], 'prd')
                    last_data = {'accept': 'application/json',
                                 'Content-Type': 'application/json',
                                 'name': last_name,
                                 'account_id': account_id_string,
                                 'site_id': site_id,
                                 'environment': 'production'
                                }
                    last_data_json = json.dumps(last_data)
                    last_results = requests.post(self.installs_api, auth=(self.user, self.password), data=last_data_json)
                    if last_results.status.code == 400:
                        print('Please revisit this install')
            else:
                #print(installs_results.json())
                print(new_name, "created!")


            #time.sleep(150)

    def get_installs_data(self):
        if self.install_results is None:
            self.install_results = requests.get(self.installs_api, auth=(self.user, self.password))

        return self.install_results.json()

    def configure_domains(self, domain_list):
        data_results = self.get_installs_data()["results"]
        for d in data_results:
            install_id = d['id']
        for line in domain_list:
            data = {'name': '',
                    'duplicate': 'false',
                    'primary': True,
                    'id': install_id
                    }
            data['name'] = line
            data_json = json.dumps(data)
            installs_url = '{}/{}/{}'.format(self.installs_api, install_id, 'domains')
            requests.post(installs_url, auth=(self.user, self.password), data=data_json)
            time.sleep(150)


if __name__ == '__main__':
    wpe = WpeAccount()
    wpe.get_creds()
    domain_list = wpe.get_cleaned_domains()
    account_id_string = wpe.get_account_data()
    wpe.create_site_experience(domain_list)
    wpe.create_installs()
    #wpe.configure_domains(domain_list)
