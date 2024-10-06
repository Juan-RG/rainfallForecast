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
            ## ToDo: Answer the client and manage petitions in background asyncrous call
            data = json.loads(request.body)
            years = 2
            params_list = createRequests(data,years)
            # Print all parameter sets
            response_list = []
            for index, params in enumerate(params_list):
                # Define the API URL
                api_url = 'https://climateserv.servirglobal.net/api/submitDataRequest/'
                response = requests.get(api_url, params=params)
                if response.status_code == 200:
                    response_text = response.text
                    id = re.search(r'\["(.*?)"\]', response_text)
                    extracted_value = id.group(1)
                    print(extracted_value)
                    response_list.append(extracted_value)  # Add the parameter set to the list
                    #avrg = waitResult(extracted_value)

                else:
                    print(f"Request failed with status code {response.status_code}")
                
            
            avrg_result = waitResult(response_list, years)
            response_data = {
                'status': 'success',
                'message': 'Request received!',
                'result': avrg_result  # Optional: Echo back the received data
            }
            #answer the client
            return JsonResponse(response_data)  # Send back a JSON response                
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        
def waitResult(extracted_value, years):
    api_url = 'https://climateserv.servirglobal.net/api/getDataRequestProgress/'
    for index, params in enumerate(extracted_value):
        params = {
            'id': params
        }
        progress = ""
        while progress != "[100.0]":
            #Wait for the last petition
            progress = requests.get(api_url, params=params)
            print(progress.text)
            progress = progress.text

    avg_list = []        
    for index, params in enumerate(extracted_value):
        api_url = 'http://climateserv.servirglobal.net/api/getDataFromRequest/'
        params = {
            'id': params
        }
        response = requests.get(api_url, params=params)
        # Extracting all the max values
        data = json.loads(response.text)
        avg_values = [item['value']['avg'] for item in data['data']]
        average = sum(avg_values) / len(avg_values)
        avg_list.append(average)

    if avg_list:
        overall_average = sum(avg_list) / len(avg_list)
        print(f"The overall average is: {overall_average}")
    else:
        print("The avg_list is empty. Cannot compute the overall average.")

    return overall_average

def createRequests(data, years):
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
    date_before = date - timedelta(days=4)
    date_after = date + timedelta(days=4)
    #three_days_before = three_days_before.strftime("%m/%d/%Y")
    #three_days_after = three_days_after.strftime("%m/%d/%Y")


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

    # Initialize a list to hold all parameter sets
    params_list = []

    for i in range(years):
        params = {
            'datatype': 0,  # Example: different datatype for each set
            'begintime': date_before.replace(year=date.year - i).strftime("%m/%d/%Y"),
            'endtime': date_after.replace(year=date.year - i).strftime("%m/%d/%Y"),
            'intervaltype': 0,
            'operationtype': 5,
            'callback': 'successCallback',
            'dateType_Category': 'default',
            'isZip_CurrentDataType': 'false',
            'geometry': json.dumps(geometry)
        }
        
        params_list.append(params)  # Add the parameter set to the list
        
    
    return params_list


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


