import requests, json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader

def dashboard(request):
    # Render the dashboard template for GET requests
    if request.method == 'GET':
        template = loader.get_template('dashboard.html')
        return HttpResponse(template.render())

    # Handle POST requests
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message = data.get('data', None)  # Extract the 'data' field
            print("Received data:", message)  # This will log to the console
            
            # You can process the data and prepare a response
            response_data = {
              'status': 'success',
              'message': 'Data received successfully!',
              'received_data': data  # Optional: Echo back the received data
            }
            return JsonResponse(response_data)  # Send back a JSON response
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
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