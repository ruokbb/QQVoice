# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time: 2024/2/2 16:19
@Author: shiqixin.set
@File: device.py
@Software: PyCharm
@desc: 
"""
import os
from config import ADB_PATH, ANDROID_PATH
import subprocess
import datetime
import sys

class Device():
    def __init__(self, ip, port=5555, target_slk_path=None):
        self.ip = ip
        self.port = port
        self.connect_device()
        self.latest_slk_file = self.find_latest_slk_file()
        self.target_slk_path = target_slk_path

    def execute_adb_command(self, command):
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, error = process.communicate()

        if process.returncode != 0:
            if sys.platform == "win32":
                raise Exception(f"[Error] executing command: {command}. Error: {error.decode('gbk')}")
            else:
                raise Exception(f"[Error] executing command: {command}. Error: {error.decode('utf-8')}")
        else:
            if sys.platform == "win32":
                return output.strip().decode('gbk')
            else:
                return output.strip().decode('utf-8')

    def connect_device(self):
        connect_command = f"{ADB_PATH} connect {self.ip}:{self.port}"
        self.execute_adb_command(connect_command)

    def disconnect_device(self):
        disconnect_command = f"{ADB_PATH} disconnect {self.ip}:{self.port}"
        self.execute_adb_command(disconnect_command)

    def find_latest_slk_file(self):
        # 获取当前日期的年份和月份
        current_year = datetime.datetime.now().year
        current_month = datetime.datetime.now().month

        # 构建当前月份和日期的文件夹名称
        target_month = str(current_month).zfill(2)
        target_day = str(datetime.datetime.now().day)

        # 构建完整的路径
        target_folder = f'{ANDROID_PATH}/{current_year}{target_month}/{target_day}'

        # 执行adb shell命令获取slk文件路径
        command = f'{ADB_PATH} shell ls {target_folder}/*.slk'
        result = self.execute_adb_command(command)

        # 解析输出并找到最新的slk文件
        slk_files = result.split('\n')
        latest_slk_file = max(slk_files, key=lambda x: x.split('_')[1])

        # 返回完整路径
        return latest_slk_file

    def replace_silk(self):
        if self.target_slk_path is None:
            return -1

        push_command = f"{ADB_PATH} push {self.target_slk_path} {self.latest_slk_file}"
        self.execute_adb_command(push_command)
        return 1


