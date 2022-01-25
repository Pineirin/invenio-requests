# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016-2022 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Fake demo records."""

import datetime
import json
import random

from edtf.parser.grammar import level0Expression
from faker import Faker


def fake_edtf_level_0():
    """Generates a fake publication_date string."""
    def fake_date(end_date=None):
        fake = Faker()
        date_pattern = ['%Y', '%m', '%d']
        # make it less and less likely to get less and less parts of the date

        if random.choice([True, False]):
            date_pattern.pop()
            if random.choice([True, False]):
                date_pattern.pop()

        return fake.date("-".join(date_pattern), end_datetime=end_date)

    f_date = fake_date()

    # if interval
    if random.choice([True, False]):
        # get f_date as date object
        parser = level0Expression("level0")
        parsed_date = parser.parseString(f_date)[0]
        date_tuple = parsed_date.lower_strict()[:3]
        f_date_object = datetime.date(*date_tuple)

        interval_start = fake_date(end_date=f_date_object)

        return "/".join([interval_start, f_date])

    return f_date


def create_fake_request(community_id, draft_id, number):
    """Create fake requests for demo purposes."""
    status_enum = ["DRAFT", "OPEN", "CANCELLED", "DECLINED", "ACCEPTED", "EXPIRED"]
    status = random.choice(status_enum)
    open = True if status == "DRAFT" or status == "OPEN" else False
    updated = fake_edtf_level_0()
    created = fake_edtf_level_0()
    fake = Faker()
    data_to_use = {
        "number": community_id + ":" + number,
        "created": created,
        "updated": updated,
        "expires_at": None,
        "is_expired": False,
        "revision_id": 3,
        "status": status,
        "is_open": open,
        "title": fake.text(max_nb_chars=50),
        "request_type": "Generic Request",
        "receiver": {
            "community": community_id
        },
        "created_by": {
            "user": "1"
        },
        "subject": {
            "record": draft_id
        }
    }

    return json.loads(json.dumps(data_to_use))
