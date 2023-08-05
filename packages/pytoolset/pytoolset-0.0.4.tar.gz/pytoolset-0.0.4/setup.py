"""

"""
import codecs
import os
import sys
"""
打包的用的setup必须引入
"""
try:
    from setuptools import setup
except:
    from distutils.core import setup


"""
当前包的版本
"""
VERSION = "0.0.4"


"""
名字，一般放包的名字
"""
NAME = "pytoolset"


"""
包含的包，可以多个，这是一个列表
"""
PACKAGES = ["pytoolset",]


"""
关于这个包的描述
"""
DESCRIPTION = "this is a test package for packing python liberaries tutorial."


"""
关于当前包的一些关键字，方便PyPI进行分类。
"""
KEYWORDS = "test python package"


"""
包的作者
"""
AUTHOR = "Zonas Wang"


"""
作者的邮件地址
"""
AUTHOR_EMAIL = "zonas.wang@gmail.com"


"""
你这个包的项目地址，如果有，给一个吧，没有你直接填写在PyPI你这个包的地址也是可以的
"""
URL = ""


"""
授权方式
"""
LICENSE = "MIT"


# 把上面的变量填入这里
setup(
    name = NAME,
    version = VERSION,
    description = DESCRIPTION,
    classifiers = [
                    'License :: OSI Approved :: MIT License',
                    'Programming Language :: Python',
                    'Intended Audience :: Developers',
                    'Operating System :: OS Independent',
                ],
    keywords = KEYWORDS,
    author = AUTHOR,
    author_email = AUTHOR_EMAIL,
    url = URL,
    license = LICENSE,
    packages = PACKAGES,
    include_package_data=True,
    zip_safe=True,
)


