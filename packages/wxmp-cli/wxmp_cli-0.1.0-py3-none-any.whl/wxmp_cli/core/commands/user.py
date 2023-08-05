import json
import sys

from wxmp_cli.core.base import BaseCommand
from wxmp_cli.wx import get_access_token, mp1421140839, WxError, mp1421140837


class Command(BaseCommand):
    def add_arguments(self, parser):
        """
        :type parser: argparse.ArgumentParser
        """
        parser.add_argument("--access-token", help="access_token")
        parser.add_argument("--openid", help="openid")
        parser.add_argument("--tagid", help="tagid")
        parser.add_argument("--output-fmt", default="csv", choices=["csv"],
                            help="output format")

    def handle(self, *args, **options):
        access_token = options["access_token"] or get_access_token()
        if not access_token:
            self.stderr.write("Cannot load access_token.")
            sys.exit(1)
        options["access_token"] = access_token

        try:
            if options["openid"] is not None:
                self.get_user(**options)
            elif options["tagid"] is not None:
                self.get_users_by_tag(**options)
        except WxError as e:
            self.stderr.write("%s: %s\n" % (e.err_code, e.err_msg))
            sys.exit(1)

    def get_user(self, **options):
        wx_user = mp1421140839.WxUser(options["access_token"])
        data = wx_user.get_user(options["openid"])
        self.stdout.write(json.dumps(data, indent="    ") + "\n")

    def get_users_by_tag(self, **options):
        try:
            users = mp1421140837.WxTags(options["access_token"]).get_users(
                options["tagid"])
            wx_user = mp1421140839.WxUser(options["access_token"])
            self._print_head()
            for openid in users["data"]["openid"]:
                user = wx_user.get_user(openid)
                self._print_user(user)
        except WxError as e:
            self.stderr.write("%s: %s\n" % (e.err_code, e.err_msg))
            sys.exit(1)

    def _print_head(self):
        heads = [
            "unionid",
            "openid",
            "nickname",
            "sex",
            "country",
            "province",
            "city",
            "headimgurl",
            "remark",
        ]
        self.stdout.write(",".join(heads) + "\n")

    def _print_user(self, user):
        info = [
            user["unionid"],
            user["openid"],
            user["nickname"],
            ("", "男", "女")[user["sex"]],
            user["country"],
            user["province"],
            user["city"],
            user["headimgurl"],
            user["remark"],
        ]
        self.stdout.write(",".join(info) + "\n")
