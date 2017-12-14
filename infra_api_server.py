#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import redis
from flask import Flask, jsonify, request
import socket


__author__ = 'KIJU KANG'

app = Flask(__name__)

duplicate_job_message = "The job is a duplicate request."
r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)


@app.route('/api/v1/cf/block', methods=['POST'])
def block_ip():
    ip = request.form.get('ip')
    chat_id = request.form.get('chat_id')
    block_job = {"action": "block", "ip": "{}".format(ip)}

    try:
        # ip address 형식인지 검사
        socket.inet_aton(ip)
        # chat_id 파라메타가 없을 경우 444 code return
        if request.form.get('chat_id') is None:
            return jsonify('invalid chat_id or invalid parameter'), 444
        # 중복된 job 이 있는지 검사 후 중복일경우 333 code return
        elif r.sismember('{}'.format(chat_id), '{}'.format(block_job)):
            return jsonify(duplicate_job_message), 333
        # chat_id 파라메타가 있고 중복된 jobs이 없을경우 member 추가 후 200 code return
        else:
            r.sadd('{}'.format(chat_id), '{}'.format(block_job))
            return jsonify('successfully received the block request of ip {}.'.format(ip)), 200
    # ip address 형식이 잘못 되었을 경우 445 code return
    except socket.error:
        return jsonify('invalid ip address'), 445


@app.route('/api/v1/cf/search', methods=['GET'])
def search_ip():
    ip = request.args.get('ip')
    chat_id = request.args.get('chat_id')
    search_job = {"action": "search", "ip": "{}".format(ip)}

    try:
        socket.inet_aton(ip)
        if request.args.get('chat_id') is None:
            return jsonify('invalid chat_id or invalid parameter'), 444
        elif r.sismember('{}'.format(chat_id), '{}'.format(search_job)):
            return jsonify(duplicate_job_message), 333
        else:
            r.sadd('{}'.format(chat_id), '{}'.format(search_job))
            return jsonify('successfully received the search request of ip {}.'.format(ip)), 200
    except socket.error:
        return jsonify('invalid ip address'), 445


@app.route('/api/v1/cf/release', methods=['POST'])
def release_ip():
    ip = request.form.get('ip')
    chat_id = request.form.get('chat_id')
    release_job = {"action": "release", "ip": "{}".format(ip)}

    try:
        socket.inet_aton(ip)
        if request.form.get('chat_id') is None:
            return jsonify('invalid chat_id or invalid parameter'), 444
        elif r.sismember('{}'.format(chat_id), '{}'.format(release_job)):
            return jsonify(duplicate_job_message), 333
        else:
            r.sadd('{}'.format(chat_id), '{}'.format(release_job))
            return jsonify('successfully received the release request of ip {}.'.format(ip)), 200
    except socket.error:
        return jsonify('invalid ip address'), 445


@app.route('/api/v1/telegram', methods=['GET'])
def get_send_telegram_message():
    chat_id = request.args.get('chat_id')
    text = request.args.get('text')
    telegram_job = {"action": "telegram_send_message", "text": "{}".format(text)}
    # chat_id 파라메타 값이 없을경우
    if request.args.get('chat_id') is None:
        return jsonify('invalid chat_id or invalid parameter'), 444
    # text 파라메타 값이 없을경우
    if request.args.get('text') is None:
        return jsonify('invalid text or invalid parameter'), 444
    # 중복된 job 이 있을 경우 333 code return
    elif r.sismember('{}'.format(chat_id), '{}'.format(text)):
        return jsonify(duplicate_job_message), 333
    # 정상적인 요청일 경우 key에 chat_id, value에 telegram_job member 추가
    else:
        r.sadd('{}'.format(chat_id), '{}'.format(telegram_job))
        return jsonify('successfully received the telegram send message request'), 200


if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", port=8080)

    # CF BLOCK IP
    # url = http://192.168.100.194:8080/v1/cf/block
    # method = Post
    # Key = ip  , value = ip address (ex. 1.1.1.1)
    # Key = chat_id , value = chat id num (ex. -123456789)
    # run server
    # nohup python -u infra_api_server.py &

    # CF CHECK IP
    # url = http://192.168.100.194:8080/v1/cf/serach
    # method = Post
    # Key = ip , value = ip address (ex. 1.1.1.1)
    # Key = chat_id , value = chat id num (ex. -1234687)
    # run server
    # nohup python -u infra_api_server.py &

    # CF RELEASE IP
    # url = http://192.168.100.194:8080/v1/cf/release
    # method = Post
    # Key = ip , value = ip address (ex. 1.1.1.1)
    # Key = chat_id , value = chat id num (ex. -123467)
    # run server
    # nohup python -u infra_api_server.py &
