from mitmproxy import ctx
import random
str=''.join(random.sample('zyxwvutsrqponmlkjihgfedcbaZYXWVUTSRQPONMLKJIHGFEDCBA',7))
def request(flow):
    if 'rooms' in flow.request.url:
        flow.request.cookies["hoteluuid"] = "FLPsul{}MnZ".format(str)

def response(flow):
   script='Object.defineProperties(navigator,{hardwareConcurrency:{get:() => 4}});Object.defineProperties(screen,{width:{get:() => 1280}};Object.defineProperties(screen,{height:{get:() => 800}};Object.defineProperties(colorDepth,{width:{get:() => 24}});Object.defineProperties(navigator,{platform:{get:() => "MacIntel"}});'

   if 'ubt/_mubt.min.js' in flow.request.url:
       flow.response.text =script+flow.response.text
   if not flow.response.status_code == 200:
       return
   html = flow.response.text
   html = html.replace('<head>', '<head><script>%s</script>' % script)
   flow.response.text = html