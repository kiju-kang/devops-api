#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# deprecated

from flask import Flask, request, jsonify
from telegram import send_telegram_to


__author__ = 'KIJU KANG'

app = Flask(__name__)


@app.route('/api/v1/telegram', methods=['GET'])
def get_send_telegram_message():
    chat_id = request.args.get('chat_id')
    text = request.args.get('text')
    response = send_telegram_to(chat_id, text)
    print(response)
    return jsonify(response), 200


@app.route('/api/v1/telegram', methods=['POST'])
def post_send_telegram_message():
    chat_id = request.form.get('chat_id')
    text = request.form.get('text')
    response = send_telegram_to(chat_id, text)
    print(response)
    return jsonify(response), 200


if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", port=8880)
