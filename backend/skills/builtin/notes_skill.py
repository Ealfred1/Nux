"""
Notes Skill (v0.4)
Quick voice notes and reminders
"""
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any
from core.skill_base import Skill, SkillMetadata


class NotesSkill(Skill):
    """Take and manage voice notes"""
    
    def __init__(self):
        super().__init__()
        self.notes_file = Path.home() / ".nuxai" / "notes.json"
        self.notes_file.parent.mkdir(parents=True, exist_ok=True)
        self._load_notes()
    
    def get_metadata(self) -> SkillMetadata:
        return SkillMetadata(
            name="notes",
            version="1.0.0",
            author="NuxAI Team",
            description="Take quick voice notes and reminders",
            triggers=["note", "remember", "remind me", "write down"]
        )
    
    async def execute(self, command: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute note command"""
        command_lower = command.lower()
        
        # Take a note
        if any(phrase in command_lower for phrase in ["note", "remember", "write down"]):
            note_text = self._extract_note_text(command)
            if note_text:
                note_id = self._save_note(note_text)
                return {
                    "success": True,
                    "result": f"Note saved: {note_text}",
                    "speak": f"I've saved that note"
                }
        
        # List notes
        elif "list notes" in command_lower or "show notes" in command_lower:
            notes = self._get_recent_notes(5)
            if notes:
                notes_text = "\n".join([f"- {n['text']}" for n in notes])
                return {
                    "success": True,
                    "result": notes_text,
                    "speak": f"You have {len(notes)} recent notes"
                }
            else:
                return {
                    "success": True,
                    "result": "No notes found",
                    "speak": "You don't have any notes yet"
                }
        
        return {
            "success": False,
            "error": "Could not understand note command"
        }
    
    def _extract_note_text(self, command: str) -> str:
        """Extract note text from command"""
        # Remove trigger words
        triggers = ["note", "remember", "remind me", "write down", "that", "to"]
        words = command.lower().split()
        
        # Find where actual note starts
        start_idx = 0
        for trigger in triggers:
            trigger_words = trigger.split()
            for i in range(len(words) - len(trigger_words) + 1):
                if words[i:i+len(trigger_words)] == trigger_words:
                    start_idx = max(start_idx, i + len(trigger_words))
        
        return " ".join(command.split()[start_idx:])
    
    def _load_notes(self):
        """Load notes from file"""
        if self.notes_file.exists():
            with open(self.notes_file, 'r') as f:
                self.notes = json.load(f)
        else:
            self.notes = []
    
    def _save_note(self, text: str) -> str:
        """Save a new note"""
        note = {
            "id": datetime.now().strftime("%Y%m%d%H%M%S"),
            "text": text,
            "timestamp": datetime.now().isoformat()
        }
        self.notes.append(note)
        
        # Save to file
        with open(self.notes_file, 'w') as f:
            json.dump(self.notes, f, indent=2)
        
        return note["id"]
    
    def _get_recent_notes(self, count: int = 5):
        """Get recent notes"""
        return sorted(self.notes, key=lambda x: x["timestamp"], reverse=True)[:count]

