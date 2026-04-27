"""Marshmallow schemas for request validation and response serialisation."""

from marshmallow import Schema, fields, validate

STATUS_VALUES = ["pending", "in_progress", "done"]
PRIORITY_VALUES = ["low", "medium", "high"]


class TaskSchema(Schema):
    """Full task representation — used for API responses."""

    id = fields.Int(dump_only=True)
    title = fields.Str(dump_only=True)
    description = fields.Str(dump_only=True, allow_none=True)
    status = fields.Str(dump_only=True)
    priority = fields.Str(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class TaskCreateSchema(Schema):
    """Validates the request body for POST /tasks."""

    title = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    description = fields.Str(load_default=None)
    status = fields.Str(
        load_default="pending",
        validate=validate.OneOf(STATUS_VALUES),
    )
    priority = fields.Str(
        load_default="medium",
        validate=validate.OneOf(PRIORITY_VALUES),
    )


class TaskUpdateSchema(Schema):
    """Validates the request body for PUT /tasks/<id> — all fields optional."""

    title = fields.Str(validate=validate.Length(min=1, max=200))
    description = fields.Str(allow_none=True)
    status = fields.Str(validate=validate.OneOf(STATUS_VALUES))
    priority = fields.Str(validate=validate.OneOf(PRIORITY_VALUES))


class TaskQueryArgsSchema(Schema):
    """Query-string parameters for filtering the task list."""

    status = fields.Str(validate=validate.OneOf(STATUS_VALUES))
    priority = fields.Str(validate=validate.OneOf(PRIORITY_VALUES))
