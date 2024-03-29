# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time: 2024/2/5 10:26
@Author: shiqixin.set
@File: slk_product.py
@Software: PyCharm
@desc: 
"""
from pathlib import Path
import subprocess
import os


def get_silk_from_wav(wav_path: str) -> str:
    """尝试将wav转换成silk文件"""
    slk_path = wav_path.replace('.wav', '.slk')
    if Path(slk_path).exists():
        os.remove(slk_path)

    command = "sh ./bin/wav2silk.sh {}".format(wav_path)
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = p.communicate()
    errMsg = stderr.decode().strip()
    # if errMsg: # ffmpeg 把所有信息输出到 stderr 了。。。
    #     print(errMsg)

    if Path(slk_path).exists():
        return slk_path
    else:
        return ""
