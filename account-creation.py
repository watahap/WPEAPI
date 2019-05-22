#!/usr/bin/env python

import re
import requests
import json
import time
from string import digits
from pprint import pprint
from typing import Any


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

        with open('domains.txt', 'r') as f:

            domains = f.read().splitlines()

        filtered_domains = []

        for line in domains:
            domain = re.sub('(https?://)?(www.)?', '', line)
            if domain[0].isdigit() == True:
                domain = domain.lstrip(digits)
            if len(domain) >= 40:
                domain = '{}.{}'.format(domain[0:30:1], 'com')
            clean_domain = re.sub('\t|\s|\r','', domain)
            filtered_domains.append(clean_domain)

        return filtered_domains

    def get_account_data(self):
        account_r = requests.get(self.account_api, auth=(self.user, self.password))
        return account_r.json()

    def create_site_experience(self, filtered_domains):
        account_id_string = self.get_account_data()["results"][0]["id"]
        data = {'accept': 'application/json',
                'Content-Type': 'application/json',
                'name': '',
                'account_id': account_id_string
                }

        for line in filtered_domains:
            data["name"] = line
            data_json = json.dumps(data)

            print('Creating site experience for', line)
            sites_results = requests.post(self.sites_api, auth=(self.user, self.password), data=data_json)
            if sites_results.status_code == 400:
                error_message = '{}, {}'.format(line, sites_results.json()["errors"][0]["message"])
                print(error_message)
            else:
                print(line, 'created!')

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
            clean_name = re.sub('\.|\-|\/', '', site_name)
            new_name = '{}{}'.format(clean_name[0:11:1], 'prd')
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
            time.sleep(150)
            if installs_results.status_code == 201:
                print(new_name, 'created successfully')
            if installs_results.status_code == 400:
                error_message = '{}, {}'.format(new_name, installs_results.json()["errors"][0]["message"][5::])
                print(error_message)
                print('Trying with shorter install name...')
                newer_name = '{}{}'.format(clean_name[0:10:1], 'prd')
                new_data = {'accept': 'application/json',
                            'Content-Type': 'application/json',
                            'name': newer_name,
                            'account_id': account_id_string,
                            'site_id': site_id,
                            'environment': 'production'
                            }
                new_data_json = json.dumps(new_data)
                retry_results = requests.post(self.installs_api, auth=(self.user, self.password), data=new_data_json)
                time.sleep(150)
                if retry_results.status_code == 201:
                    print(newer_name, 'created successfully')
                if retry_results.status_code == 400:
                    new_error_message = '{}, {}'.format(newer_name, retry_results.json()["errors"][0]["message"][5::])
                    print(new_error_message)
                    print('Trying with even shorter install name...')
                    last_name = '{}{}'.format(clean_name[0:9:1], 'prd')
                    last_data = {'accept': 'application/json',
                                 'Content-Type': 'application/json',
                                 'name': last_name,
                                 'account_id': account_id_string,
                                 'site_id': site_id,
                                 'environment': 'production'
                                }
                    last_data_json = json.dumps(last_data)
                    last_results = requests.post(self.installs_api, auth=(self.user, self.password), data=last_data_json)
                    time.sleep(150)
                    if last_results.status_code == 201:
                        print(last_name, 'created successfully')
                    if last_results.status_code == 400:
                        print('Please revisit this install')


    def get_installs_data(self):
        if self.install_results is None:
            self.install_results = requests.get(self.installs_api, auth=(self.user, self.password))

        return self.install_results.json()

    def configure_domains(self):
        domain_data_results = requests.get(self.sites_api, auth=(self.user, self.password))
        install_data_results = domain_data_results.json()
        for d in install_data_results["results"]:
            install_id = d["installs"][0]["id"]
            domain_name = d["name"]
            data = {'name': domain_name,
                    'duplicate': False,
                    'primary': True,
                    }
            data_json = json.dumps(data)
            installs_url = '{}/{}/{}'.format(self.installs_api, install_id, 'domains')
            print('Adding domain for', domain_name)
            domain_results = requests.post(installs_url, auth=(self.user, self.password), data=data_json)
            time.sleep(150)
            if domain_results.status_code == 400:
                print(domain_results.json())
            if domain_results.status_code == 201:
                print(domain_name, 'configured successfully')
                www_domain = '{}.{}'.format('www',domain_name)
                www_data = {'name': www_domain,
                            'duplicate': False,
                            'primary': True,
                            }
                www_json = json.dumps(www_data)
                print('Adding domain for', www_domain)
                www_domain_results = requests.post(installs_url, auth=(self.user, self.password), data=www_json)
                time.sleep(150)
                if www_domain_results.status_code == 400:
                    print(www_domain_results.json())
                if www_domain_results.status_code == 201:
                    print(www_domain, 'configured successfully')

if __name__ == '__main__':
    wpe = WpeAccount()
    wpe.get_creds()
    filtered_domains = wpe.get_cleaned_domains()
    account_id_string = wpe.get_account_data()
    wpe.create_site_experience(filtered_domains)
    wpe.create_installs()
    wpe.configure_domains()
