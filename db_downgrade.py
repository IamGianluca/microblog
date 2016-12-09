#!/home/gianluca/.virtualenvs/microblog/bin/python3

from migrate.versioning import api

from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO


version = api.db_version(url=SQLALCHEMY_DATABASE_URI,
                         repository=SQLALCHEMY_MIGRATE_REPO)
api.downgrade(url=SQLALCHEMY_DATABASE_URI,
              repository=SQLALCHEMY_MIGRATE_REPO,
              version=version - 1)
version = api.db_version(url=SQLALCHEMY_DATABASE_URI,
                         repository=SQLALCHEMY_MIGRATE_REPO)
print('Current database version: {}'.format(str(version)))
