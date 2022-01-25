# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016-2021 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Tests for the CLI."""

from pathlib import Path

from faker import Faker
from invenio_access.permissions import system_identity
from invenio_communities.fixtures.demo import create_fake_community
from invenio_communities.fixtures.tasks import create_demo_community
from invenio_rdm_records.proxies import current_rdm_records

from invenio_requests.fixtures.demo import create_fake_request
from invenio_requests.fixtures.tasks import create_demo_request


def test_fake_demo_request_creation(app, db, location, es_clear, vocabularies):
    """Assert that demo community creation works without failing."""
    #breakpoint()

    vocabularies.load_vocabulary(
        'resource_types',
        {
            "pid-type": "rsrct",
            "data-file": (
                Path(__file__).parent / "data/vocabularies/resource_types.yaml"
            )
        },
        delay=False
    )
    vocabularies.load_vocabulary(
        'languages',
        {
            "pid-type": "lng",
            "data-file": (
                Path(__file__).parent / "data/vocabularies/languages.yaml"
            )
        },
        delay=False
    )

    faker = Faker()
    community = create_fake_community(faker)
    create_demo_community(community)
    print(community)
    records_service = current_rdm_records.records_service
    draft = records_service.create(system_identity, minimal_record())
    records_service.publish(system_identity, draft.id)
    print(draft)
    create_demo_request(create_fake_request(community.id, draft.id, 1))


def minimal_record():
    """Minimal record data as dict coming from the external world."""
    return {
        "pids": {},
        "access": {
            "record": "public",
            "files": "public",
        },
        "files": {
            "enabled": False,  # Most tests don't care about files
        },
        "metadata": {
            "publication_date": "2020-06-01",
            "resource_type": {"id": "image-photo"},
            "creators": [{
                "person_or_org": {
                    "family_name": "Brown",
                    "given_name": "Troy",
                    "type": "personal"
                }
            }, {
                "person_or_org": {
                    "name": "Troy Inc.",
                    "type": "organizational",
                },
            }],
            "title": "A Romans story"
        }
    }
