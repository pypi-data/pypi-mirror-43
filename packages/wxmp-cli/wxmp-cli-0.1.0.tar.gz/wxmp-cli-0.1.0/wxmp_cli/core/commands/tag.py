import argparse
import json

import sys

from wxmp_cli.core.base import BaseCommand
from wxmp_cli.wx import mp1421140837, get_access_token, WxError


class Command(BaseCommand):
    def add_arguments(self, parser):
        """
        :type parser: argparse.ArgumentParser
        """
        parser.add_argument(
            "-X", default="GET",
            choices=["GET"],
            help="default: GET")
        parser.add_argument("--access-token", help="access_token")
        parser.add_argument("--tagid", help="tagid")
        parser.add_argument("--name", "--tag-name", dest="tag_name",
                            help="tag name")

    def handle(self, *args, **options):
        access_token = options["access_token"] or get_access_token()
        if not access_token:
            self.stderr.write("Cannot load access_token.")
            sys.exit(1)
        options["access_token"] = access_token

        try:
            if options["X"] == "GET":
                self.get_tags(**options)
            elif options["X"] == "CREATE":
                self.create_tag(**options)
            elif options["X"] == "UPDATE":
                self.update_tag(**options)
            elif options["X"] == "DELETE":
                self.delete_tag(**options)
        except WxError as e:
            self.stderr.write("%s: %s\n" % (e.err_code, e.err_msg))
            sys.exit(1)

    def get_tags(self, **options):
        wx_tags = mp1421140837.WxTags(options["access_token"])
        data = wx_tags.get_tags()
        self.stdout.write(json.dumps(data, indent="    ") + "\n")

    def create_tag(self, **options):
        pass

    def update_tag(self, **options):
        pass

    def delete_tag(self, **options):
        pass
