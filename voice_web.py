# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time: 2024/2/2 16:46
@Author: shiqixin.set
@File: voice_web.py
@Software: PyCharm
@desc: 
"""
import os.path

import gradio as gr
from fastapi import FastAPI
import uvicorn
from network.request import get_model_names_api, get_refer_list_api, upload_refer_api, download_wav_api
from parser.slk_product import get_silk_from_wav
from parser.amr_product import get_amr_from_wav

select_model_name = "default"
select_refer = "default"
wav_path = "aoutput.wav"


def get_model_names():
    data = get_model_names_api()
    if data is None:
        return ["default"]
    else:
        return data


def get_tone_list(model_name):
    data = get_refer_list_api(model_name)
    if data is None:
        return []
    else:
        return data


def change_model_names():
    _model_names = get_model_names()
    return {"choices": _model_names, "__type__": "update"}


def change_model(model_name):
    global select_model_name, select_refer
    select_model_name = model_name
    _tone_list = get_tone_list(model_name)
    if _tone_list:
        select_refer = _tone_list[0]
    else:
        select_refer = "default"
        _tone_list = ["default"]
    return {"choices": _tone_list, "value": _tone_list[0], "__type__": "update"}


def change_tone(tone):
    global select_refer
    select_refer = tone


def get_tts_wav(inp_ref, prompt_text, prompt_language, text, text_language):
    print(inp_ref)
    if inp_ref and prompt_text and prompt_language:
        # 自定义参考音频
        # 上传音频
        upload_result = upload_refer_api(inp_ref, prompt_text, prompt_language)
        if not upload_result:
            raise Exception("upload faild")
        # 获取音频
        download_result = download_wav_api("tmp", text, text_language, select_model_name, output_path=wav_path)
        if not download_result:
            raise Exception("download faild")
    else:
        # 使用预设音频
        download_result = download_wav_api(select_refer, text, text_language, select_model_name, output_path=wav_path)
        if not download_result:
            raise Exception("download faild")
    # 前端显示 output.wav
    # 打开音频文件并读取其内容
    with open(wav_path, 'rb') as f:
        audio_bytes = f.read()

    return audio_bytes


def download_slk():
    if os.path.exists(wav_path):
        slk_path = get_silk_from_wav(wav_path)
        return slk_path
    else:
        print("wav不存在:{}".format(wav_path))
        return ""


def download_amr():
    if os.path.exists(wav_path):
        amr_path = get_amr_from_wav(wav_path)
        return amr_path
    else:
        print("wav不存在:{}".format(wav_path))
        return ""


model_names = get_model_names()
tone_list = ["default"]

with gr.Blocks(title="语音替换") as demo:
    with gr.Group():
        gr.Markdown(value="模型选择")
        with gr.Row():
            model_dropdown = gr.Dropdown(label="模型列表", choices=model_names, value=select_model_name,
                                         interactive=True)
            refer_dropdown = gr.Dropdown(label="语气", choices=tone_list, value=select_refer, interactive=True)
            refresh_button = gr.Button("刷新模型列表", variant="primary")
            refresh_button.click(fn=change_model_names, inputs=[], outputs=[model_dropdown])
            model_dropdown.change(change_model, [model_dropdown], [refer_dropdown])
            refer_dropdown.change(change_tone, [refer_dropdown], [])
        gr.Markdown(value="*请上传并填写参考信息")
        with gr.Row():
            inp_ref = gr.Audio(label="请上传3-10秒内的参考音频，超时会报错！", type="filepath")
            prompt_text = gr.Textbox(label="参考音频文本", value="")
            prompt_language = gr.Dropdown(
                label="参考音频的语种", choices=["中文", "英文", "日文"]
            )
        gr.Markdown(value="请填写目标文本。中英混合选中文，日英混合选日文")
        with gr.Row():
            text = gr.Textbox(label="目标文本")
            text_language = gr.Dropdown(
                label="语种", choices=["中文", "英文", "日文"], value="中文"
            )
            inference_button = gr.Button("合成语音", variant="primary")
            output = gr.Audio(label="输出的语音")
        inference_button.click(
            get_tts_wav,
            [inp_ref, prompt_text, prompt_language, text, text_language],
            [output]
        )
        gr.Markdown(value="语音替换")
        with gr.Row():
            silk_file = gr.components.File(label="语音文件")
            slk_btn = gr.Button("生成slk文件", variant="primary")
            amr_btn = gr.Button("生成amr文件", variant="primary")
        slk_btn.click(fn=download_slk, outputs=silk_file)
        amr_btn.click(fn=download_amr, outputs=silk_file)

app = FastAPI()
app = gr.mount_gradio_app(app, demo, path="/QQVoice")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9769)
