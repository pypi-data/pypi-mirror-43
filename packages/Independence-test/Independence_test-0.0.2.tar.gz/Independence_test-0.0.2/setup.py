# -*- coding: utf-8 -*-
"""
Created on Thu May  3 16:50:29 2018

@author: yili.peng
"""

from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='Independence_test'
      ,version='0.0.2'
      ,description='Time Series Independence test'
      ,long_description=readme()
      ,author='Yili Peng'
      ,author_email='yili_peng@outlook.com'
      ,packages=['Independence_test'])