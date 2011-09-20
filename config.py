
from os.path import abspath, dirname, join

# Configuration file... just a regular python file.
PARENT_DIR = dirname(__file__)

options = dict(
    host = 'www.homebeforedark.org',

    event_path_format = "%(year)s/%(month)s/%(slug)s",


    Jinja2 = {
        'template_path': [
            abspath(join(PARENT_DIR, 'templates')),
            abspath(join(PARENT_DIR, 'events', 'templates')),
        ],
        'environment_args': {
            'autoescape': False,
        },
        
        'globals': {
            'STATIC_URL': '/static/',
        }
    }
)








