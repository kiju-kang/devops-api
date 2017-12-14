#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import requests


__author__ = 'KIJU KANG'

# ALARM_BOT_TOKEN = '' -- deprecated
GenieGenieWorldBot_BOT_TOKEN = ''
SYSTEM_CHAT_ID = ''
LABS_CHAT_ID = ''


def send_telegram(bot_token, chat_id, text):
    print('chat_id: {} / text: {}'.format(chat_id, text))
    return requests.post(
        url='https://api.telegram.org/bot{0}/sendMessage'.format(bot_token),
        data={'chat_id': '{}'.format(chat_id), 'text': '{}'.format(text)},
        timeout=10
    ).json()


def send_telegram_to(chat_id, text):
    return send_telegram(bot_token=GenieGenieWorldBot_BOT_TOKEN, chat_id=chat_id, text=text)


def send_telegram_labs(text):
    return send_telegram_to(chat_id=GenieGenieWorldBot_BOT_TOKEN, text=text)


def send_telegram_system(text):
    return send_telegram_to(chat_id=GenieGenieWorldBot_BOT_TOKEN, text=text)
