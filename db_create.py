#!/home/gianluca/.virtualenvs/microblog/bin/python3

from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO
from app import db
import os.path


db.create_all()
if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
    api.create(repository=SQLALCHEMY_MIGRATE_REPO,
               name='database repository')
    api.version_control(url=SQLALCHEMY_DATABASE_URI,
                        repository=SQLALCHEMY_MIGRATE_REPO)
else:
    api.version_control(url=SQLALCHEMY_DATABASE_URI,
                        repository=SQLALCHEMY_MIGRATE_REPO,
                        version=api.version(SQLALCHEMY_MIGRATE_REPO))
