#!/home/gianluca/.virtualenvs/microblog/bin/python3

import os

import imp
from migrate.versioning import api

from app import db
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO


old_version = api.db_version(url=SQLALCHEMY_DATABASE_URI,
                         repository=SQLALCHEMY_MIGRATE_REPO)
version = str(old_version + 1).zfill(3)
migration = os.path.join(SQLALCHEMY_MIGRATE_REPO,
                         'versions/{}_migration.py'.format(version))
tmp_module = imp.new_module('old_model')
old_model = api.create_model(url=SQLALCHEMY_DATABASE_URI,
                             repository=SQLALCHEMY_MIGRATE_REPO)
exec(old_model, tmp_module.__dict__)

# create a migration script comparing the db structure (obtained from 'app.db')
# against the structure of our models (obtained from `app/models.py')
script = api.make_update_script_for_model(url=SQLALCHEMY_DATABASE_URI,
                                          repository=SQLALCHEMY_MIGRATE_REPO,
                                          oldmodel=tmp_module.meta,
                                          model=db.metadata)
open(migration, 'wt').write(script)
api.upgrade(url=SQLALCHEMY_DATABASE_URI, repository=SQLALCHEMY_MIGRATE_REPO)
new_version = api.db_version(url=SQLALCHEMY_DATABASE_URI,
                         repository=SQLALCHEMY_MIGRATE_REPO)
print('New migration saved as {}'.format(migration))
print('Current database version: {}'.format(str(new_version)))
