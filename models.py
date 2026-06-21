from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any

class DeploymentStatus(str, Enum):
    QUEUED = "queued"
    IN_PROGRESS = "in_progress"
    SUCCESS = "success"
    FAILED = "failed"

@dataclass
class Deployment:
    id: str
    service: str
    status: DeploymentStatus
    duration: int
    timestamp: str  # ISO-8601 formatted string
    commit_sha: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert Deployment instance to a dictionary for JSON serialization."""
        return {
            "id": self.id,
            "service": self.service,
            "status": self.status.value,
            "duration": self.duration,
            "timestamp": self.timestamp,
            "commit_sha": self.commit_sha
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Deployment":
        """Create a Deployment instance from a dictionary."""
        return cls(
            id=data["id"],
            service=data["service"],
            status=DeploymentStatus(data["status"]),
            duration=data["duration"],
            timestamp=data["timestamp"],
            commit_sha=data["commit_sha"]
        )
