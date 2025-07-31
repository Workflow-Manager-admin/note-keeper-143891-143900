from marshmallow import Schema, fields

# PUBLIC_INTERFACE
class NoteSchema(Schema):
    """Schema for a Note object"""
    id = fields.Int(dump_only=True, description="The unique identifier for a note")
    title = fields.Str(required=True, description="The title of the note")
    content = fields.Str(required=True, description="The content of the note")


# PUBLIC_INTERFACE
class NoteCreateSchema(Schema):
    """Schema for creating a new note"""
    title = fields.Str(required=True, description="The title of the note")
    content = fields.Str(required=True, description="The content of the note")

# PUBLIC_INTERFACE
class NoteUpdateSchema(Schema):
    """Schema for updating an existing note"""
    title = fields.Str(required=True, description="The updated title of the note")
    content = fields.Str(required=True, description="The updated content of the note")
