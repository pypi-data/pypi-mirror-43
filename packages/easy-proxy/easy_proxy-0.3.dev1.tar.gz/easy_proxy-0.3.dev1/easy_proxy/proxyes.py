from .base_classes import *
from .base_classes.proxy_getter import _re_proxy_format
from lxml import etree
from .setting import spyder_list
import re

def proxy_class(clazz):
    spyder_list.append(clazz)


@proxy_class
class Data5uProxy(BaseProxy):
    '''
    http://www.data5u.com/
    '''
    def __init__(self):
        self.url_list = [
            'http://www.data5u.com/',
            'http://www.data5u.com/free/gngn/index.shtml',
            'http://www.data5u.com/free/gnpt/index.shtml'
        ]
        self.func_list = [
            lambda x: etree.HTML(x.content),
            lambda x: [":".join(ui.xpath('.//li/text()')[0:2]) for ui in x.xpath('//ul[@class="l2"]')]
        ]

@proxy_class
class DoubleSixProxy(BaseProxy):
    '''
    http://www.66ip.cn/rj.html
    '''
    def __init__(self):
        self.url_list = [
            "http://www.66ip.cn/nmtq.php?getnum={}",
        ]
        self.before_func = [
            lambda x:x.format(20)
        ]

        def change_gbk(x):
            x.encoding = "GBK"
            return x

        self.after_func = [
            change_gbk,
        ]
        self.func_list = [
            lambda x:re.findall(_re_proxy_format, x.text)
        ]

@proxy_class
class XICIProxy(BaseProxy):
    '''
    国内{高匿/透明}代理
        https://www.xicidaili.com/nn/
        https://www.xicidaili.com/nt/
    '''
    def __init__(self):
        self.url_list = [
            'http://www.xicidaili.com/nn/',  # 高匿
            'http://www.xicidaili.com/nt/',  # 透明
        ]
        self.func_list = [
            lambda x:etree.HTML(x.content),
            lambda x:[":".join(ui.xpath('./td/text()')[0:2]) for ui in x.xpath('.//table[@id="ip_list"]//tr[position()>1]')],
        ]

@proxy_class
class GBJProxy(BaseProxy):
    '''
    全网代理 http://www.goubanjia.com
    '''

    def __init__(self):
        self.url_list = [
            "http://www.goubanjia.com",
        ]

        xpath_str = """.//*[not(contains(@style, 'display: none'))
                                                and not(contains(@style, 'display:none'))
                                                and not(contains(@class, 'port'))
                                                ]/text()
                                        """

        self.func_list = [
            lambda x:etree.HTML(x.content),
            lambda x:x.xpath('//td[@class="ip"]'),
            lambda x:[join_ip_port(ui) for ui in x],
        ]
        def join_ip_port(x):
            id = "".join(x.xpath(xpath_str))
            port = x.xpath(".//span[contains(@class, 'port')]/text()")[0]
            return f"{id}:{port}"

@proxy_class
class QuickProxy(BaseProxy):
    '''
    快代理
    https://www.kuaidaili.com/free/inha/
    https://www.kuaidaili.com/free/intr/
    '''
    def __init__(self):
        self.url_list = [
            'https://www.kuaidaili.com/free/inha/',
            'https://www.kuaidaili.com/free/intr/'
        ]

        self.func_list = [
            lambda x: etree.HTML(x.content),
            lambda x: [":".join(ui.xpath('./td/text()')[0:2]) for ui in x.xpath('.//table//tr')]
        ]

@proxy_class
class SeaProxy(BaseProxy):
    '''
    IP海
    http://www.iphai.com/free/ng
    '''
    def __init__(self):
        self.url_list = [
            'http://www.iphai.com/free/ng',
            'http://www.iphai.com/free/np',
            'http://www.iphai.com/free/wg',
            'http://www.iphai.com/free/wp'
        ]
        self.func_list = [
            lambda x:re.findall(r'<td>\s*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s*?</td>[\s\S]*?<td>\s*?(\d+)\s*?</td>', x.text),
            lambda x:[":".join(e) for e in x]
        ]



