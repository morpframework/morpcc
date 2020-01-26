# Copyright (c) 2019 Mohd Izhar Firdaus Bin Ismail
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from .democms.app import App
from morpfw.tests.common import get_client, create_admin
import os
import yaml
import tempfile

pages = [
    "/",
    "/profile/+view",
    "/page/+listing",
    "/page/+create",
    "/page/+modal-create",
    "/page/+datatable.json",
    "/+site-settings",
]


def test_democms(pgsql_db):
    settings_file = os.path.join(os.path.dirname(__file__), "democms/settings.yml")
    with open(settings_file) as sf:
        settings = yaml.load(sf, Loader=yaml.Loader)

    settings["configuration"][
        "morpfw.storage.sqlstorage.dburi"
    ] = "postgresql://postgres@localhost:45678/morpcc_tests"

    test_settings = tempfile.mktemp()
    with open(test_settings, "w") as ts:
        yaml.dump(settings, ts)

    c = get_client(test_settings)
    os.unlink(test_settings)

    create_admin(c, "admin", "password", "admin@localhost.local")

    r = c.get("/")
    # test redirect to login page
    assert r.status_code == 302
    assert r.headers["Location"].split("?")[0].endswith("/login")

    # test login
    r = c.post(
        r.headers["Location"],
        {
            "__formid_": "deform",
            "username": "admin",
            "password": "password",
            "Submit": "Login",
        },
    )

    assert "userid" in c.cookies.keys()

    # test load homepage
    r = c.get("/")

    assert r.status_code == 200

    # test load common pages
    for p in pages:
        r = c.get(p)
        assert r.status_code == 200

    # create page
    r = c.post(
        "/page/+create",
        {
            "__formid_": "deform",
            "title": "pagetitle",
            "description": "pagedesc",
            "location": "pageloc",
            "body": "pagebody",
            "Submit": "submit",
        },
    )

    assert r.status_code == 302

    page_url = r.headers["Location"]

    r = r.follow().follow()

    assert r.status_code == 200

    # edit page

    r = c.post(
        page_url + "/+edit",
        {
            "__formid_": "deform",
            "title": "pagetitle",
            "description": "pagedesc",
            "location": "pageloc",
            "body": "pagebody2",
            "Submit": "submit",
        },
    )

    assert r.status_code == 302

    r = r.follow().follow()

    assert r.status_code == 200

