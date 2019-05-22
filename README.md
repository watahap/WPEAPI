This script ties into CAPI to create customers accounts based on a list of domain names. 

In the same working directory as the script, place the list of domains you're wanting to create into a file named *domains.txt*.

The logic of the script will remove protocols, www subdomains, and all variations of extra whitespace in the formatting. 

Example list of domains: 

http://domain.com
https://www.domain.com
shop.domain.com

The script breaks down into 4 major functions: 

# get_cleaned_domains

Before processing the domains, this function's logic cleans them up.  Being that the rest of the script hinges on these domains, we've gotta have a solid data set for the script to ingest. 

Since the user portal doesn't like installs that start with numbers, and site experiences over 40 characters, we take care of that here as well. 

# create_site_experience

Ingesting each line of the cleaned domains, we make a post request to the sites experiences endpoint creating one named for each respective line.

# create_installs

After the sites have been created, we use the JSON output of the sites endpoint to set our variables for the post request to the installs endpoint. 

Given that installs can't be over 14 characters, we build logic into the function to work within that restriction.  There is also logic to retry on duplicate install names, shortening the length of the install name by one index each attempt (2 retries total). 

# configure_domains

Using the same sites endpoint, we craft the URL to for the post request to the domains endpoint.  Once we have that URL, we make the post request to configure domain.com and www.domain.com for each install respectively. 
