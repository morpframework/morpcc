# Copyright (c) 2019 Mohd Izhar Firdaus Bin Ismail
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import tempfile

import morpfw.sql as morpsql
import yaml
from morpfw.tests.common import create_admin, get_client, make_request

from .democms.app import App

pages = [
    "/",
    "/profile/+view",
    "/page/+listing",
    "/page/+create",
    "/page/+modal-create",
    "/page/+datatable.json",
    "/+site-settings",
]


def follow(resp):
    while resp.status_code == 302:
        resp = resp.follow()

    return resp


def test_democms(pgsql_db, pgsql_db_warehouse):
    settings_file = os.path.join(os.path.dirname(__file__), "democms/settings.yml")
    with open(settings_file) as sf:
        settings = yaml.load(sf, Loader=yaml.Loader)

    settings["configuration"][
        "morpfw.storage.sqlstorage.dburi"
    ] = "postgresql://postgres@localhost:45678/morpcc_tests"

    settings["configuration"][
        "morpfw.storage.sqlstorage.dburi.warehouse"
    ] = "postgresql://postgres@localhost:45678/morpcc_warehouse"

    test_settings = tempfile.mktemp()
    with open(test_settings, "w") as ts:
        yaml.dump(settings, ts)

    c = get_client(test_settings)
    os.unlink(test_settings)

    req = make_request(c.app.app)
    morpsql.Base.metadata.create_all(bind=req.db_session.bind)

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
            "__formid__": "deform",
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
            "__formid__": "deform",
            "title": "pagetitle",
            "description": "pagedesc",
            "location": "pageloc",
            "body": "pagebody2",
            "Submit": "submit",
        },
    )

    assert r.status_code == 302

    r = follow(r)

    assert r.status_code == 200

    # test application creation

    r = c.post(
        "/application/+create",
        {
            "__formid__": "deform",
            "name": "test_app",
            "title": "Application",
            "icon": "database",
        },
    )

    app_loc = r.headers["Location"]
    app_uuid = app_loc.split("/")[-1]

    assert r.headers.get("X-MORP-FORM-FAILED", None) is None
    assert r.status_code == 302
    assert follow(r).status_code == 200
    # create entity

    r = c.post(
        "/entity/+create",
        {
            "__formid__": "deform",
            "name": "person",
            "title": "Person",
            "application_uuid": app_uuid,
        },
    )

    assert r.headers.get("X-MORP-FORM-FAILED", None) is None
    assert r.status_code == 302
    person_loc = r.headers["Location"]
    person_uuid = person_loc.split("/")[-1]
    assert follow(r).status_code == 200

    # create attribute
    r = c.post(
        "/attribute/+create",
        {
            "__formid__": "deform",
            "name": "personid",
            "type": "integer",
            "title": "Person ID",
            "entity_uuid": person_uuid,
        },
    )

    assert r.headers.get("X-MORP-FORM-FAILED", None) is None
    assert r.status_code == 302

    person_id_loc = r.headers["Location"]
    person_id_uuid = person_id_loc.split("/")[-1]

    assert follow(r).status_code == 200

    r = c.post(
        "/attribute/+create",
        {
            "__formid__": "deform",
            "name": "full_name",
            "type": "string",
            "title": "Full Name",
            "entity_uuid": person_uuid,
        },
    )

    assert r.headers.get("X-MORP-FORM-FAILED", None) is None

    person_name_loc = r.headers["Location"]
    person_name_uuid = person_name_loc.split("/")[-1]

    assert r.status_code == 302
    assert follow(r).status_code == 200

    r = c.post(
        "/behaviorassignment/+create",
        {
            "__formid__": "deform",
            "behavior": "morpcc.titled_document",
            "entity_uuid": person_uuid,
        },
    )

    assert r.headers.get("X-MORP-FORM-FAILED", None) is None
    assert r.status_code == 302
    assert follow(r).status_code == 200

    r = c.post(
        "/entity/+create",
        {
            "__formid__": "deform",
            "name": "address",
            "title": "Address",
            "application_uuid": app_uuid,
        },
    )

    assert r.headers.get("X-MORP-FORM-FAILED", None) is None
    address_loc = r.headers.get("Location")
    address_uuid = address_loc.split("/")[-1]

    assert r.status_code == 302
    assert follow(r).status_code == 200

    r = c.post(
        "/attribute/+create",
        {
            "__formid__": "deform",
            "name": "address",
            "type": "string",
            "title": "Address",
            "entity_uuid": address_uuid,
        },
    )

    assert r.headers.get("X-MORP-FORM-FAILED", None) is None
    assert r.status_code == 302
    assert follow(r).status_code == 200

    r = c.post(
        "/relationship/+create",
        {
            "__formid__": "deform",
            "name": "personid",
            "title": "Person",
            "entity_uuid": address_uuid,
            "reference_attribute_uuid": person_id_uuid,
            "reference_search_attribute_uuid": person_name_uuid,
        },
    )

    assert r.headers.get("X-MORP-FORM-FAILED", None) is None
    person_address_rel_loc = r.headers.get("Location")
    person_address_rel_uuid = person_address_rel_loc.split("/")[-1]
    assert r.status_code == 302
    assert follow(r).status_code == 200

    r = c.post(
        "/backrelationship/+create",
        {
            "__formid__": "deform",
            "name": "addresses",
            "title": "Addresses",
            "entity_uuid": address_uuid,
            "reference_relationship_uuid": person_address_rel_uuid,
        },
    )

    assert r.headers.get("X-MORP-FORM-FAILED", None) is None
    assert r.status_code == 302
    assert follow(r).status_code == 200
