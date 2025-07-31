import os
import json
from typing import List, Dict, Optional
from threading import Lock

# PUBLIC_INTERFACE
class Note:
    """
    Represents a Note object.
    """
    def __init__(self, id: int, title: str, content: str):
        self.id = id
        self.title = title
        self.content = content

    def to_dict(self):
        return {"id": self.id, "title": self.title, "content": self.content}

    @staticmethod
    def from_dict(data: Dict):
        return Note(
            id=data["id"],
            title=data["title"],
            content=data["content"],
        )


class NoteStorage:
    """
    Handles persistent storage for notes using a JSON file.
    Thread-safe for simple use cases.
    """
    _lock = Lock()

    def __init__(self, storage_path: str = "notes_data.json"):
        self.storage_path = storage_path
        self._notes: List[Note] = []
        self._next_id = 1
        self._load()

    def _load(self):
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self._notes = [Note.from_dict(d) for d in data]
                if self._notes:
                    self._next_id = max(note.id for note in self._notes) + 1
            except Exception:
                self._notes = []
                self._next_id = 1
        else:
            self._notes = []
            self._next_id = 1

    def _save(self):
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump([note.to_dict() for note in self._notes], f, indent=2)

    # PUBLIC_INTERFACE
    def list_notes(self) -> List[Note]:
        """
        Returns a list of all notes.
        """
        with self._lock:
            return list(self._notes)

    # PUBLIC_INTERFACE
    def get_note(self, note_id: int) -> Optional[Note]:
        """
        Returns a note by ID, or None if not found.
        """
        with self._lock:
            return next((n for n in self._notes if n.id == note_id), None)

    # PUBLIC_INTERFACE
    def create_note(self, title: str, content: str) -> Note:
        """
        Creates a new note, assigns a unique ID, and persists it.
        """
        with self._lock:
            note = Note(self._next_id, title, content)
            self._notes.append(note)
            self._next_id += 1
            self._save()
            return note

    # PUBLIC_INTERFACE
    def update_note(self, note_id: int, title: str, content: str) -> Optional[Note]:
        """
        Updates an existing note. Returns updated note or None if not found.
        """
        with self._lock:
            for note in self._notes:
                if note.id == note_id:
                    note.title = title
                    note.content = content
                    self._save()
                    return note
        return None

    # PUBLIC_INTERFACE
    def delete_note(self, note_id: int) -> bool:
        """
        Deletes a note by ID. Returns True if deleted, False if not found.
        """
        with self._lock:
            for i, note in enumerate(self._notes):
                if note.id == note_id:
                    del self._notes[i]
                    self._save()
                    return True
        return False

# A global instance for app-wide use
note_storage = NoteStorage()
