from fastapi import FastAPI
from pydantic import BaseModel
import random

app = FastAPI()
flashcards = []

class Flashcard(BaseModel):
    student_id: str
    question: str
    answer: str

SUBJECT_KEYWORDS = {
    "Physics": ["force", "acceleration", "newton"],
    "Biology": ["photosynthesis", "plant"],
    "Math": ["algebra", "equation"],
    "Chemistry": ["atom", "reaction"]
}

def detect_subject(text):
    text = text.lower()
    for subject, keywords in SUBJECT_KEYWORDS.items():
        if any(word in text for word in keywords):
            return subject
    return "General"

@app.post("/flashcard")
def add_flashcard(f: Flashcard):
    subject = detect_subject(f.question)
    flashcards.append({
        "student_id": f.student_id,
        "question": f.question,
        "answer": f.answer,
        "subject": subject
    })
    return {"message": "Flashcard added successfully", "subject": subject}

@app.get("/get-subject")
def get_flashcards(student_id: str, limit: int = 5):
    student_cards = [c for c in flashcards if c["student_id"] == student_id]
    result = []
    subjects = {}
    for c in student_cards:
        if c["subject"] not in subjects:
            subjects[c["subject"]] = []
        subjects[c["subject"]].append(c)
    for s in subjects.values():
        result.append(random.choice(s))
        if len(result) >= limit:
            break
    return result
