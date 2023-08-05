# -*- coding: utf-8 -*-
"""
Created on Wed Dec 26 17:16:22 2018

@author: yili.peng
"""

from setuptools import setup
from pypandoc import convert_file

setup(name='multi_factor_model'
      ,version='0.0.0a5'
      ,description='factor model'
      ,long_description=convert_file('README.md', 'rst', format='markdown_github').replace("\r","")
      ,lisence='MIT'
      ,author='Yili Peng'
      ,author_email='yili_peng@outlook.com'
      ,packages=['multi_factor_model']
      ,zip_safe=False)
