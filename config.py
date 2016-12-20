import os


# database settings
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = ''.join(['sqlite:///',
                                   os.path.join(basedir, 'app.db')])
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False

# security options
WTF_CSRF_ENABLED = True
SECRET_KEY = os.environ.get('MICROBLOG_SECRET')

# login format for OpenID providers
OPENID_PROVIDERS = [
    {'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id' },
    {'name': 'Yahoo', 'url': 'https://me.yahoo.com' },
    {'name': 'AOL', 'url': r'http://openid.aol.com/<username>' },
    {'name': 'Flickr', 'url': r'http://www.flickr.com/<username>' },
    {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}
]

# email server
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

# administrator list
ADMINS = [os.environ.get('ADMIN_MAIL_ADDRESS')]

# pagination
POST_PER_PAGE = 3

# whooshalchemy
WHOOSH_BASE = os.path.join(basedir, 'search.db')
MAX_SEARCH_RESULTS = 50
