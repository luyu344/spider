from mitmproxy import ctx
import time
import hashlib
import os

md5=hashlib.md5()
time_text=(time.strftime('%Y-%m-%d')+'vps_24').encode('utf-8')
md5.update(time_text)
uuid='xDVG2'+md5.hexdigest()[:11]

#xDVG2 xDVT3
def response(flow):
    with open(os.path.dirname(__file__)+'/san.js','r') as f:
        text=f.read()
    with open(os.path.dirname(__file__)+'/mar.js','r') as ff:
        text1=ff.read()

    if  'sanctuary'  in flow.request.url:
        flow.response.text = text.replace('qafGI3nhbgtfdlop',uuid)


    if 'marketing' in flow.request.url:
        flow.response.text = text1.replace('qafGI3nhbgtfdlop',uuid)

