from flask.views import MethodView
from flask_smorest import Blueprint, abort

from app.models import note_storage
from app.schemas import NoteSchema, NoteCreateSchema, NoteUpdateSchema

blp = Blueprint(
    "Notes",
    "notes",
    url_prefix="/notes",
    description="Operations on notes"
)

@blp.route("/")
class NotesList(MethodView):
    """
    get:
      summary: List notes
      description: Retrieve a list of all notes.
    post:
      summary: Create a new note
      description: Create and persist a new note.
    """
    # PUBLIC_INTERFACE
    @blp.response(200, NoteSchema(many=True), description="List of all notes")
    def get(self):
        """Returns list of all notes"""
        notes = note_storage.list_notes()
        return [n.to_dict() for n in notes]

    # PUBLIC_INTERFACE
    @blp.arguments(NoteCreateSchema, location="json")
    @blp.response(201, NoteSchema, description="The created note")
    def post(self, note_data):
        """
        Creates a new note.
        """
        note = note_storage.create_note(note_data["title"], note_data["content"])
        return note.to_dict()


@blp.route("/<int:note_id>")
class NoteDetail(MethodView):
    """
    get:
      summary: Get a note by id
      description: Returns the note with the given id.
    put:
      summary: Update a note
      description: Updates an existing note fully.
    delete:
      summary: Delete a note
      description: Deletes the note with the given id.
    """
    # PUBLIC_INTERFACE
    @blp.response(200, NoteSchema, description="The note object")
    def get(self, note_id):
        """Returns the note by id"""
        note = note_storage.get_note(note_id)
        if not note:
            abort(404, message="Note not found.")
        return note.to_dict()

    # PUBLIC_INTERFACE
    @blp.arguments(NoteUpdateSchema, location="json")
    @blp.response(200, NoteSchema, description="The updated note")
    def put(self, note_data, note_id):
        """
        Updates an existing note.
        """
        note = note_storage.update_note(note_id, note_data["title"], note_data["content"])
        if not note:
            abort(404, message="Note not found.")
        return note.to_dict()

    # PUBLIC_INTERFACE
    @blp.response(204, description="Note deleted")
    def delete(self, note_id):
        """Deletes the note by id"""
        deleted = note_storage.delete_note(note_id)
        if not deleted:
            abort(404, message="Note not found.")
        # 204 No Content has no body
        return ""
