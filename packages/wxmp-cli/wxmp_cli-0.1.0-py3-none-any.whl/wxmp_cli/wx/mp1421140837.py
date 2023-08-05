import requests

from wxmp_cli import wx


class WxTags(object):
    tag_get_url = "%s%s" % (wx.WX_API_DOMAIN, wx.WX_TAGS_GET_URI)
    get_users_url = "%s%s" % (wx.WX_API_DOMAIN, wx.WX_USER_TAG_GET_URI)

    def __init__(self, access_token):
        self.access_token = access_token

    def create_tag(self):
        pass

    def get_tags(self):
        params = {"access_token": self.access_token}
        resp = requests.get(self.tag_get_url, params=params)
        return wx.convert_resp_data(resp.json())

    def update_tag(self):
        pass

    def delete_tag(self):
        pass

    def get_users(self, tagid="", next_openid=""):
        params = {"access_token": self.access_token}
        data = {
            "tagid": tagid,
            "next_openid": next_openid,
        }
        resp = requests.post(self.get_users_url, params=params, json=data)
        return wx.convert_resp_data(resp.json())
