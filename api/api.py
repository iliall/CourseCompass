import os
import requests

API_KEY = os.getenv('API_KEY')

class API:
    def requirementsDescription(request: dict) -> str:
        term = request.get('term')
        subject = request.get('subject')
        catalogNumber = request.get('catalog-number')
        headers = {'x-api-key': API_KEY}
        response = requests.get('https://openapi.data.uwaterloo.ca/v3/Courses/' + 
                                str(term) + '/' + 
                                str(subject) + '/' + 
                                str(catalogNumber), headers=headers)
        if response.status_code == 200:
            return response.json()[0].get('requirementsDescription')
        else:
            return response.text
        
    def subjects() -> list[str]:
        headers = {'x-api-key': API_KEY}
        response = requests.get('https://openapi.data.uwaterloo.ca/v3/Subjects', headers=headers)
        if response.status_code == 200:
            codes = [subject['code'] for subject in response.json()]
            return codes
        else:
            return [response.text]
        
    def codes(request: dict) -> list[str]:
        term = request.get('term')
        subject = request.get('subject')
        headers = {'x-api-key': API_KEY}
        response = requests.get('https://openapi.data.uwaterloo.ca/v3/Courses/' + 
                                str(term) + '/' + 
                                str(subject), headers=headers)
        if response.status_code == 200:
            codes = [course['catalogNumber'] for course in response.json()]
            return codes
        else:
            return []