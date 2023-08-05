name = "zoltpy"

import os
import time
import click
import requests
import json
import pprint

# ---- Variables ----
ZOLTAR_HOST = 'https://reichlab-forecast-repository.herokuapp.com'

# ---- the app ----
#@click.command()
#@click.argument('forecast_csv_file', type=click.Path(file_okay=True, exists=True))

def print_models():
    """
    This app demonstrates some of Zoltar's API features. It assumes the projects defined in make_minimal_projects.py
    have been loaded, and that an account with the appropriate authorizations is identified in the below environment
    variables.

    Inputs:
    - DEV_USERNAME environment variable: username of account in server
    - DEV_PASSWORD environment variable: password for ""
    - forecast_csv_file app argument: path of the forecast *.cdc.csv file to load into the private project's
    """
    #
    # authenticate the dev user
    #
    username = os.environ.get('DEV_USERNAME')
    mo1_token = get_token(ZOLTAR_HOST, username, os.environ.get('DEV_PASSWORD'))

    # Print indents in dictionaries
    pp = pprint.PrettyPrinter(indent=4)
    
    # Print models in a project
    projects = get_projects(ZOLTAR_HOST, mo1_token)
    project = get_project_from_obj_list(projects, 'CDC Flu challenge')
    pp.pprint(project['models'])
    

    model_uri = project['models'][0]
    print(mo1_token)
    model = get_resource(model_uri, mo1_token)
    #pp.pprint(model)

'''
def delete_forecast(timezero, forecast_csv_file):
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Delete the existing forecast, if any
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    username = os.environ.get('DEV_USERNAME')
    mo1_token = get_token(ZOLTAR_HOST, username, os.environ.get('DEV_PASSWORD'))

    timezero = '20181203'  # YYYYMMDD_DATE_FORMAT
    forecast_for_tz_date = get_forecast_from_obj(model, timezero_date)
    forecast_uri = forecast_for_tz_date['forecast']
    print('- forecast_for_tz_date', forecast_for_tz_date)
    # example:
    # {'timezero_date': '20170117', 'data_version_date': None, 'forecast': 'http://127.0.0.1:8000/api/forecast/40/'}

    if forecast_uri:
        print('  = deleting existing forecast', forecast_uri)
        delete_resource(forecast_uri, mo1_token)
    else:
        print('  = no existing forecast')


def upload_forecast(forecast_csv_file):
    # upload a new forecast
    #
    # from UploadFileJob:
    upload_file_job = upload_forecast(model_uri, mo1_token, timezero_date, forecast_csv_file)
    # example:
    # {'id': 50,
    #  'url': 'http://localhost:8000/api/uploadfilejob/50/',
    #  'status': 2,
    #  'user': 'http://localhost:8000/api/user/3/',
    #  'created_at': '2018-09-05T09:18:21.346093-04:00',
    #  'updated_at': '2018-09-05T09:18:22.164622-04:00',
    #  'failure_message': '',
    #  'filename': 'EW1-KoTsarima-2017-01-17-small.csv',
    #  'input_json': "{'forecast_model_pk': 3, 'timezero_pk': 4}",
    #  'output_json': None}
    upload_file_job = do_busy_poll(mo1_token, upload_file_job)

    #
    # print the model's forecasts again - see the new url for '20170117'?
    #
    model = get_resource(model_uri, mo1_token)
    print('- updated model forecasts', model['forecasts'])

    #
    # get the new forecast from the upload_file_job by parsing the generic 'output_json' field
    #
    new_forecast_pk = upload_file_job['output_json']['forecast_pk']
    new_forecast = get_forecast(ZOLTAR_HOST, mo1_token, new_forecast_pk)
    print('- new forecast', new_forecast_pk, new_forecast)

    #
    # GET its data (default format is JSON)
    #
    data_uri = new_forecast['forecast_data']
    data_json = get_resource(data_uri, mo1_token)
    print('- data_json', data_json)

    # GET the data as CSV
    # - todo fix api_views.forecast_data() to use proper accept type rather than 'format' query parameter
    response = requests.get(data_uri,
                            headers={'Authorization': 'JWT {}'.format(mo1_token)},
                            params={'format': 'csv'})
    data_csv = response.content
    print('- data_csv', data_csv)

    # done
    print('- done')
'''

#
# ---- REST and other utility functions ----
#

def print_json(my_json):
    parsed = json.loads(my_json)
    return print(json.dumps(parsed, indent=2, sort_keys=True))

def do_busy_poll(token, upload_file_job):
    #
    # get the updated status via polling (busy wait every 1 second)
    #
    #print('- polling for status change. upload_file_job pk:', upload_file_job['id'])
    print(upload_file_job)
    while True:
        upload_file_job = get_upload_file_job(ZOLTAR_HOST, token, upload_file_job['id'])
        status_out = upload_file_job['status']
        status_key = {
            0 :"PENDING",
            1 : "CLOUD_FILE_UPLOADED",
            2 : "QUEUED",
            3 : "CLOUD_FILE_DOWNLOADED",
            4 : "SUCCESS",
            5 : "FAILED"
        }
        
        print(status_key.get(status_out))
        time.sleep(1)
    return upload_file_job


def get_resource(uri, token):
    response = requests.get(uri, headers={'Accept': 'application/json; indent=4',
                                          'Authorization': 'JWT {}'.format(token)})
    return response.json()


def delete_resource(uri, token):
    response = requests.delete(uri, headers={'Accept': 'application/json; indent=4',
                                             'Authorization': 'JWT {}'.format(token)})
    if response.status_code != 204:  # HTTP_204_NO_CONTENT
        raise RuntimeError('delete_resource(): status code was not 204: {}'.format(response.text))


def get_token(host, username, password):
    response = requests.post(host + '/api-token-auth/', {'username': username, 'password': password})
    if response.status_code != 200:  # HTTP_200_OK
        raise RuntimeError('get_token(): status code was not 200: {}'.format(response.text))

    return response.json()['token']


def upload_forecast(model_uri, token, timezero_date, file):  # timezero_date format: YYYYMMDD_DATE_FORMAT
    response = requests.post(model_uri + 'forecasts/',
                             headers={'Authorization': 'JWT {}'.format(token)},
                             data={'timezero_date': timezero_date},
                             files={'data_file': open(file, 'rb')})
    return response.json()  # UploadFileJobSerializer


def get_projects(host, token):
    return get_resource(host + '/api/projects/', token)


def get_project(host, token, project_pk):
    return get_resource(host + '/api/project/{}/'.format(project_pk), token)


def get_upload_file_job(host, token, upload_file_pk):
    return get_resource(host + '/api/uploadfilejob/{}/'.format(upload_file_pk), token)


def get_project_from_obj_list(project_list, name):
    for project in project_list:
        if project['name'] == name:
            return project

    return None


def get_forecast_from_obj(model, timezero_date):  # timezero_date format: YYYYMMDD_DATE_FORMAT
    for forecast in model['forecasts']:
        if forecast['timezero_date'] == timezero_date:
            return forecast

    return None


def get_forecast(host, token, forecast_pk):
    return get_resource(host + '/api/forecast/{}/'.format(forecast_pk), token)


if __name__ == '__main__':
    print_models()