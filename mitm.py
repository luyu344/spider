from mitmproxy import ctx
import time
import hashlib
import os

md5=hashlib.md5()
time_text=(time.strftime('%Y-%m-%d')+'vps_24').encode('utf-8')
md5.update(time_text)
uuid='xDVT3'+md5.hexdigest()[:11]
# uuid='t9FgC0hOf101uSOd'
#xDVG2 xDVT3

def request(flow):
    if 'rooms' in flow.request.url:
        flow.request.cookies["MKT_Pagesource"] = "H5"
        flow.request.cookies["_abtest_userid"]="=469d3aa6-cd28-4b77-b851-9b11c2d7ad62"
        flow.request.cookies["supportwebp"]="false"

def response(flow):
    with open(os.path.dirname(__file__)+'/san.js','r') as f:
        text=f.read()
    with open(os.path.dirname(__file__)+'/mar.js','r') as ff:
        text1=ff.read()

    if  'sanctuary'  in flow.request.url:
        flow.response.text = text.replace('qafGI3nhbgtfdlop',uuid)


    if 'marketing' in flow.request.url:
        flow.response.text = text1.replace('qafGI3nhbgtfdlop',uuid)

