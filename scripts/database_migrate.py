#!/usr/bin/env python
# coding: utf-8

import imp

from app import database
from configuration import Configuration
from migrate.versioning import api

version = api.db_version(Configuration.SQLALCHEMY_DATABASE_URI, Configuration.SQLALCHEMY_MIGRATE_REPO)
migration = Configuration.SQLALCHEMY_MIGRATE_REPO + ('/versions/%03d_migration.py' % (version + 1))
tmp_module = imp.new_module('old_model')
old_model = api.create_model(Configuration.SQLALCHEMY_DATABASE_URI, Configuration.SQLALCHEMY_MIGRATE_REPO)
exec (old_model, tmp_module.__dict__)
script = api.make_update_script_for_model(Configuration.SQLALCHEMY_DATABASE_URI, Configuration.SQLALCHEMY_MIGRATE_REPO,
                                          tmp_module.meta, database.metadata)
open(migration, "wt").write(script)
api.upgrade(Configuration.SQLALCHEMY_DATABASE_URI, Configuration.SQLALCHEMY_MIGRATE_REPO)
version = api.db_version(Configuration.SQLALCHEMY_DATABASE_URI, Configuration.SQLALCHEMY_MIGRATE_REPO)

print('# Migration created successfully')
print('# Migration saved as: ' + migration)
print('# Database version: ' + str(version))
