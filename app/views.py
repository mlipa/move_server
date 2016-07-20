#!/usr/bin/env python
# coding: utf-8

from app import application
from flask import render_template


@application.route('/')
def home():
    return render_template('base.html')
