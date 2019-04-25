#!/usr/bin/python3

import requests
import json
from utils import Util
from group import Group


class Client:
    def __init__(self, token):
        self.util = Util(token)

    def list_groups(self):
        groups = [None]
        params = {'page':1, 'per_page':10}
        while groups:
            groups = self.util.ask_for('/groups',params)
            yield groups
            params['page'] += 1


    def search_groups_by_name(self, search):
        current = []
        for group_list in self.list_groups():
            for group in group_list:
                if search.strip().lower() in group['name'].strip().lower():
                    current.append(Group(group['name'], group['group_id']))
                    if len(current) == 10:
                        yield current
                        current = []
        yield current
    
