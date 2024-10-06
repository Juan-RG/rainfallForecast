import requests, json
import re
from datetime import datetime, timedelta
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader

def home(request):
  template = loader.get_template('home.html')
  return HttpResponse(template.render())

def dashboard(request):
    # Render the dashboard template for GET requests
    if request.method == 'GET':
        template = loader.get_template('dashboard.html')
        return HttpResponse(template.render())

    # Handle POST requests
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            api_url, params = createRequest(data)
            response = requests.get(api_url, params=params)
            if response.status_code == 200:
                response_text = response.text
                print(response_text)
                id = match = re.search(r'\["(.*?)"\]', response_text)
                extracted_value = id.group(1)
                print(extracted_value)
                avrg = waitResult(extracted_value)
                response_data = {
                    'status': 'success',
                    'message': 'Request received!',
                    'received_data': data  # Optional: Echo back the received data
                }
            else:
                print(f"Request failed with status code {response.status_code}")
            return JsonResponse(response_data)  # Send back a JSON response
                   
            return JsonResponse(response_data)  # Send back a JSON response
        except json.JSONDecodeError:
            print("Entro2")
            return JsonResponse({"error": "Invalid JSON"}, status=400)
def waitResult(extracted_value):
    api_url = 'https://climateserv.servirglobal.net/api/getDataRequestProgress/'
    params = {
        'id': extracted_value
    }
    progress = ""
    while progress != "[100.0]":
        progress = requests.get(api_url, params=params)
        print(progress)
        print(progress.text)
        progress = progress.text

    api_url = 'http://climateserv.servirglobal.net/api/getDataFromRequest/'
    response = requests.get(api_url, params=params)
    print(response)
    print(response.text)

    return response

def createRequest(data):
    min_lat = data.get('minLat')
    max_lat = data.get('maxLat')
    min_lng = data.get('minLng')
    max_lng = data.get('maxLng')
    location = data.get('location')
    characteristics = data.get('characteristics')
    date = data.get('date')
    date = datetime.strptime(date, "%Y-%m-%d")

    # Reduce the year by 1
    date = date.replace(year=date.year - 1)

    # Calculate three days before and after
    three_days_before = date - timedelta(days=30)
    three_days_after = date + timedelta(days=30)
    print(three_days_before)
    print(three_days_after)
    three_days_before = three_days_before.strftime("%m/%d/%Y")
    three_days_after = three_days_after.strftime("%m/%d/%Y")

            # Define the API URL
    api_url = 'https://climateserv.servirglobal.net/api/submitDataRequest/'

    coordinates = [
                [min_lng, min_lat],  # Bottom-left corner
                [min_lng, max_lat],  # Top-left corner
                [max_lng, max_lat],  # Top-right corner
                [max_lng, min_lat],  # Bottom-right corner
                [min_lng, min_lat],  # Close the polygon by repeating the first point
            ]
    geometry = {
                "type": "Polygon",
                "coordinates": [coordinates]
            }                        
            # Parameters to be added
    params = {
                'datatype': 0,
                'begintime': three_days_before,
                'endtime':  three_days_after,
                'intervaltype': 0,
                'operationtype': 5,
                'callback': 'successCallback',
                'dateType_Category': 'default',
                'isZip_CurrentDataType': 'false',
                'geometry': json.dumps(geometry)
            }
    
    return api_url,params


''''
def dashboard(request):
  template = loader.get_template('dashboard.html')
  print("Entro")
  return HttpResponse(template.render())
@csrf_exempt
def fetchingClimateSERV(request):
  print("Entro2")
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
        api_url = 'https://climateserv.servirglobal.net/api/submitDataRequest/?datatype=0&begintime=01/01/2023&endtime=12/30/2023&intervaltype=0&operationtype=5&callback=successCallback&dateType_Category=default&isZip_CurrentDataType=false&geometry={"type":"Polygon","coordinates":[[[min_lng,min_lat],[max_lng,min_lat],[max_lng,max_lat],[min_lng,max_lat],[min_lng,min_lat]]]}'
        # params = {
        #     'datatype': 0,  # Assuming 'rainfall' for now: takes integer and 0 is for rainfall
        #     'begintime': '2023-01-01',  # Example start date
        #     'endtime': '2023-12-31',  # Example end date
        #     'intervaltype': 0,  # Example interval type
        #     'operationtype': 0,  # Example operation type
        #     'geometry': {"type":"Polygon","coordinates":[[[min_lng, min_lat], [max_lng, min_lat], [max_lng, max_lat], [min_lng, max_lat], [min_lng, min_lat]]]}
        # }

        # Make the API request
        response = requests.get(api_url, params=params)

        # Process the response and return the data
        return JsonResponse(response.json())
'''

def help(request):
  template = loader.get_template('help.html')
  return HttpResponse(template.render())


