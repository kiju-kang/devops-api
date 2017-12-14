#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import json
import requests


__author__ = 'KIJU KANG'

CF_AUTH_KEY = ''
CF_AUTH_EMAIL = 'kiju.kang@naver.com'
CF_ZONE_ID = ''

CF_HEADERS = {'X-auth-Email': '{}'.format(CF_AUTH_EMAIL),
              'X-Auth-Key': '{}'.format(CF_AUTH_KEY),
              'Content-Type': 'application/json'}


def cf_block_ip(ip):
    data = {"mode": "block", "configuration": {"target": "ip", "value": "{}".format(ip)},
            "notes": "Blocked by devops_internal_api"}

    return requests.post(
        url='https://api.cloudflare.com/client/v4/zones/{}/firewall/access_rules/rules'.format(CF_ZONE_ID),
        headers=CF_HEADERS,
        data=json.dumps(data),
        timeout=10
    ).json()


def cf_search_ip(ip):
    return requests.get(
        url='https://api.cloudflare.com/client/v4/zones/{0}/firewall/access_rules/'
            'rules?scope_type=zone&mode=block&configuration_target=ip&configuration_value={1}&'
            'page=1&per_page=50&order=scope_type&direction=desc&match=all"'.format(CF_ZONE_ID, ip),
        headers=CF_HEADERS,
        timeout=10
    ).json()


def cf_release_ip(release_id):
    data = {"cascade": "none"}
    return requests.delete(
        url='https://api.cloudflare.com/client/v4/zones/{0}/firewall/access_rules/rules/{1}'.format(CF_ZONE_ID, release_id),
        headers=CF_HEADERS,
        data=json.dumps(data),
        timeout=10
    ).json()
