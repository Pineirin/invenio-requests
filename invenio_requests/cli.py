# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016-2022 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Command-line tools for demo module."""

import click
from faker import Faker
from flask.cli import with_appcontext
from invenio_access.permissions import system_identity
from invenio_communities.fixtures.demo import create_fake_community
from invenio_communities.fixtures.tasks import create_demo_community
from invenio_rdm_records.proxies import current_rdm_records

from .fixtures.demo import create_fake_request
from .fixtures.tasks import create_demo_request


@click.group()
def requests():
    """Invenio communities commands."""


@requests.command('demo')
@with_appcontext
def demo():
    """Create 100 fake requests for demo purposes."""
    click.secho('Creating demo requests...', fg='green')

    faker = Faker()
    community = create_fake_community(faker)
    create_demo_community(community)

    for index in range(100):
        records_service = current_rdm_records.records_service
        draft = records_service.create(system_identity, minimal_record())
        records_service.publish(system_identity, draft.id)
        fake_data = create_fake_request(draft.id, community.id, index)
        create_demo_request.delay(fake_data)

    click.secho('Created requests!', fg='green')


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