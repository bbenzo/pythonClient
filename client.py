import json

import requests

from helpers import auth_header, api_response
from models import RegisterRequest, AccessRefreshToken, LoginRequest, ProfileRequest, AccessToken

host = "https://app.dev.finux.ai/"

def access_for_refresh_token(token):
    path = "api/refreshtoken"
    request = {
        "refreshToken": token
    }

    response = requests.post(host + path, data=request)
    data = json.loads(response.text)

    return AccessToken.from_json(data)

def health_check():
    path = "api/ping"
    response = requests.get(host+path)
    return response


def register(name, password, repeat_password):
    path = "api/register"

    request = RegisterRequest(name, password, repeat_password)

    # send register credentials
    response = requests.post(host+path, data=request.to_json())

    # create register data
    result = api_response(response)
    return AccessRefreshToken(result.data)


def login(name, password):
    path = "/api/login"

    request = LoginRequest(name, password)

    # send register credentials
    response = requests.post(host + path, data=request.to_json())

    # create register data
    result = api_response(response)
    return AccessRefreshToken(result.data)


def profile(business_ID, company, first_name, last_name, tokens):
    path = "/api/user/profile"

    # create request
    request = ProfileRequest(
        business_ID=business_ID,
        company=company,
        first_name=first_name,
        last_name=last_name
    )

    # first we try the access token
    headers = auth_header(tokens.access_token)
    response = requests.put(host+path, headers=headers, data=request.to_json())

    # if access token is expired, we send the request token to fetch another access token
    if response.status_code == 401:
        access_token = access_for_refresh_token(tokens.refresh_token)
        headers = auth_header(access_token)
        response = requests.put(host + path, headers=headers, data=request.to_json())

    # map to response model
    result = api_response(response)
    return result.status


def fetch_data():
    path = "/api/user/profile"
    response = requests.get(host+path)
    # something
    pass

def change_password(new_password, old_password, repeat_password):
    path = "/api/user/changepw"
    response = requests.put(host+path)
    # something
    pass

def feedback(message, reply):
    path = "/api/user/feedback"
    response = requests.post(host+path)
    # something
    pass

def connect_bank_account(bank_code, extra_secret, save_secret, secret, username):
    path = "/api/user/connector/bank/account"
    response = requests.post(host+path)
    # something
    pass

def get_all_bank_accounts():
    path = "/api/user/connector/bank/account"
    response = requests.get(host+path)
    # something
    pass

def get_forecast():
    path = "/api/user/intelligence/forecast"
    response = requests.get(host+path)
    # something
    pass

def get_partners():
    path = "/api/user/intelligence/procentpartner/{span}"
    response = requests.get(host+path)
    # something
    pass

def get_top_customers_suppliers():
    path = "/api/user/intelligence/toppartner/{request_type}/{span}"
    response = requests.get(host+path)
    # something
    pass

def get_smartalerts():
    path = "api/user/intelligence/smartalerts"
    response = requests.get(host+path)
    # something
    pass

def branches():
    path = "api/ressources/branches"
    response = requests.get(host+path)
    # something
    pass


if __name__ == "__main__":
    # test register function
    register_data = register("bba1210@web.de", "Meinpasswort#12", "Meinpasswort#12")


