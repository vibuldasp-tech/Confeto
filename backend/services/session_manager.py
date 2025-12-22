"""
Session Manager - Handle session creation, storage, and cleanup
All data is ephemeral and session-based (no persistent storage)
"""

import os
import uuid
import json
import shutil
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime


class SessionManager:
    def __init__(self, sessions_dir: str = "sessions"):
        self.sessions_dir = Path(sessions_dir)
        self.sessions_dir.mkdir(exist_ok=True)
    
    def create_session(self) -> str:
        """Create a new session with unique ID"""
        session_id = str(uuid.uuid4())
        session_dir = self.sessions_dir / session_id
        session_dir.mkdir(exist_ok=True)
        
        # Create session metadata
        metadata = {
            "session_id": session_id,
            "created_at": datetime.utcnow().isoformat(),
            "status": "created"
        }
        
        with open(session_dir / "metadata.json", "w") as f:
            json.dump(metadata, f, indent=2)
        
        return session_id
    
    def session_exists(self, session_id: str) -> bool:
        """Check if session exists"""
        return (self.sessions_dir / session_id).exists()
    
    def get_session_dir(self, session_id: str) -> Path:
        """Get session directory path"""
        return self.sessions_dir / session_id
    
    def save_session_data(self, session_id: str, key: str, data: Any):
        """Save data to session"""
        session_dir = self.get_session_dir(session_id)
        
        with open(session_dir / f"{key}.json", "w") as f:
            json.dump(data, f, indent=2)
    
    def load_session_data(self, session_id: str, key: str) -> Optional[Any]:
        """Load data from session"""
        session_dir = self.get_session_dir(session_id)
        data_file = session_dir / f"{key}.json"
        
        if not data_file.exists():
            return None
        
        with open(data_file, "r") as f:
            return json.load(f)
    
    def delete_session(self, session_id: str):
        """Delete session and all its files"""
        session_dir = self.get_session_dir(session_id)
        
        if session_dir.exists():
            shutil.rmtree(session_dir)
    
    def cleanup_old_sessions(self, max_age_hours: int = 24):
        """Clean up sessions older than specified hours"""
        import time
        current_time = time.time()
        
        for session_dir in self.sessions_dir.iterdir():
            if not session_dir.is_dir():
                continue
            
            # Check age based on directory creation time
            dir_age = current_time - session_dir.stat().st_mtime
            if dir_age > (max_age_hours * 3600):
                shutil.rmtree(session_dir)
