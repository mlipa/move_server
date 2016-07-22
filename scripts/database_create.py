#!/usr/bin/env python
# coding: utf-8

import os

from app import database
from configuration import Configuration
from migrate.versioning import api

database.create_all()

if not os.path.exists(Configuration.SQLALCHEMY_MIGRATE_REPO):
    api.create(Configuration.SQLALCHEMY_MIGRATE_REPO, 'database_repository')

api.version_control(Configuration.SQLALCHEMY_DATABASE_URI, Configuration.SQLALCHEMY_MIGRATE_REPO)
version = api.db_version(Configuration.SQLALCHEMY_DATABASE_URI, Configuration.SQLALCHEMY_MIGRATE_REPO)

print('# Database repository created successfully')
print('# Database version: ' + str(version))