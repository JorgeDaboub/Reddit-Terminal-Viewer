#!/usr/bin/env python3
import os
import sys

import requests
import pprint
import re

# Constants

ISGD_URL = 'http://is.gd/create.php'

# Functions

def usage(status=0):
    ''' Display usage information and exit with specified status '''
    print('''Usage: {} [options] URL_OR_SUBREDDIT

    -s          Shorten URLs using (default: False)
    -n LIMIT    Number of articles to display (default: 10)
    -o ORDERBY  Field to sort articles by (default: score)
    -t TITLELEN Truncate title to specified length (default: 60)
    '''.format(os.path.basename(sys.argv[0])))
    sys.exit(status)

def load_reddit_data(url):
    ''' Load reddit data from specified URL into dictionary

    >>> len(load_reddit_data('https://reddit.com/r/nba/.json'))
    27

    >>> load_reddit_data('linux')[0]['data']['subreddit']
    'linux'
    '''
    # TODO: Verify url parameter (if it starts with http, then use it,
    # otherwise assume it is just a subreddit).
    if url[:4] != 'http':
        url = 'https://www.reddit.com/r/' + url + '/.json'
    headers = {'user-agent': 'reddit-{}'.format(os.environ.get('USER', 'cse-20289-sp20'))}
    response = requests.get(url, headers=headers)
    data = response.json()
    data = data['data']['children']
    
    return data

def shorten_url(url):
    ''' Shorten URL using is.gd service

    >>> shorten_url('https://reddit.com/r/aoe2')
    'https://is.gd/dL5bBZ'

    >>> shorten_url('https://cse.nd.edu')
    'https://is.gd/3gwUc8'
    '''
    # TODO: Make request to is.gd service to generate shortened url.
    response = requests.get(ISGD_URL, params={'format': 'json', 'url': url})
    shorten = response.json()
    
    return shorten['shorturl']


def print_reddit_data(data, limit=10, orderby='score', titlelen=60, shorten=False):
    ''' Dump reddit data based on specified attributes '''
    # TODO: Sort articles stored in data list by the orderby key, and then
    # print out each article's index, title, score, and url using the following
    # format:
    #
    #   print(f'{index:4}.\t{title} (Score: {score})\n\t{url}')
    #
    # Note: Trim or modify the output based on the keyword arguments to the function.
    if orderby != 'score':
        articles = sorted(data, key=lambda i: i['data'][orderby])
    else:
        articles = sorted(data, key=lambda i: i['data']['score'], reverse=True)

    for i in range(0, limit):
        if i in range(1,limit):
            print()

        if len(articles[i]['data']['title']) > titlelen:
            title = articles[i]['data']['title'][:titlelen]
        else:
            title = articles[i]['data']['title']

        if shorten:
            url = shorten_url(articles[i]['data']['url'])
        else:
            url = articles[i]['data']['url']

        score = articles[i]['data']['score']
        index = i + 1

        print(f"{index:4}.\t{title} (Score: {score})\n\t{url}")
    pass

def main():
    # TODO: Parse command line arguments
    arguments = sys.argv[1:]
    url       = None
    limit     = 10
    orderby   = 'score'
    titlelen  = 60
    shorten   = False

    if len(arguments) == 0:
        usage()
    
    while len(arguments) != 0:   
        temp = arguments.pop(0)
        if temp == '-s':
            shorten = True
        elif temp == '-n':
            try:
                limit = int(arguments.pop(0))
            except ValueError:
                print("Non interger limit entered.")
                usage()
        elif temp == '-o':
            orderby = arguments.pop(0)
        elif temp == '-t':
            try:
                titlelen = int(arguments.pop(0))
            except ValueError:
                print("Non interger title length entered.")
                usage()
        elif temp == '-h':
            usage()
        elif len(arguments) > 0:
            usage()

    url = temp

    # print(arguments)
    # print(url)
    # print(limit)
    # print(orderby)
    # print(titlelen)
    # print(shorten)

    # TODO: Load data from url and then print the data
    data = load_reddit_data(url)

    print_reddit_data(data,limit, orderby, titlelen, shorten)
   
    pass

# Main Execution

if __name__ == '__main__':
    main()

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
