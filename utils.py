
import os
import re
import unicodedata

import webapp2
from webapp2_extras import jinja2

import config

def is_devel():
    return os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')

def jinja2_factory(app):
    j = jinja2.Jinja2(app, config.options['Jinja2'])

    j.environment.filters.update({
        # Set filters.
        # ...
    })
    j.environment.globals.update({
        # Set global variables.
        'uri_for': webapp2.uri_for,
        'request': app.request,
        'config': config,
        'devel': os.environ['SERVER_SOFTWARE'].startswith('Devel'),
    })
    return j


def slugify(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore')
    return re.sub('[^a-zA-Z0-9-]+', '-', s).strip('-').lower()

def intget(val, default=None):
    try:
        return int(val)
    except ValueError:
        return default

def ping_googlesitemap():
    from google.appengine.api import urlfetch
    google_url = 'http://www.google.com/webmasters/tools/ping?sitemap=http://' + config.options.get('host') + '/sitemap.xml.gz'
    response = urlfetch.fetch(google_url, '', urlfetch.GET)
    if response.status_code / 100 != 2:
        raise Warning("Google Sitemap ping failed", response.status_code, response.content)
