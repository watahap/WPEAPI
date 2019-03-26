#!/usr/bin/env python

import re
import requests
import json

# from pprint import pprint


class WpeAccount:
    def __init__(self):
        self.user = None
        self.password = None
        self.account_api = "https://api.wpengineapi.com/v0/accounts?limit=100&offset=0"
        self.sites_api = "https://api.wpengineapi.com/v1/sites"
        self.installs_api = "https://api.wpengineapi.com/v1/installs"
        self.sites_results = None

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
        # Put Error checking here

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
            requests.post(self.sites_api, auth=(self.user, self.password), data=data_json)

    def get_sites_data(self):
        if self.sites_results is None:
            self.sites_results = requests.get(self.sites_api, auth=(self.user, self.password))

        return self.sites_results.json()

    def create_installs(self, domain_list):
        # account_id_string = self.get_account_data()["results"][0]["id"]
        # site_id = self.get_sites_data()["results"][0]["id"]
        # install_name = self.get_sites_data()["results"][0]["installs"][0]["name"]
        # install_environment = self.get_sites_data()["results"][0]["installs"][0]["environment"]
        # install_id = self.get_sites_data()["results"][0]["installs"][0]["id"]
        # site_name = self.get_sites_data()["results"][0]["name"]
        #
        # data = {'accept': 'application/json',
        #         'Content-Type': 'application/json',
        #         'name': site_name[0:9:1] + 'prd',
        #         'account_id': account_id_string,
        #         'site_id': site_id,
        #         'environment': 'production'
        #         }
        data_results = self.get_sites_data()["results"]
        for index, site_data in data_results.items():
            account_id_string = self.get_account_data()["results"][index]["id"]
            site_id = data_results[index]["id"]
            install_name = self.get_sites_data()["results"][index]["installs"][index]["name"]
            install_environment = self.get_sites_data()["results"][index]["installs"][index]["environment"]
            install_id = self.get_sites_data()["results"][index]["installs"][index]["id"]
            site_name = self.get_sites_data()["results"][index]["name"]
            #data_json = json.dumps(data)
            #requests.post(self.installs_api, auth=(self.user, self.password), data=data_json)



    # Makes Post request to create install named domain in respective site experience

    def configure_domain():
        site_id
        domain_list
        install_id
        creds

        # Makes Post request to configure production domain to install in respective site experience 


if __name__ == '__main__':
    wpe = WpeAccount()
    wpe.get_creds()
    domain_list = wpe.get_cleaned_domains()
    # account_id_string = wpe.get_account_data()
    #wpe.create_site_experience(domain_list)
    wpe.create_installs(domain_list)
