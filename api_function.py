import requests


def get_lat_long(country_name:str):
    
    api_url = 'https://api.api-ninjas.com/v1/geocoding?city={}'.format(country_name)
    response = requests.get(api_url + country_name, headers={'X-Api-Key': 'FiO9Z3Qca/VxkcMsfLuqZA==g3UfHYWbuYY7YfKP'})
    if response.status_code == requests.codes.ok:
        print(response.text)
    else:
        print("Error:", response.status_code, response.text)

get_lat_long("India")