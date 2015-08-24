#!/usr/bin/python3

####################################################################
#
# This script gets a list of upcoming events via the Meetup API and
# updates the contents in _includes/upcoming.html accordingly.
#
####################################################################

import datetime
import os
import requests
import string
import sys

num_events = 5

api_call = 'https://api.meetup.com/2/events?offset=0&format=json&limited_events=False&group_urlname=Code-for-Tuscaloosa&page=200&fields=&order=time&desc=false&status=upcoming&sig_id=142197972&sig=30469a8bbe49fb53a9dacdfe8f9f6485a047a9d2'
script_path = os.path.dirname(os.path.realpath(__file__))
include_path = os.path.dirname(script_path) + '/_includes/upcoming.html'

try:

    r = requests.get(api_call)

    events = r.json()['results']

    event_template = string.Template('''    <li>
        <a href="$url"
           onclick="trackOutboundLink('$url'); return false;">
            $date $name
        </a>
    </li>\n''')

    html = '<ul>\n'

    for event in events[0:(num_events-1)]:
        url = event['event_url']
        date = datetime.datetime.utcfromtimestamp(event['time'] / 1000.0).strftime('%b %d')
        name = event['name']
        html += event_template.substitute(url=url, date=date, name=name)

    html += '</ul>\n'

    include = open(include_path, 'w')
    include.write(html)
    include.close()

    print('Ready to commit!')

except:
    print(sys.exc_info(), file=sys.stderr)
    sys.exit(1)
