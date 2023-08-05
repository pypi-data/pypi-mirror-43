# -*- coding: utf-8 -*-
"""
Created on Thu Jun 21 10:54:40 2018

@author: yili.peng
"""

from setuptools import setup
from pypandoc import convert_file

setup(name='barra_risk_model'
      ,version='0.1.5'
      ,description='Barra Risk Model CN version'
      ,long_description=convert_file('README.md', 'rst', format='markdown_github').replace("\r","")
      ,lisence='MIT'
      ,author='Yili Peng'
      ,author_email='yili_peng@outlook.com'
      ,packages=['barra_risk_model',
                 'barra_risk_model.common',
                 'barra_risk_model.Factor_return',
                 'barra_risk_model.Factor_manufacture',
                 'barra_risk_model.Wind_update'
                 ]
      ,install_requires=[
          'RNWS>=0.1.0',
      ]
      ,zip_safe=False)