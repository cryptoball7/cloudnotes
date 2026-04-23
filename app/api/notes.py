from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.deps import get_db, get_current_user
from app.models.note import Note
from app.models.user import User
from app.schemas.note import NoteCreate, NoteUpdate, NoteOut

router = APIRouter()

# ✅ Create Note
@router.post("/", response_model=NoteOut)
def create_note(
    note: NoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_note = Note(
        title=note.title,
        content=note.content,
        user_id=current_user.id
    )

    db.add(new_note)
    db.commit()
    db.refresh(new_note)

    return new_note


# ✅ Get All Notes (ONLY user's notes)
@router.get("/", response_model=list[NoteOut])
def get_notes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    notes = db.query(Note).filter(Note.user_id == current_user.id).all()
    return notes


# ✅ Update Note (ONLY if owned)
@router.put("/{note_id}", response_model=NoteOut)
def update_note(
    note_id: int,
    updated: NoteUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    note = db.query(Note).filter(Note.id == note_id).first()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    if note.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    note.title = updated.title
    note.content = updated.content

    db.commit()
    db.refresh(note)

    return note


# ✅ Delete Note (ONLY if owned)
@router.delete("/{note_id}")
def delete_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    note = db.query(Note).filter(Note.id == note_id).first()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    if note.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    db.delete(note)
    db.commit()

    return {"message": "Note deleted"}

