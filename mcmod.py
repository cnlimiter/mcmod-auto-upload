import json
import os
import time

import requests
from ruamel.yaml import YAML

from log import log

if not os.path.exists("mods"):
    os.makedirs("mods")
    log.info("已创建 mods 文件夹")

yaml = YAML()
with open('id.yml', 'r', encoding='utf-8') as f:
    yml = yaml.load(f)

cookie = 'XX'  # 填入_uuid


def upload(cookies: str, file, classID, mcVerList, platformList, apiList, tagList):
    start = time.time()
    url = 'https://modfile-dl.mcmod.cn/action/upload/'
    headers = {'Cookie': '_uuid=' + cookies}
    file1 = open('mods/' + file, 'rb')
    form = {
        'file1': file1,
        'classID': (None, classID),
        'mcverList': (None, mcVerList),
        'platformList': (None, platformList),
        'apiList': (None, apiList),
        'tagList': (None, tagList)
    }
    response = requests.post(url, headers=headers, files=form)
    msg = json.loads(response.text[3:])
    try:
        if msg['success']['upload']:
            log.info(f"文件 {file} 上传成功，{time.time() - start:.1f} s")
        elif msg['success']['update']:
            log.info(f"文件 {file} 覆盖成功，{time.time() - start:.1f} s")
        else:
            log.error(f"文件 {file} 上传失败，服务器返回信息如下：")
            log.error(msg)
    except KeyError:
        log.error(f"文件 {file} 上传失败，服务器返回信息如下：")
        log.error(msg)
    file1.close()


for mod in os.listdir("mods"):
    cache = os.path.splitext(mod)[0].split("-")
    abs_path = os.path.abspath(mod)
    if cache.__contains__("forge") or cache.__contains__("fabric") or cache.__contains__("quilt"):
        y = yml[cache[0]]
        upload(cookies=cookie, file=mod, classID=y["classID"], mcVerList=cache[2], platformList=y["platformList"],
               apiList=y["apiList"], tagList=y["tagList"])
    else:
        y = yml[cache[0]]
        upload(cookies=cookie, file=mod, classID=y["classID"], mcVerList=cache[1], platformList=y["platformList"],
               apiList=y["apiList"], tagList=y["tagList"])
