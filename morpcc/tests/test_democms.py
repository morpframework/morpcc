# Copyright (c) 2019 Mohd Izhar Firdaus Bin Ismail
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from .democms.app import App
from morpfw.tests.common import get_client
import os


def test_democms(pgsql_db):
    c = get_client(App, config=os.path.join(
        os.path.dirname(__file__), 'democms/settings.yml'))
    r = c.get('/')

    print(r.body)
