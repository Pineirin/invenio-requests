# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 CERN.
#
# Invenio-Requests is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Request views module."""

from flask import render_template
from sqlalchemy.orm.exc import NoResultFound
from flask import g
from invenio_requests.views.decorators import pass_request
from invenio_rdm_records.resources.serializers import UIJSONSerializer
from invenio_rdm_records.proxies import current_rdm_records_service

@pass_request
def requests_detail(request=None, pid_value=None):
    """Community detail page."""
    request_dict = request.to_dict()

    # temporarily, until serializers and avatars implemented
    request_dict["created_by"].update({
        "avatar": "/static/images/placeholder.png",
        "full_name": "Uma Thurman"
    })

    request_dict["receiver"].update({
        "avatar": "/static/images/placeholder.png",
        "full_name": "John Travolta"
    })
    draft = None
    request_dict["topic"] = request._request.topic.resolve()
    record = request_dict["topic"]
    draft = current_rdm_records_service.read_draft(id_=record["id"],
                                                   identity=g.identity)
    is_draft = draft._record.is_draft
    permissions = draft.has_permissions_to(['edit', 'new_version', 'manage',
                                            'update_draft', 'read_files']),
    draft = UIJSONSerializer().serialize_object_to_dict(draft.data)

    # end temporary block

    return render_template(
        f"invenio_requests/{request_dict['type']}/index.html",
        request=request_dict,  # TODO: use serializer
        record=draft,
        is_preview=True,
        is_draft=is_draft,
        permissions=permissions,
        files=[]
    )
