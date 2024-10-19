from datetime import datetime, timedelta
import json
import sys
import re
import asyncio
import aiohttp
import random  # Import random module

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

def createRequests(data, years=2):
    """
    Create a list of API request parameters for the given data and number of years.

    Args:
        data (dict): Dictionary containing the required fields for API requests.
        years (int): Number of years for which to generate requests (default: 2).

    Returns:
        list: A list of dictionaries with API request parameters.
    """
    
    try:
        # Extract coordinates and other required data from the input
        min_lat = data['minLat']
        max_lat = data['maxLat']
        min_lng = data['minLng']
        max_lng = data['maxLng']
        date_str = data['date']
    except KeyError as e:
        raise ValueError(f"Missing required field: {e}")

    try:
        # Parse the date
        date = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Invalid date format. Expected YYYY-MM-DD")

    # Adjust the date by reducing one year
    date = date.replace(year=date.year - 1)

    # Calculate the range (three days before and after the date)
    date_before = date - timedelta(days=2)
    date_after = date + timedelta(days=2)

    # Define the bounding box coordinates as a polygon
    coordinates = [
        [min_lng, min_lat],  # Bottom-left
        [min_lng, max_lat],  # Top-left
        [max_lng, max_lat],  # Top-right
        [max_lng, min_lat],  # Bottom-right
        [min_lng, min_lat],  # Close the polygon
    ]
    geometry = {
        "type": "Polygon",
        "coordinates": [coordinates]
    }

    # List to hold the generated parameters for each year
    params_list = []

    # Loop through the number of years and generate request parameters
    for i in range(years):
        params = {
            'datatype': 0,  # Example: datatype remains the same
            'begintime': date_before.replace(year=date.year - i).strftime("%m/%d/%Y"),
            'endtime': date_after.replace(year=date.year - i).strftime("%m/%d/%Y"),
            'intervaltype': 0,
            'operationtype': 5,
            'callback': 'successCallback',
            'dateType_Category': 'default',
            'isZip_CurrentDataType': 'false',
            'geometry': json.dumps(geometry)
        }
        params_list.append(params)

    return params_list

# Helper function to make API requests
async def fetch_api_data(session, api_url, params):
    try:
        async with session.get(api_url, params=params) as response:
            if response.status == 200:
                response_text = await response.text()
                id_match = re.search(r'\["(.*?)"\]', response_text)
                if id_match:
                    return id_match.group(1)
            elif response.status == 503:
                wait_time = random.uniform(0, 0.2)
                await asyncio.sleep(wait_time)
                return await fetch_api_data(session, api_url, params)  # Retry the request
            else:
                return f"Error: {response.status}"
    except aiohttp.ClientError as e:
        return f"Request failed: {str(e)}"

# Asynchronous function to process multiple API requests
async def process_api_requests(params_list):
    api_url = 'https://climateserv.servirglobal.net/api/submitDataRequest/'
    async with aiohttp.ClientSession() as session:  # Create a single session for all requests
        tasks = [fetch_api_data(session, api_url, params) for params in params_list]
        return await asyncio.gather(*tasks)  
    


# Asynchronous version of the function
async def waitResult(extracted_value, years):
    api_progress_url = 'https://climateserv.servirglobal.net/api/getDataRequestProgress/'
    api_data_url = 'http://climateserv.servirglobal.net/api/getDataFromRequest/'
    
    async with aiohttp.ClientSession() as session:
        # List to store the tasks for checking progress
        progress_tasks = []
        
        for params in extracted_value:
            progress_tasks.append(check_progress(session, api_progress_url, params))
        
        # Wait for all progress tasks to complete
        await asyncio.gather(*progress_tasks)
        
        # Now create tasks to get data from the API after progress is 100%
        data_tasks = []
        avg_list = []
        
        for params in extracted_value:
            data_tasks.append(get_data_from_api(session, api_data_url, params, avg_list))
        
        # Wait for all data tasks to complete
        await asyncio.gather(*data_tasks)

    if avg_list:
        overall_average = sum(avg_list) / len(avg_list)
        print(f"The overall average is: {overall_average}")
        return overall_average
    else:
        print("The avg_list is empty. Cannot compute the overall average.")
        return None

# Asynchronous function to check progress
async def check_progress(session, api_url, params):
    params = {'id': params}
    progress = ""
    while progress != "[100.0]":
        async with session.get(api_url, params=params) as response:
            progress = await response.text()
            print(progress)
            
            if progress == "[-1]":
                break  # Stop if there's an error or invalid request
            
        await asyncio.sleep(1)  # Add a short sleep to avoid spamming the API

# Asynchronous function to get data from the API
async def get_data_from_api(session, api_url, params, avg_list):
    params = {'id': params}
    
    async with session.get(api_url, params=params) as response:
        response_text = await response.text()
        data = json.loads(response_text)
        
        # Extract the avg values from the data
        avg_values = [item['value']['avg'] for item in data['data']]
        print(avg_values)
        
        if avg_values:
            average = sum(avg_values) / len(avg_values)
            avg_list.append(average)



"""
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
            id = data.get('id')
            response_data = {
                'id': id,
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
            if progress.text == "[-1]" :
                break
    
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
        print(avg_values)
        average = sum(avg_values) / len(avg_values)
        avg_list.append(average)

    if avg_list:
        overall_average = sum(avg_list) / len(avg_list)
        print(f"The overall average is: {overall_average}")
    else:
        print("The avg_list is empty. Cannot compute the overall average.")

    return overall_average

"""

