import requests, json


from django.http import HttpResponse, JsonResponse
from django.template import loader
from .climateservAPI import *




def home(request):
  template = loader.get_template('home.html')
  return HttpResponse(template.render())

def help(request):
  template = loader.get_template('help.html')
  return HttpResponse(template.render())


async def dashboard(request):
    if request.method == 'GET':
        template = loader.get_template('dashboard.html')
        return HttpResponse(template.render())
    
    if request.method == 'POST':
        try:
            # Parse the incoming JSON request
            data = json.loads(request.body)
            years = 2

            # Create the request parameters
            params_list = createRequests(data, years)

                       # Process the API requests asynchronously
            response_list = await process_api_requests(params_list)
            # Process the API results (assuming waitResult can handle the response_list)
            avrg_result = await waitResult(response_list, years)
            response_data = {
                'id': data.get('id'),
                'status': 'success',
                'message': 'Request received!',
                'result': avrg_result
            }

            # Return the JSON response
            return JsonResponse(response_data)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

