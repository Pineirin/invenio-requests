# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016-2022 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Celery tasks for fixtures."""


from celery import shared_task
from invenio_access.permissions import system_identity

from invenio_requests.customizations import DefaultRequestType
from invenio_requests.proxies import current_requests


@shared_task
def create_demo_request(data):
    """Create a demo request."""
    def request_record_input_data():
        """Input data to a Request record."""
        return {"title": "Demo", "receiver": {"user": "1"}}

    def create_request(identity, request_record_input_data, requests_service):
        input_data = request_record_input_data
        receiver = identity[1]
        # Need to use the service to get the id
        item = requests_service.create(
            identity, input_data, DefaultRequestType, receiver=receiver
        )
        return item._request

    requests_service = current_requests.requests_service
    request = create_request(
        system_identity, request_record_input_data(), requests_service
    )
    id_ = request.id
    data.id = id_
    requests_service.execute_action(system_identity, id_, "submit", data)
