
import os
import re
import unicodedata

from google.appengine.ext.webapp.template import _swap_settings

from django import template
from django.template import loader

import config

BASE_DIR = os.path.dirname(__file__)

if config.options.get('template_dirs'):
    def mk_template_dir(base, path):
        return os.path.abspath(os.path.join(BASE_DIR, path))
    TEMPLATE_DIRS = [mk_template_dir(BASE_DIR, path) for path in config.options.get('template_dirs')]
else:
    TEMPLATE_DIRS = ['templates']


def slugify(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore')
    return re.sub('[^a-zA-Z0-9-]+', '-', s).strip('-')


def get_template_vals_defaults(template_vals=None):
    # todo: do I need a way in the config to add a big list of items to include?
    if template_vals is None:
        template_vals = {}
        
    template_vals.update({
        'STATIC_URL': config.options.get('static_url', '/static/'),
        'config': config,
        'devel': os.environ['SERVER_SOFTWARE'].startswith('Devel'),
    })
    return template_vals

def render_template(template_name, template_vals=None):
    """
    Purpose is to set up proper template directories, add the
    default items to template context and render the template.
    """
    template_vals = get_template_vals_defaults(template_vals)
    template_vals.update({'template_name': template_name})
    old_settings = _swap_settings({'TEMPLATE_DIRS': TEMPLATE_DIRS})
    try:
        tpl = loader.get_template(template_name)
        rendered = tpl.render(template.Context(template_vals))
    finally:
        _swap_settings(old_settings)
    return rendered

def ping_googlesitemap():
    from google.appengine.api import urlfetch
    google_url = 'http://www.google.com/webmasters/tools/ping?sitemap=http://' + config.options.get('host') + '/sitemap.xml.gz'
    response = urlfetch.fetch(google_url, '', urlfetch.GET)
    if response.status_code / 100 != 2:
        raise Warning("Google Sitemap ping failed", response.status_code, response.content)