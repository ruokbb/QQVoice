# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time: 2024/2/4 11:06
@Author: shiqixin.set
@File: request.py
@Software: PyCharm
@desc: 
"""

import requests
import json
from network.config import GET_MODEL_NAMES_URL, GET_REFER_LIST_URL, UPLOAD_REFER_URL, DOWNLOAD_WAV_URL, TOKEN


def get_model_names_api():
    headers = {"token": TOKEN}
    response = requests.get(GET_MODEL_NAMES_URL, headers=headers)
    data = response.json()
    if data['code'] == 0:
        return data['data']
    else:
        print("Error:", data['message'])
        return None


def get_refer_list_api(model_name="default"):
    headers = {"token": TOKEN}
    response = requests.get(GET_REFER_LIST_URL + "?model_name={}".format(model_name), headers=headers)
    data = response.json()
    if data['code'] == 0:
        return data['data']
    else:
        print("Error:", data['message'])
        return None


def upload_refer_api(file_path, file_text, file_language):
    headers = {"token": TOKEN}
    data = {"file_text": file_text, "file_language": file_language}
    with open(file_path, "rb") as f:
        files = {"file": ("tmp.wav", f)}
        response = requests.post(UPLOAD_REFER_URL, headers=headers, data=data, files=files)
    data = response.json()
    if data['code'] == 0:
        print("Success")
        return 1
    else:
        print("Error:", data['message'])
        return -1


def download_wav_api(refer_name, text, text_language, model_name, output_path="output.wav"):
    headers = {"token": TOKEN}
    payload = {"refer_name": refer_name, "text": text, "text_language": text_language, "model_name": model_name}
    response = requests.get(DOWNLOAD_WAV_URL, headers=headers, params=payload)
    if 'audio/wav' in response.headers['Content-Type']:
        with open(output_path, 'wb') as f:
            f.write(response.content)
        return 1
    elif 'application/json' in response.headers['Content-Type']:
        json_data = response.json()
        print(json_data)
        return -1
