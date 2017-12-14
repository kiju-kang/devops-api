#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import ast
import errno
import sys
import time
import redis
from os import strerror
from cloud_flare import cf_block_ip, cf_search_ip, cf_release_ip
from properties import REDIS_HOST, REDIS_PORT
from telegram import SYSTEM_CHAT_ID, LABS_CHAT_ID, send_telegram_labs, send_telegram_to


__author__ = 'KIJU KANG'

except_io_error = "I/O error({0}): {1}".format(errno, strerror)
except_value_error = "Could not convert data to an integer."
except_unexpected_error = "Unexpected error:", sys.exc_info()[0]


class RedisHandler:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.r = redis.StrictRedis(host=self.host, port=self.port, db=0)

    # member 가 존재하는지 조회
    def has_key(self, chat_id):
        print('hasKey: {}'.format(chat_id))
        return self.r.srandmember(chat_id)

    def read(self, chat_id):
        # chat_id key로 member를 꺼낸 후 member 는 집합에서 삭제후 redis_response에 결과값 저장
        redis_response = self.r.spop(chat_id)
        decode_redis_result = redis_response.decode('utf-8')
        # 결과값 문자열을 dict 로 변환
        return ast.literal_eval(decode_redis_result)

    def block(self, ip, chat_id):
        print('block: {}'.format(chat_id))
        # ip 파라메타로 cf_block_ip 함수 호출 후 block_result 에 결과값 저장
        block_result = cf_block_ip(ip)
        # cf_block_ip response 가 success 이면
        if block_result['success']:
            return self.blocked_message(ip)
        # cf_block_ip response 가 error 이면
        else:
            error = block_result['errors']
            error_reason = ('Call to cf api failed. {}'.format(error))
            return 'Block result = {}'.format(error_reason)

    def search(self, ip, chat_id):
        print('search: {}'.format(chat_id))
        search_result = cf_search_ip(ip)
        if search_result['result_info']['count'] >= 1:
            return self.search_blocked_message(ip)
        else:
            return self.search_unblocked_message(ip)

    def release(self, ip, chat_id):
        print('release: {}'.format(chat_id))
        search_result = cf_search_ip(ip)

        if search_result['result_info']['count'] >= 1:
            release_id = search_result['result'][0]['id']
            release_result = cf_release_ip(release_id)
            cf_release_ip(release_result)
            return self.release_message(ip)
        elif not search_result['result']:
            return self.search_unblocked_message(ip)
        else:
            error = search_result['errors']
            error_reason = ('Call to cf api failed. {}'.format(error))
            return 'Release result = ' + error_reason

    def telegram_api_send_message(self, chat_id, text):
        telegram_result = send_telegram_to(chat_id, text)
        if telegram_result['ok']:
            return self.telegram_send_message(text)
        else:
            error = telegram_result['errors']
            error_reason = ('Call to telegram api failed. {}'.format(error))
            return 'send_message result = {}'.format(error_reason)

    @staticmethod
    def search_blocked_message(ip):
        return 'Search result = ip {} 는 차단 되었습니다..'.format(ip)

    @staticmethod
    def search_unblocked_message(ip):
        return 'Search result = ip {} 는 차단 되지 않았습니다..'.format(ip)

    @staticmethod
    def blocked_message(ip):
        return 'Block result = {} blocked by devops_internal_api'.format(ip)

    @staticmethod
    def release_message(ip):
        return 'Release result = ip {} 차단 해제 되었습니다..'.format(ip)

    @staticmethod
    def telegram_send_message(text):
        return 'telegram send_message result = "{}" telegram message 정상 발송 되었습니다.'.format(text)


def redis_enhanced():
    handler = RedisHandler(REDIS_HOST, REDIS_PORT)
    key_list = [LABS_CHAT_ID, SYSTEM_CHAT_ID]

    while True:
        try:
            for chat_id in key_list:
                if handler.has_key(chat_id):
                    resp = handler.read(chat_id)
                    if 'ip' in resp:
                        ip = resp['ip']
                    elif 'text' in resp:
                        text = resp['text']
                        if resp['action'] == 'block':
                            send_message = handler.block(ip, chat_id)
                        elif resp['action'] == 'release':
                            send_message = handler.release(ip, chat_id)
                        elif resp['action'] == 'telegram_send_message':
                            send_message = handler.telegram_api_send_message(chat_id, text)
                        else:
                            send_message = handler.search(ip, chat_id)
                        send_telegram_to(chat_id=chat_id, text=send_message)

                else:
                    print("----------------------")
                    time.sleep(1)
        except IOError:
            send_telegram_labs(text=except_io_error + 'by devops-internal-api')
        except ValueError:
            send_telegram_labs(text=except_value_error + 'by devops-internal-api')
        except:
            send_telegram_labs(text=except_unexpected_error + 'by devops-internal-api')
            raise


redis_enhanced()
