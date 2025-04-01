import requests
from airtable import Airtable
import os
from os.path import join, dirname
from dotenv import load_dotenv
from tqdm import tqdm

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

base_id = os.environ.get('base_id')
table_name = os.environ.get('table_name')
airtable_token = os.environ.get('airtable_token')
api_key = os.environ.get('api_key')

airtable = Airtable(base_id, table_name, airtable_token)


headers = {'Authorization': 'Bearer ' + api_key}
api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
params = {
    'linkedin_profile_url': None,
    'personal_contact_number': 'include',
    'personal_email': 'include',
    'inferred_salary': 'include',
    'skills': 'include',
    'use_cache': 'if-present',
    'fallback_to_cache': 'on-error',
}

for record in tqdm(airtable.get_all()):
    id = record['id']
    params['linkedin_profile_url'] = record['fields']['LinkedIn']
    response = requests.get(api_endpoint,
                            params=params,
                            headers=headers).json()
    if 'experiences' in response:
        current_company = response['experiences'][0]['company']
        title = response['experiences'][0]['title']
        airtable.update(id, {'Current company': current_company,
                             'Job title': title})
    else:
        airtable.update(id, {'Current company': "unknown",
                             'Job title': "unknown"})
        print(response)