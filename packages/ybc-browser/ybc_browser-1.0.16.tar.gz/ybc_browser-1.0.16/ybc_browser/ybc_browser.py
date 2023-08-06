# coding=utf-8
import webbrowser
import pypinyin
import os
import sys
from ybc_exception import *

urls = {
    'baidu': 'http://www.baidu.com',
    'yuanfudao': 'http://yuanfudao.com',
    'xiaoyuan': 'http://www.yuanfudao.com/info/emojis',
    'sougou': 'http://www.sogou.com',
    'sanliuling': 'http://www.so.com',
    'shipin': 'http://v.qq.com',
    'youxi': 'http://www.4399.com',
    'yinyue': 'http://music.163.com',
    'donghua': 'http://child.iqiyi.com',
    'dianying': 'http://www.iqiyi.com/dianying/',
    'biancheng': 'https://python.yuanfudao.com/',
    'shuai': 'https://www.yuanfudao.com/tutor-ybc-course-api/fshow/king1.jpg',
    'bilibili': 'https://www.bilibili.com/',
    'duichenhuihua': 'http://weavesilk.com/',
    'diantai': 'http://www.qingting.fm/',
    'zhongguose': 'http://zhongguose.com',
    'jike': 'http://geektyper.com/',
    'tupiantexiao': 'https://photomosh.com/',
    'wenzitexiao': 'http://tholman.com/texter/',
    'yishusheji': 'http://huaban.com/',
    'sumiaoshangse': 'http://paintschainer.preferred.tech/index_zh.html',
    'shubiaogangqin': 'http://touchpianist.com/',
}

websites = {
    'baidu': 'http://www.baidu.com',
    'yuanfudao': 'http://yuanfudao.com',
    'xiaoyuan': 'http://www.yuanfudao.com/info/emojis',
    'sougou': 'http://www.sogou.com',
    'sanliuling': 'http://www.so.com',
    'shipin': 'http://v.qq.com',
    'youxi': 'http://www.4399.com',
    'yinyue': 'http://music.163.com',
    'donghua': 'http://child.iqiyi.com',
    'dianying': 'http://www.iqiyi.com/dianying/',
    'shuai': 'https://www.yuanfudao.com/tutor-ybc-course-api/fshow/king1.jpg',
    'bilibili': 'https://www.bilibili.com/',
    'duichenhuihua': 'http://weavesilk.com/',
    'diantai': 'http://www.qingting.fm/',
    'zhongguose': 'http://zhongguose.com',
    'jike': 'http://geektyper.com/',
    'tupiantexiao': 'https://photomosh.com/',
    'wenzitexiao': 'http://tholman.com/texter/',
    'yishusheji': 'http://huaban.com/',
    'sumiaoshangse': 'http://paintschainer.preferred.tech/index_zh.html',
    'shubiaogangqin': 'http://touchpianist.com/',
    'zhifa': 'https://www.typing.com/',
    'rumen': 'https://m.yuanfudao.com/lessons/groups/14898?groupName=%E7%8C%BF%E7%BC%96%E7%A8%8B%E5%85%A5%E9%97%A8%E7%8F%AD%0A&studyPhase=xiaoxue&redirectSingle=true&keyfrom=yfd-mkt-ybc-cxq-031805',
    'biancheng': 'https://m.yuanfudao.com/lessons/groups/14898?groupName=%E7%8C%BF%E7%BC%96%E7%A8%8B%E5%85%A5%E9%97%A8%E7%8F%AD%0A&studyPhase=xiaoxue&redirectSingle=true&keyfrom=yfd-mkt-ybc-cxq-031805'
}


def open_browser(text):
    """
    :param text: 希望打开的网页名称
    :return: 在浏览器中打开一个网页
    """
    error_msg = "'text'"
    if not isinstance(text, str):
        raise ParameterTypeError(function_name=sys._getframe().f_code.co_name, error_msg=error_msg)

    if not text:
        raise ParameterValueError(function_name=sys._getframe().f_code.co_name, error_msg=error_msg)

    res = ''.join(pypinyin.lazy_pinyin(text))

    url = str()
    for key in urls.keys():
        if res in key or key in res:
            url = urls[key]
            break
    if not url:
        print("没有识别到可执行的命令，必须使用已支持的语音命令")
        return -1
    try:
        return webbrowser.open_new_tab(url)
    except Exception as e:
        raise InternalError(e, 'ybc_browser')


def open_local_page(file_name):
    """
    :param file_name: 要打开的文件名称
    :return: 打开一个文件
    """
    error_msg = "'file_name'"
    if not isinstance(file_name, str):
        raise ParameterTypeError(function_name=sys._getframe().f_code.co_name, error_msg=error_msg)

    if not file_name:
        raise ParameterValueError(function_name=sys._getframe().f_code.co_name, error_msg=error_msg)
    try:
        file_path = os.path.abspath(file_name)
        local_url = 'file://' + file_path
        return webbrowser.open_new_tab(local_url)
    except Exception as e:
        raise InternalError(e, 'ybc_browser')


def website(text):
    """
    :param text: 希望返回网址的网站名称
    :return: 网站的网址
    """
    error_msg = "'text'"
    if not isinstance(text, str):
        raise ParameterTypeError(function_name=sys._getframe().f_code.co_name, error_msg=error_msg)

    if not text:
        raise ParameterValueError(function_name=sys._getframe().f_code.co_name, error_msg=error_msg)

    res = ''.join(pypinyin.lazy_pinyin(text))

    website = str()
    for key in websites.keys():
        if res in key or key in res:
            website = websites[key]
            break
    if not website:
        print("没有识别到可执行的命令，必须使用已支持的语音命令")
        return -1
    else:
        return website


def main():
    # open_local_page("1")
    print(website('编程'))


if __name__ == '__main__':
    main()
