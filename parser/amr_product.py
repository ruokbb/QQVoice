# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time: 2024/2/6 17:26
@Author: shiqixin.set
@File: amr_product.py
@Software: PyCharm
@desc: 
"""
from pathlib import Path
import subprocess
import os

def get_amr_from_wav(wav_path: str) -> str:
    """尝试将wav转换成silk文件"""
    amr_path = wav_path.replace('.wav', '.amr')
    slk_path = wav_path.replace('.wav', '.slk')
    if Path(amr_path).exists():
        os.remove(amr_path)
    if Path(slk_path).exists():
        os.remove(slk_path)

    command = "sh ./bin/wav2silk.sh {}".format(wav_path)
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = p.communicate()
    errMsg = stderr.decode().strip()
    # if errMsg: # ffmpeg 把所有信息输出到 stderr 了。。。
    #     print(errMsg)

    if Path(slk_path).exists():
        os.rename(slk_path, amr_path)
        return amr_path
    else:
        return ""
