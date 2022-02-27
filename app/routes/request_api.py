import uuid
import random
import datetime
import json
import os
import pathlib
import time
import requests
from flask import jsonify, abort, request, Blueprint


OPEN_WEATHER_API_KEY = "0c14cc83914e1e5ea5f85656c5dcc762"

parentDir = pathlib.Path(__file__).parent.resolve()

REQUEST_API = Blueprint('request_api', __name__)


def get_blueprint():
    # Return blueprint of the main app module
    return REQUEST_API


@REQUEST_API.route('/recent_request', methods=['GET'], strict_slashes=False)
def get_most_recent_request_record():

    request_record_root = os.path.join(parentDir, 'request_records', '')
    file_list = os.listdir(request_record_root)
    path_list = [os.path.join(request_record_root, filename) for filename in file_list]

    for theFile in path_list:
        date_str0 = os.path.basename(theFile).split('request_')[1].split('.json')[0]
        datetime_obj0 = datetime.datetime.strptime(date_str0, '%m:%d:%y:%H:%M:%S')
        for compare_file in path_list:
            date_str1 = os.path.basename(compare_file).split('request_')[1].split('.json')[0]
            datetime_obj1 = datetime.datetime.strptime(date_str1, '%m:%d:%y:%H:%M:%S')
            if datetime_obj1 > datetime_obj0:
                recent_file = compare_file
            if datetime_obj1 < datetime_obj0:
                recent_file = theFile
    print(recent_file)
    with open(recent_file, 'r') as request_file:
        file_content = json.load(request_file)

    return jsonify([file_content]), 200

@REQUEST_API.route('/requests', methods=['GET'])
def get_requests():

    request_record_root = os.path.join(parentDir, 'request_records', '')
    file_list = os.listdir(request_record_root)
    path_list = [os.path.join(request_record_root, filename) for filename in file_list]

    requestRecordList = []
    for filePath in path_list:
        with open(filePath, 'r') as requestRecordFile:
            requestRecord = json.load(requestRecordFile)
        requestRecordList.append(requestRecord)

    #print(f"requestRecordList: {requestRecordList}")
    return jsonify({"requests": requestRecordList}), 200
    #return_list = [{'uuid': '99e4eb45-3baa-426a-a7b7-1cd838382b8d', 'city_name': 'Boston', 'field': 'temp', 'date': '02:24:22:21:06:20'},
    #               {'uuid': '8a741b23-8b72-4a98-8775-ff7ce3b4232b', 'city_name': 'London', 'field': 'temp', 'date': '02:23:22:15:25:56'}]
    #return jsonify({'requests': return_list}), 200


@REQUEST_API.route('/create_request', methods=['POST'])
def create_request():

    if not request.get_json(force=True):
        abort(400)
    data = request.get_json(force=True)

    date_now = datetime.datetime.now().strftime("%m:%d:%y:%H:%M:%S")
    request_record_filename = f'request_{date_now}.json'
    req_record_path = os.path.join(parentDir, 'request_records', request_record_filename)
    new_uuid = str(uuid.uuid4())
    json_entry = {'uuid': new_uuid, 'data': data, 'date': date_now}
    with open(req_record_path, 'w') as req_record_file:
        json.dump(json_entry, req_record_file)

    print(f"Created request: {json_entry}")

    return jsonify({'request': json_entry}), 200


@REQUEST_API.route('/', methods=['GET','POST'])
def get_weather_by_city_info():

    if not request.get_json(force=True):
        abort(400)
    data = request.get_json(force=True)
    print(data)

    # search by city name, city id, city lat/lon coordinates, city zipcode
    data_keys = data['data'].keys()
    if 'city_name' in data_keys:
        city_info = f"{data['data']['city_name']}"
        if 'state_code' in data_keys:
            city_info = f"{data['data']['city_name']},{data['data']['state_code']}"
        if 'country_code' in data_keys:
            city_info = f"{data['data']['city_name']},{data['data']['state_code']},{data['data']['country_code']}"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city_info}&appid={OPEN_WEATHER_API_KEY}"

    if 'city_id' in data_keys:
        city_info = f"{data['data']['city_id']}"
        url = f"http://api.openweathermap.org/data/2.5/weather?id={city_info}&appid={OPEN_WEATHER_API_KEY}"

    if ('lat' and 'lon') in data_keys:
        city_info = f"lat={data['data']['lat']}&lon={data['data']['lon']}"
        url = f"http://api.openweathermap.org/data/2.5/weather?{city_info}&appid={OPEN_WEATHER_API_KEY}"

    if ('zip_code' and 'country_code') in data_keys:
        city_info = f"{data['data']['zip_code']}, {data['data']['country_code']}"
        url = f"http://api.openweathermap.org/data/2.5/weather?zip={city_info}&appid={OPEN_WEATHER_API_KEY}"

    print(url)
    response = requests.get(url)
    response_json = json.loads(response.text)
    print(response_json)

    if data['data']['field'] == 'temp':
        result = response_json['main']['temp']
    if data['data']['field'] == 'temp min':
        result = response_json['main']['temp_min']
    if data['data']['field'] == 'temp max':
        result = response_json['main']['temp_max']
    if data['data']['field'] == 'real feel':
        result = response_json['main']['feels_like']
    if data['data']['field'] == 'pressure':
        result = response_json['main']['pressure']
    if data['data']['field'] == 'humidity':
        result = response_json['main']['humidity']

    print(f"result: {result}")

    return jsonify({f"result": result}), 200


if __name__ == "__main__":
    #jobs_user_org_path = os.path.join(parentDir, 'jobs', defaultOrg, defaultUser, 'wrf', '456g', '')
    #print(jobs_user_org_path)
    pass