#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import json
import requests
import logging

logging.basicConfig(level=logging.WARNING,
                    format='%(asctime)s - %(filename)s [line:%(lineno)d] - %(levelname)s: %(message)s')
# usage:
# logging.debug('this is a loggging debug message')
# logging.warning('this is loggging a warning message')
# logging.error('this is an loggging error message')
# logging.critical('this is a loggging critical message')

username = os.environ['USERNAME']       # 帐号
password = os.environ['PASSWORD']       # 密码MD5 32位(小写)
question_num = os.environ['QUESTION']   # 安全提问 参考下面
question_answer = os.environ['ANSWER']  # 安全提问答案
sckey = os.environ['SCKEY'] # 
sckeyurl = "https://sc.ftqq.com/" + sckey + ".send?text=summersec-t00ls-sign-success"

# 0 = 没有安全提问
# 1 = 母亲的名字
# 2 = 爷爷的名字
# 3 = 父亲出生的城市
# 4 = 您其中一位老师的名字
# 5 = 您个人计算机的型号
# 6 = 您最喜欢的餐馆名称
# 7 = 驾驶执照的最后四位数字


def t00ls_login(u_name, u_pass, q_num, q_ans):
    """
    t00ls 登录函数
    :param u_name: 用户名
    :param u_pass: 密码的 md5 值 32 位小写
    :param q_num: 安全提问类型
    :param q_ans: 安全提问答案
    :return: 签到要用的 hash 和 登录后的 Cookies
    """
    login_data = {
        'action': 'login',
        'username': u_name,
        'password': u_pass,
        'questionid': q_num,
        'answer': q_ans
    }
    response_login = requests.post('https://www.t00ls.net/login.json', data=login_data)
    response_login_json = json.loads(response_login.text)

    if response_login_json['status'] != 'success':
        return None
    else:
        logging.warning("用户: {0} 登入成功!".format(username))
        formhash = response_login_json['formhash']
        t00ls_cookies = response_login.cookies
        return formhash, t00ls_cookies


def t00ls_sign(t00ls_hash, t00ls_cookies):
    """
    t00ls 签到函数
    :param t00ls_hash: 签到要用的 hash
    :param t00ls_cookies: 登录后的 Cookies
    :return: 签到后的 JSON 数据
    """
    sign_data = {
        'formhash': t00ls_hash,
        'signsubmit': "true"
    }
    response_sign = requests.post('https://www.t00ls.net/ajax-sign.json', data=sign_data, cookies=t00ls_cookies)
    return json.loads(response_sign.text)


def main():
    response_login = t00ls_login(username, password, question_num, question_answer)
    if response_login:
        response_sign = t00ls_sign(response_login[0], response_login[1])
        if response_sign['status'] == 'success':
            requests.get(url=sckeyurl)
            logging.warning("签到成功")
        elif response_sign['message'] == 'alreadysign':
            logging.warning("今日已签到")
        else:
            logging.error("出现玄学问题了,签到失败")
            sys.exit(1)
    else:
        logging.error("登录失败,请检查输入资料是否正确")
        sys.exit(1)


if __name__ == '__main__':
    main()