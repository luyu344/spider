from mitmproxy import ctx
import time
import hashlib
import os

md5=hashlib.md5()
time_text=(time.strftime('%Y-%m-%d')+'vps_24').encode('utf-8')
md5.update(time_text)
uuid='xDVG2'+md5.hexdigest()[:11]
# uuid='GPDNupX52pldVadM' # GPDNupX69pldVadM
# uuid='t9FgC0hOf101uSOd'
#xDVG2 xDVT3

# def request(flow):
#     if 'rooms' in flow.request.url:
#         flow.request.cookies["MKT_Pagesource"] = "H5"
#         flow.request.cookies["_abtest_userid"]="=469d3aa6-cd28-4b77-b851-9b11c2d7ad62"
#         flow.request.cookies["supportwebp"]="false"

def response(flow):
    # script='Object.defineProperties(navigator,{platform:{get:() => "iphone"}});Object.defineProperties(screen,{width:{get:() => 375}});Object.defineProperties(screen,{height:{get:() => 667}});Object.defineProperties(navigator,{colorDepth:{get:() => 32}});'
    # if 'ubt/_mubt.min.js' in flow.request.url:
    #    flow.response.text =script+flow.response.text
    # if not flow.response.status_code == 200:
    #    return
    # html = flow.response.text
    # html = html.replace('<head>', '<head><script>%s</script>' % script)
    # flow.response.text = html








    # script = """function breakOn(obj, propertyName, mode, func) {
    #     // this is directly from https://github.com/paulmillr/es6-shim
    #     function getPropertyDescriptor(obj, name) {
    #         var property = Object.getOwnPropertyDescriptor(obj, name);
    #         var proto = Object.getPrototypeOf(obj);
    #         while (property === undefined && proto !== null) {
    #             property = Object.getOwnPropertyDescriptor(proto, name);
    #             proto = Object.getPrototypeOf(proto);
    #         }
    #         return property;
    #     }
    #
    #     function verifyNotWritable() {
    #         if (mode !== 'read')
    #             throw "This property is not writable, so only possible mode is 'read'.";
    #     }
    #
    #     var enabled = true;
    #     var originalProperty = getPropertyDescriptor(obj, propertyName);
    #     var newProperty = { enumerable: originalProperty.enumerable };
    #
    #     // write
    #     if (originalProperty.set) {// accessor property
    #         newProperty.set = function(val) {
    #             if(String(val).indexOf('hoteluuid')>-1)
    #                   { debugger;originalProperty.set.call(this, val);}
    #               // { originalProperty.set.call(this,"hoteluuid=GPDNupX69pldVadM;path=/" );}
    #
    #          //   else if(String(val).indexOf('support')>-1)
    #            //     { originalProperty.set.call(this,"supportwebp=false;path=/" ); }
    #
    #
    #             else
    #             {originalProperty.set.call(this, val);}
    #         }
    #     } else if (originalProperty.writable) {// value property
    #         newProperty.set = function(val) {
    #             if(enabled && (!func || func && func(val)))
    #                { debugger;}
    #
    #             originalProperty.value = val;
    #         }
    #     } else  {
    #         verifyNotWritable();
    #     }
    #
    #     // read
    #     newProperty.get = function(val) {
    #           if(enabled && mode === 'read' && (!func || func && func(val)))
    #             debugger;
    #
    #         return originalProperty.get ? originalProperty.get.call(this, val) : originalProperty.value;
    #     }
    #
    #     Object.defineProperty(obj, propertyName, newProperty);
    #
    #     return {
    #       disable: function() {
    #         enabled = false;
    #       },
    #
    #       enable: function() {
    #         enabled = true;
    #       }
    #     };
    # };
    #     var bp = breakOn(document, 'cookie', false);"""
    # # 11  uuidkey
    # if not flow.response.status_code == 200:
    #     return
    # html = flow.response.text
    # html = html.replace('<head>', '<head><script>%s</script>' % script)
    # flow.response.text = html
    #


    with open(os.path.dirname(__file__)+'/san.js','r') as f:
        text=f.read()
    with open(os.path.dirname(__file__)+'/mar_.js','r') as ff:
        text1=ff.read()

    if  'sanctuary'  in flow.request.url:
        flow.response.text = text.replace('qafGI3nhbgtfdlop',uuid)


    if 'marketing' in flow.request.url:
        flow.response.text = text1.replace('qafGI3nhbgtfdlop',uuid)

