#!/usr/bin/env python
# coding: utf-8

from configuration import Configuration
from migrate.versioning import api

version = api.db_version(Configuration.SQLALCHEMY_DATABASE_URI, Configuration.SQLALCHEMY_MIGRATE_REPO)
api.downgrade(Configuration.SQLALCHEMY_DATABASE_URI, Configuration.SQLALCHEMY_MIGRATE_REPO, version - 1)
version = api.db_version(Configuration.SQLALCHEMY_DATABASE_URI, Configuration.SQLALCHEMY_MIGRATE_REPO)

print('# Database version: ' + str(version))
