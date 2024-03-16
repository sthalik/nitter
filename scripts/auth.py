# adapted from
# https://github.com/zedeus/nitter/issues/983#issuecomment-1914616663
import requests
import base64
import json
import sys
import os
import logging
from typing import Optional
from dataclasses import dataclass


logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG if os.getenv("DEBUG") == "1" else logging.INFO)


TW_CONSUMER_KEY = '3nVuSoBZnx6U4vzUxf5w'
TW_CONSUMER_SECRET = 'Bcs59EFbbsdF6Sl9Ng71smgStWEGwXXKSjYvPVt7qys'
TW_ANDROID_BASIC_TOKEN = 'Basic {token}'.format(token=base64.b64encode(
    (TW_CONSUMER_KEY + ":" + TW_CONSUMER_SECRET).encode()
).decode())
logging.debug("TW_ANDROID_BASIC_TOKEN=" + TW_ANDROID_BASIC_TOKEN)


def auth(username: str, password: str) -> Optional[dict]:
    logging.debug("start auth")

    bearer_token_req = requests.post("https://api.twitter.com/oauth2/token",
        headers={
        'Authorization': TW_ANDROID_BASIC_TOKEN,
        "Content-Type": "application/x-www-form-urlencoded",
        },
        data='grant_type=client_credentials'
    ).json()
    bearer_token = ' '.join(str(x) for x in bearer_token_req.values())
    logging.debug("bearer_token=" + bearer_token)

    guest_token = requests.post("https://api.twitter.com/1.1/guest/activate.json", headers={
        'Authorization': bearer_token,
    }).json()['guest_token']
    logging.debug("guest_token=" + guest_token)

    twitter_header = {
        'Authorization': bearer_token,
        "Content-Type": "application/json",
        "User-Agent":
            "TwitterAndroid/9.95.0-release.0 (29950000-r-0) ONEPLUS+A3010/9 (OnePlus;ONEPLUS+A3010;OnePlus;OnePlus3;0;;1;2016)",
        "X-Twitter-API-Version": '5',
        "X-Twitter-Client": "TwitterAndroid",
        "X-Twitter-Client-Version": "9.95.0-release.0",
        "OS-Version": "28",
        "System-User-Agent":
            "Dalvik/2.1.0 (Linux; U; Android 9; ONEPLUS A3010 Build/PKQ1.181203.001)",
        "X-Twitter-Active-User": "yes",
        "X-Guest-Token": guest_token,
    }

    session = requests.Session()

    task1 = session.post('https://api.twitter.com/1.1/onboarding/task.json',
        params={
            'flow_name': 'login',
            'api_version': '1',
            'known_device_token': '',
            'sim_country_code': 'us'
        },
        json={
            "flow_token": None,
            "input_flow_data": {
                "country_code": None,
                "flow_context": {
                    "referrer_context": {
                        "referral_details": "utm_source=google-play&utm_medium=organic",
                        "referrer_url": ""
                    },
                    "start_location": {
                        "location": "deeplink"
                    }
                },
                "requested_variant": None,
                "target_user_id": 0
            }
        },
        headers=twitter_header
    )

    session.headers['att'] = task1.headers.get('att')
    task2 = session.post('https://api.twitter.com/1.1/onboarding/task.json', 
        json={
            "flow_token": task1.json().get('flow_token'),
            "subtask_inputs": [{
                    "enter_text": {
                        "suggestion_id": None,
                        "text": username,
                        "link": "next_link"
                    },
                    "subtask_id": "LoginEnterUserIdentifier"
                }
            ]
        },
        headers=twitter_header
    )

    task3 = session.post('https://api.twitter.com/1.1/onboarding/task.json', 
        json={
            "flow_token": task2.json().get('flow_token'),
            "subtask_inputs": [{
                    "enter_password": {
                        "password": password,
                        "link": "next_link"
                    },
                    "subtask_id": "LoginEnterPassword"
                }
            ],
        },
        headers=twitter_header
    )

    task4 = session.post('https://api.twitter.com/1.1/onboarding/task.json', 
        json={
            "flow_token": task3.json().get('flow_token'),
            "subtask_inputs": [{
                    "check_logged_in_account": {
                        "link": "AccountDuplicationCheck_false"
                    },
                    "subtask_id": "AccountDuplicationCheck"
                }
            ]
        },
        headers=twitter_header
    ).json()

    for t4_subtask in task4.get('subtasks', []):
        if 'open_account' in t4_subtask:
            return t4_subtask['open_account']

    return None


def parse_auth_file(auth_file: str) -> bool:
    try:
        with open(auth_file, "r") as f:
            res = json.loads(f.read())
    except json.JSONDecodeError:
        logging.error(f"Auth file is not a valid json file")
        return False
    if isinstance(res, dict):
        logging.error(f"Expecting auth file to be a json list")
        return False
    if len(res) == 0:
        logging.error(f"Expecting auth file to be non-empty")
        return False
    for i, r in enumerate(res):
        if "oauth_token" not in r:
            logging.error(f"Expecting 'oauth_token' in auth item #{i}")
            return False
        if "oauth_token_secret" not in r:
            logging.error(f"Expecting 'oauth_token_secret' in auth item #{i}")
            return False
    return True


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 auth.py <output_file> <username> <password>")
        sys.exit(1)
    output_file = sys.argv[1]
    if os.path.exists(output_file):
        print(f"Validating auth file {output_file}")
        if parse_auth_file(output_file):
            print(f"Auth file {output_file} is valid")
            sys.exit(0)
        else:
            print(f"Auth file {output_file} is invalid. Please remove and rerun.")
            sys.exit(1)
    username = sys.argv[2]
    password = sys.argv[3]
    auth_res = auth(username, password)
    if auth_res is None:
        print("Failed authentication. You might have entered the wrong username/password or enabled MFA. Please rerun with environment variable DEBUG=1 for debugging.")
        sys.exit(1)
    with open(output_file, "w") as f:
        f.write(json.dumps([auth_res]))
    print(f"Auth file {output_file} created successfully")
