# -*- coding: utf-8 -*-

"""
    apimaticcalculatorpytho

    This file was automatically generated for testing by APIMATIC v2.0 ( https://apimatic.io ).
"""

from apimaticcalculatorpytho.decorators import lazy_property
from apimaticcalculatorpytho.configuration import Configuration
from apimaticcalculatorpytho.controllers.simple_calculator import SimpleCalculator


class ApimaticcalculatorpythoClient(object):

    config = Configuration

    @lazy_property
    def simple_calculator(self):
        return SimpleCalculator()


    def __init__(self,
                 gfdsfkl=None,
                 dsfsdf=None,
                 basic_auth_user_name=None,
                 basic_auth_password=None):
        if gfdsfkl != None:
            Configuration.gfdsfkl = gfdsfkl
        if dsfsdf != None:
            Configuration.dsfsdf = dsfsdf
        if basic_auth_user_name != None:
            Configuration.basic_auth_user_name = basic_auth_user_name
        if basic_auth_password != None:
            Configuration.basic_auth_password = basic_auth_password


