import json

import os

WX_API_DOMAIN = "https://api.weixin.qq.com"
# 获取access_token
WX_TOKEN_URI = "/cgi-bin/token"
# 创建标签
WX_TAGS_CREATE_URI = "/cgi-bin/tags/create"
# 获取公众号已创建的标签
WX_TAGS_GET_URI = "/cgi-bin/tags/get"
# 编辑标签
WX_TAGS_UPDATE_URI = "/cgi-bin/tags/update"
# 删除标签
WX_TAGS_DELETE_URI = "/cgi-bin/tags/delete"
# 获取标签下粉丝列表
WX_USER_TAG_GET_URI = "/cgi-bin/user/tag/get"
# 获取用户基本信息
WX_USER_INFO_URI = "/cgi-bin/user/info"

token_file = "%s/.wxmp-cli.json" % os.environ["HOME"]


class WxError(Exception):
    err_codes = {
        -1: "系统繁忙",
        0: "请求成功",
        40001: "AppSecret错误",
        40002: "请确保grant_type字段值为client_credential",
        40003: "传入非法的openid",
        40013: "AppID无效",
        40164: "调用接口的IP地址不在白名单中，请在接口IP白名单中进行设置",
        45056: "创建的标签数过多，请注意不能超过100个",
        45057: "该标签下粉丝数超过10w，不允许直接删除",
        45058: "不能修改0/1/2这三个系统默认保留的标签",
        45157: "标签名非法，请注意不能和其他标签重名",
        45158: "标签名长度超过30个字节",
        45159: "非法的tag_id",
    }

    def __init__(self, err_code="-1"):
        self.err_code = err_code
        self.err_msg = self.err_codes.get(err_code)


def save_access_token(data):
    text = json.dumps(data, indent="    ")
    with open(token_file, "w") as f:
        f.write(text)


def get_access_token():
    if not os.path.isfile(token_file):
        return ""
    with open(token_file, "r") as f:
        text = f.read()
        try:
            data = json.loads(text)
            return data.get("access_token", "")
        except:
            return ""


def convert_resp_data(resp_data):
    if "errcode" in resp_data.keys():
        raise WxError(resp_data["errcode"])
    else:
        return resp_data
