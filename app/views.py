# -*- coding: utf-8 -*-
import os
import json
import time

import arrow
import tablib
from flask import g, request, make_response, jsonify, abort

from . import db, app, cache, logger, access_logger
#from .models import *
from . import helper


@app.route('/')
def index_get():
    result = {
        'exp': '%sexp' % (request.url_root)
    }
    header = {'Cache-Control': 'public, max-age=600'}
    return jsonify(result), 200, header

@app.route('/exp', methods=['POST'])
def export_post():
    if not request.json:
        return jsonify({'message': 'Problems parsing JSON'}), 415
    try:
        type = request.json.get('type', 'xlsx')
        data = tablib.Dataset(headers=request.json['headers'])
        for i in request.json['datas']:
            data.append(i)
        now = arrow.now('PRC').format('YYYYMMDD')
        name = '{0}/{1}/{2}.{3}'.format(app.config['BASE_PATH'], now, request.json['title'], type)
        path = '{0}/{1}'.format(app.config['BASE_PATH'], now)
        if not os.path.isdir(path):
            os.makedirs(path)
        with open(name.encode('utf-8'), 'wb') as f:
            f.write(data.export(type))
    except Exception as e:
        logger.exception(e)
        raise
    return jsonify({'path': '{0}/{1}/{2}.{3}'.format(app.config['BASE_URL_PATH'], now, request.json['title'], type)}), 201
