
# Configuration file... just a regular python file.
options = dict(
    host = 'www.homebeforedark.org',

    static_url = '/static/',

    event_path_format = "%(year)s/%(month)s/%(slug)s/",

    # enter template dirs relative to this config file
    template_dirs = (
        'events/templates',
        'templates',
    ),
)








