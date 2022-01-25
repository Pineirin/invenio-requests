# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 CERN.
# Copyright (C) 2021 Northwestern University.
#
# Invenio-RDM-Records is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Test fixtures for application vocabulary fixtures."""

import pathlib

import pytest
from invenio_access.permissions import system_identity
from invenio_requests.fixtures.vocabularies import VocabulariesFixture


@pytest.fixture()
def vocabularies():
    """Vocabularies object fixture."""
    return VocabulariesFixture(
        system_identity,
        [pathlib.Path(__file__).parent / "data"],
        'vocabularies.yaml',
    )
