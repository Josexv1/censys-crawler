#!/usr/bin/env python3
import json
import requests
import ast
from sys import argv
from pkgutil import simplegeneric

def t_print(field, array):
    try:
        print('[+][%s]: %s' % (field, array[field]))
    except:
        pass
# Function to clean \n \r
@simplegeneric
def get_items(obj):
    while False:  # no items, a scalar object
        yield None

@get_items.register(dict)
def _(obj):
    return obj.iteritems()  # json object

@get_items.register(list)
def _(obj):
    return enumerate(obj)  # json array

def strip_whitespace(json_data):
    for key, value in get_items(json_data):
        if hasattr(value, 'strip'):  # json string
            json_data[key] = value.strip()
        else:
            strip_whitespace(value)  # recursive call

# API Credentials
#   * https://censys.io/account
API_URL = "https://www.censys.io/api/v1/search/ipv4"
API_ID = "YOUR KEY"
SECRET = "YOUR KEy"


header_query = {
    'Content-type':'application/json', 'Accept': 'text/plain','User-Agent':'Mozilla/5.0 Gecko/20100101 Firefox/43.0'
                }

try:

    qry = (argv[1]).strip()
    for r in range(int(argv[2])):

        # The Search API
        #   * https://censys.io/api/v1/docs/search

        # Search Syntax
        #   * https://censys.io/ipv4/help

        data = {
                "query":("%s" % qry), "page":(r+1),
                "fields":
                    [
                        'ip',
                        'location.country',

                        '80.http.get.title.raw',
                        '80.http.get.headers.server',

                        '22.ssh.banner.raw_banner',
                        '22.ssh.banner.software_version',
                        '22.ssh.banner.metadata.product',
                        '22.ssh.banner.metadata.description',

                        '21.ftp.banner.banner',
                        '21.ftp.banner.metadata.manufacturer',
                        '21.ftp.banner.metadata.version',

                    ]
                }

        r = requests.post(API_URL, auth=(API_ID, SECRET), data=json.dumps(data), headers=header_query)
        #rst = json.loads((r.content).decode())
        rst = ast.literal_eval((r.content).decode())
        strip_whitespace(rst)

        for n in rst['results']:
            t_print('ip', n)
            t_print('location.country', n)
            t_print('80.http.get.title.raw', n)
            t_print('80.http.get.headers.server', n)
            t_print('22.ssh.banner.raw_banner', n)
            t_print('22.ssh.banner.software_version', n)
            t_print('22.ssh.banner.metadata.product', n)
            t_print('22.ssh.banner.metadata.description', n)
            t_print('21.ftp.banner.banner', n)
            t_print('21.ftp.banner.metadata.manufacturer', n)
            t_print('21.ftp.banner.metadata.version', n)
            print('%s\n' % ('#'*92)) #92 is my console width

except Exception as err:
    print(err)
