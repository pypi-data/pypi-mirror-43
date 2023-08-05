import argparse
from getpass import getpass

import sys

from wxmp_cli.core.base import BaseCommand
from wxmp_cli.wx import mp1421140183, WxError, save_access_token


class Command(BaseCommand):
    def add_arguments(self, parser):
        """
        :type parser: argparse.ArgumentParser
        """
        parser.add_argument("appid", nargs="?", help="appid")
        parser.add_argument("secret", nargs="?", help="secret")

    def handle(self, *args, **options):
        appid = options["appid"]
        secret = options["secret"]
        if appid is None:
            appid = input("appid: ")
        if secret is None:
            secret = getpass("secret: ")

        try:
            data = mp1421140183.WxAuth(appid, secret).get_access_token()
            save_access_token(data)
        except WxError as e:
            self.stderr.write("%s: %s\n" % (e.err_code, e.err_msg))
            sys.exit(1)
