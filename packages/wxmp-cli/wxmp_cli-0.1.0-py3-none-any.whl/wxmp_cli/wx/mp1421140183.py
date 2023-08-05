import requests

from wxmp_cli import wx


class WxAuth(object):
    wx_token_url = "%s%s" % (wx.WX_API_DOMAIN, wx.WX_TOKEN_URI)

    def __init__(self, appid, secret):
        self.appid = appid
        self.secret = secret

    def get_access_token(self):
        params = {
            "grant_type": "client_credential",
            "appid": self.appid,
            "secret": self.secret,
        }
        resp = requests.get(self.wx_token_url, params=params)
        return wx.convert_resp_data(resp.json())
