# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 CERN.
# Copyright (C) 2021 Northwestern University.
# Copyright (C) 2021 TU Wien.
#
# Invenio-Requests is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""RequestEvents Service."""

from invenio_db import db
from invenio_records_resources.services import RecordService

from ...records.api import Request, RequestEventType


class RequestEventsService(RecordService):
    """Request Events service."""

    def create(self, identity, request_id, data):
        """Create a request event.

        :param request_id: Identifier of the request.
        :param identity: Identity of user creating the event.
        :param dict data: Input data according to the data schema.
        """
        request = self._get_request(request_id)
        permission = self._get_permission("create", data["type"])
        self.require_permission(identity, permission, request=request)

        # Validate data and create record with pid
        # (if there are errors, .load() raises)
        data, errors = self.schema.load(
            data,
            context={"identity": identity},
        )

        # It's the components that save the actual data in the record.
        record = self.record_cls.create(
            {},
            request=request.model,
            type=data["type"],
        )

        # Run components
        self.run_components(
            "create", identity=identity, record=record, request=request, data=data
        )

        # Persist record (DB and index)
        record.commit()
        db.session.commit()
        if self.indexer:
            self.indexer.index(record)

        return self.result_item(
            self,
            identity,
            record,
            links_tpl=self.links_item_tpl,
        )

    def read(self, identity, id_):
        """Retrieve a record."""
        record = self._get_event(id_)
        request = record.request

        # Same "read_event" permission for all types of events
        self.require_permission(identity, "read_event", request=request)

        return self.result_item(
            self,
            identity,
            record,
            links_tpl=self.links_item_tpl,
        )

    def update(self, identity, id_, data, revision_id=None):
        """Replace an event."""
        record = self._get_event(id_)

        self.check_revision_id(record, revision_id)

        # Permissions
        permission = self._get_permission("update", data["type"])
        self.require_permission(identity, permission, record=record)

        data, _ = self.schema.load(
            data, context=dict(identity=identity, pid=record.pid, record=record)
        )

        # Run components
        self.run_components(
            "update",
            identity=identity,
            record=record,
            data=data,
        )

        record.commit()
        db.session.commit()

        if self.indexer:
            self.indexer.index(record)

        return self.result_item(
            self,
            identity,
            record,
            links_tpl=self.links_item_tpl,
        )

    def delete(self, identity, id_, revision_id=None):
        """Delete an event from database and search indexes.

        Deleting a comment is wiping the content and setting the type
        to deleted.

        Deleting other events is really deleting them.
        """
        record = self._get_event(id_)

        self.check_revision_id(record, revision_id)

        # Permissions
        permission = self._get_permission("delete", record.type)
        self.require_permission(identity, permission, record=record)

        if record.type == RequestEventType.COMMENT.value:
            record["type"] = RequestEventType.DELETED_COMMENT.value
            record["content"] = ""
            record.commit()
            db.session.commit()
            if self.indexer:
                self.indexer.index(record, refresh=True)
        else:
            record.delete()
            db.session.commit()
            if self.indexer:
                self.indexer.delete(record, refresh=True)

        return self.result_item(
            self,
            identity,
            record,
            links_tpl=self.links_item_tpl,
        )

    def search(self, identity, params=None, es_preference=None, **kwargs):
        """Search for records matching the querystring."""
        params = params or {}

        # Permissions
        request_id = params.get("request_id")
        request = self._get_request(request_id) if request_id else None
        self.require_permission(identity, "search", request=request)

        # Prepare and execute the search
        search = self._search(
            "search",
            identity,
            params,
            es_preference,
            permission_action="read_event",
            **kwargs,
        )
        search_result = search.execute()

        return self.result_list(
            self,
            identity,
            search_result,
            params,
            # links_tpl=LinksTemplate(self.config.links_search, context={
            #     "args": params
            # }),
            # links_item_tpl=self.links_item_tpl,
        )

    # Utilities
    @property
    def request_cls(self):
        """Get associated request class."""
        return self.config.request_cls

    def _get_permission(self, action, event_type):
        """Get associated permission.

        Needed to distinguish between comment creation and other events.
        """
        if event_type == RequestEventType.COMMENT.value:
            return f"{action}_event_comment"
        else:
            return f"{action}_event"

    def _get_request(self, request_id):
        """Get associated request."""
        # TODO: Replace with whatever interface Request provides to get one
        from ..requests import RequestsService, RequestsServiceConfig

        return RequestsService(config=RequestsServiceConfig())._get_request(request_id)

    def _get_event(self, event_id, with_deleted=True):
        """Get associated event_id."""
        return self.record_cls.get_record(event_id, with_deleted=with_deleted)