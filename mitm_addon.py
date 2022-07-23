from mitmproxy import http
from mitmproxy import ctx
from config import Config
from captcha import RuCaptcha, CapMonster
import json

class MitmHCaptcha:
    def __init__(self):
        pass

    def response(self, flow: http.HTTPFlow) -> None:
        if "https://hcaptcha.com/getcaptcha" in flow.request.pretty_url:
            ctx.log.info("HCaptcha")

            capmonster = CapMonster(apikey=Config.APIKEY_CAPMONSTER)
            solve_hcaptcha = capmonster.get_solve_hcaptcha(sitekey=Config.SITEKEY, url=Config.URL_PAGE)

            data = json.loads(flow.response.get_text())
            hcaptcha_c = data['c']
            new_data = """{"c": %s,"pass": true,"generated_pass_UUID": "%s","expiration": 120}""" % (json.dumps(hcaptcha_c), solve_hcaptcha)

            flow.response.text = new_data




addons = [MitmHCaptcha()]