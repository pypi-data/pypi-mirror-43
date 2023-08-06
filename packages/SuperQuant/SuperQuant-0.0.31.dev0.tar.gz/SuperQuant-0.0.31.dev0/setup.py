#coding :utf-8


"""
SuperQuant

SuperQuant Financial Strategy Framework

by Junfeng Li

2019/02/06
"""


import codecs
import io
import os
import re
import sys
import webbrowser
import platform

from setuptools import setup,find_packages

"""
打包的用的setup必须引入，
"""

if sys.version_info.major != 3 or sys.version_info.minor not in [4, 5, 6, 7, 8]:
    print('wrong version, should be 3.4/3.5/3.6/3.7/3.8 version')
    sys.exit()

version = '0.0.31.dev0'
author = 'Junfeng Li'

try:
    if sys.platform in ['win32', 'darwin']:
        print(webbrowser.open(
            'https://github.com/Fengbrain/SuperQuant'))
        print('finish install')
except:
    pass


def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()


NAME = "SuperQuant"

"""
名字，一般放你包的名字即可
"""
PACKAGES = ["SuperQuant"]#find_packages()#["SuperQuant","SuperQuant.SQ_Backtesting"]
"""
包含的包，可以多个，这是一个列表
"""

DESCRIPTION = "SuperQuant:Quantitative Financial Strategy Framework"

LONG_DESCRIPTION = 'tools'
# with open("README_ENG.md", "r") as fh:
#     LONG_DESCRIPTION = fh.read()


"""
参见read方法说明
"""

KEYWORDS = ["SuperQuant", "quant", "finance", "Backtest", 'Framework']
"""
关于当前包的一些关键字，方便PyPI进行分类。
"""

AUTHOR_EMAIL = "617644591@qq.com"

URL = "https://github.com/Fengbrain/SuperQuant"


LICENSE = "MIT"

setup(
    name=NAME,
    version=version,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    # install_requires=['pandas>=0.23.4', 'numpy>=1.12.0', 'tushare', 'flask_socketio>=2.9.0 ', 'motor>=1.1', 'seaborn>=0.8.1', 'pyconvert>=0.6.3',
    #                   'lxml>=4.0', ' beautifulsoup4', 'matplotlib', 'requests', 'selenium', 'tornado',
    #                   'demjson>=2.2.4', 'scrapy',
    #                   'pymongo>=3.7', 'six>=1.10.0', 'tabulate>=0.7.7', 'pytdx>=1.67', 'retrying>=1.3.3',
    #                   'zenlog>=1.1', 'delegator.py>=0.0.12', 'flask>=0.12.2', 'pyecharts', 'protobuf>=3.4.0'],
    # entry_points={
    #     'console_scripts': [
    #         'quantaxis=QUANTAXIS.QACmd:QA_cmd',
    #         'quantaxisq=QUANTAXIS.QAFetch.QATdx_adv:bat',
    #         'qarun=QUANTAXIS.QACmd.runner:run'
    #     ]
    # },
    # install_requires=requirements,
    keywords=KEYWORDS,
    author=author,
    author_email=AUTHOR_EMAIL,
    url=URL,
    license=LICENSE,
    packages=PACKAGES,
    include_package_data=True,
    zip_safe=True
)

# 把上面的变量填入了一个setup()中即可。
