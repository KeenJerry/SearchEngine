from django.core.management.base import BaseCommand, CommandError
from SearchEngine.tools import TrieTree
import os
import json


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('path_to_term')

    def handle(self, *args, **options):

        list_dir = os.listdir(options["path_to_term"])  # 列出文件夹下所有的目录与文件
        for item in list_dir:
            path = os.path.join(options["path_to_term"], item)
            if os.path.isfile(path):
                file = open(path)
                dict = json.load(file)
                for key_term in dict:






