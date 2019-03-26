#!/bin/bash

### Build credentials

apicreds=$(echo $apiuser\:$apipass)
account_id=$(curl --silent -X GET "https://api.wpengineapi.com/v0/accounts?limit=100&offset=0" -H "accept: application/json" -u "$apicreds" | awk -F'[\"]' '{print $12}')
domains=$(cat domains.txt | sed 's/www\.//g' | awk '!a[$0]++')

### Prompting User for credential input

function setcreds () {

read -p 'Username: ' apiuser
read -sp 'Password: ' apipass

}

### Create Sites from the domain list and output to site_list.txt

function addsites () {

for i in $domains; do 
    curl --silent -X POST "https://api.wpengineapi.com/v0/sites" -H "accept: application/json" -u "$apicreds"  -H "Content-Type: application/json" -d "{ \"name\": \"$i\", \"account_id\": \"$account_id\"}" && echo ""; 
done > site_list.txt

}

### Add prod installs to the Site groups and output to install_list.txt

function addinstalls () {

cat site_list.txt | awk -F'[\"]' '{print $4,$8}' | sed 's/\.//g' | while read line; do 
        site_id=$(echo -e "$line" | awk '{print $1}'); 
        install_name=$(echo -e "$line" | awk '{print $2}' | sed 's/www\.//g' | sed 's/\.//g' | cut -c 1-11 | awk '{print $1 "prd"}'); 
   curl -X POST "https://api.wpengineapi.com/v0/installs" -H "accept: application/json" -u "$apicreds" -H "Content-Type: application/json" -d "{ \"name\": \"$install_name\", \"account_id\": \"$account_id\", \"site_id\": \"$site_id\", \"environment\": \"production\"}" && echo ""; 
    sleep 60; 
done > install_list.txt

}

### Add domains to the prod installs and output to domainsoutput.txt

function adddomains () {

domaindata=$(paste -d ' ' <(cat install_list.txt | awk -F'[\"]' '{print $4}') <(cat domains.txt | sed 's/www\.//g' | awk '!a[$0]++') > domaindata.txt)
cat domaindata.txt | while read line; do
    install_id=$(echo -e "$line" | awk '{print $1}');
    domain_name=$(echo -e "$line" | awk '{print $2}');
    www_domain_name=$(echo -e "$line" | awk '{print $2}' | sed -e 's/^/www\./');
curl --silent -X POST "https://api.wpengineapi.com/v0/installs/$install_id/domains" -H "accept: application/json" -u "$apicreds" -H "Content-Type: application/json" -d "{ \"name\": \"$domain_name\", \"primary\": true}" && echo ""; sleep 60; curl --silent -X POST "https://api.wpengineapi.com/v0/installs/$install_id/domains" -H "accept: application/json" -u "$apicreds" -H "Content-Type: application/json" -d "{ \"name\": \"$www_domain_name\", \"primary\": true}" && echo "";

done > domainsoutput.txt

}

function clean_up(){

rm site_list.txt install_list.txt domainsoutput.txt domaindata.txt

};
