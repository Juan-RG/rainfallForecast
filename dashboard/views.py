import requests, json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

def dashboard(request):
  template = loader.get_template('dashboard.html')
  return HttpResponse(template.render())

@csrf_exempt
def fetchingClimateSERV(request):
  if request.method == 'POST':
        data = json.loads(request.body)
        min_lat = data.get('minLat')
        max_lat = data.get('maxLat')
        min_lng = data.get('minLng')
        max_lng = data.get('maxLng')
        # if to be used in the future might need to convert datatype
        # location = data.get('location')
        # characteristics = data.get('characteristics')

        # Construct the ClimateSERV API request
        api_url = 'https://climateserv.servirglobal.net/chirps/submitDataRequest/'
        params = {
            'datatype': 0,  # Assuming 'rainfall' for now: takes integer and 0 is for rainfall
            'begintime': '2023-01-01',  # Example start date
            'endtime': '2023-12-31',  # Example end date
            'intervaltype': 0,  # Example interval type
            'operationtype': 0,  # Example operation type
            'geometry': f'POLYGON(({min_lng} {min_lat},{max_lng} {min_lat},{max_lng} {max_lat},{min_lng} {max_lat},{min_lng} {min_lat}))',
        }

        # Make the API request
        response = requests.get(api_url, params=params)

        # Process the response and return the data
        return JsonResponse(response.json())