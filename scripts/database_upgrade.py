#!/usr/bin/env python
# coding: utf-8

from configuration import Configuration
from migrate.versioning import api

api.upgrade(Configuration.SQLALCHEMY_DATABASE_URI, Configuration.SQLALCHEMY_MIGRATE_REPO)
version = api.db_version(Configuration.SQLALCHEMY_DATABASE_URI, Configuration.SQLALCHEMY_MIGRATE_REPO)

print('# Database version: ' + str(version))
