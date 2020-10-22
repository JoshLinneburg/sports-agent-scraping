#!/usr/bin/env python
# coding: utf-8

# In[23]:


import json
import requests
import pandas as pd
import time
from bs4 import BeautifulSoup as bs

results = []

base_url = 'https://www.fiba.basketball/en/Module/06bcf0e2-3456-4ad6-8ecc-bf65747492c4'

params = {'PersonSearch.Freetext': None, 
          'PersonSearch.Country': None, 
          'PersonSearch.Nationality': None, 
          'PersonId': None, 
          'type': 'searchresults'}

response = requests.get(url=base_url, params=params)

html = bs(response.text)
table = html.find('tbody')
rows = table.findAll('tr')
agent_ids = [row['data-item-id'] for row in rows]

for agent_id in agent_ids:
    response = requests.get(url=base_url, params={'type': 'item', 'PersonId': agent_id})
    agent = bs(response.text)
    
    agent_name_html = agent.find('div', class_='group_right')
    agent_details_html = agent.find('div', class_='agent_details')
    
    try:
        first_name = agent_name_html.find('span', class_='firstname').text.strip()
    except AttributeError:
        first_name = None
        
    try:
        last_name = agent_name_html.find('span', class_='lastname').text.strip()
    except AttributeError:
        last_name = None

    try:
        licence_number = agent_name_html.find('div', class_='licence_number').text.strip('\n').split('\n')[1]
    except AttributeError:
        licence_number = None
    except IndexError:
        licence_number = None

    try:
        company = agent_details_html.find('div', class_='company').text.strip('\n').split('\n')[1]
    except AttributeError:
        company = None
    except IndexError:
        company = None
        
    try:
        address = agent_details_html.find('div', class_='address').text.strip('\n').split('\n')[1]
    except AttributeError:
        address = None
    except IndexError:
        address = None
        
    try:
        office_tel = agent_details_html.find('div', class_='office_tel').text.strip('\n').split('\n')[1]
    except AttributeError:
        office_tel = None
    except IndexError:
        office_tel = None
        
    try:
        office_mobile = agent_details_html.find('div', class_='office_mobile').text.strip('\n').split('\n')[1]
    except AttributeError:
        office_mobile = None
    except IndexError:
        office_mobile = None
        
    try:
        office_email = agent_details_html.find('div', class_='office_email').text.strip('\n').split('\n')[1]
    except AttributeError:
        office_email = None
    except IndexError:
        office_email = None
        
    try:
        website = agent_details_html.find('div', class_='website').text.strip('\n').split('\n')[1]
    except AttributeError:
        website = None
    except IndexError:
        website = None
    
    d = {
        'first_name': first_name,
        'last_name': last_name,
        'licence_number': licence_number,
        'company': company,
        'address': address,
        'office_tel': office_tel,
        'office_mobile': office_mobile,
        'office_email': office_email,
        'website': website
    }
    
    results.append(d)
    
    time.sleep(1)
    
    print(f'{len(results)} / {len(agent_ids)} agents scraped!')
    
df = pd.DataFrame(results)
df.to_csv('nba_agents.csv', index=False)

