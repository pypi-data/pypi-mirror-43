# -*- coding: utf-8 -*-
"""
Created on Thu May  3 16:50:29 2018

@author: yili.peng
"""

from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='CVineModel'
      ,version='0.0.3'
      ,description='CVine Colpula Model'
      ,long_description=readme()
      ,keywords='Vine Copula'
      ,author='Yili Peng'
      ,author_email='yili_peng@outlook.com'
      ,packages=['CVineModel'])