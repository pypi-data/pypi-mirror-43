import requests

from wxmp_cli import wx


class WxUser(object):
    user_info_url = "%s%s" % (wx.WX_API_DOMAIN, wx.WX_USER_INFO_URI)

    def __init__(self, access_token):
        self.access_token = access_token

    def get_user(self, openid, lang="zh_CN"):
        params = {
            "access_token": self.access_token,
            "openid": openid,
            "lang": lang,
        }
        resp = requests.get(self.user_info_url, params=params)
        return wx.convert_resp_data(resp.json())
