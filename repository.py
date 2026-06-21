import json
import os
from typing import List, Optional
from models import Deployment

class DeploymentRepository:
    def __init__(self, filepath: str = "seed_data.json"):
        self.filepath = filepath
        self._deployments: List[Deployment] = []
        self._load_data()

    def _load_data(self):
        """Loads data from the seed file and populates the in-memory store."""
        if not os.path.exists(self.filepath):
            # Attempt to locate relative to this file's folder
            base_dir = os.path.dirname(os.path.abspath(__file__))
            alternative_path = os.path.join(base_dir, self.filepath)
            if os.path.exists(alternative_path):
                self.filepath = alternative_path
            else:
                raise FileNotFoundError(
                    f"Seed data file not found at {self.filepath} or {alternative_path}. "
                    "Please run generate_seed_data.py first."
                )

        with open(self.filepath, "r") as f:
            data = json.load(f)
            self._deployments = [Deployment.from_dict(item) for item in data]

    def get_all(self, service: Optional[str] = None, status: Optional[str] = None) -> List[Deployment]:
        """Get all deployments, with optional filtering by service and/or status."""
        filtered = self._deployments
        
        if service:
            filtered = [d for d in filtered if d.service.lower() == service.lower()]
            
        if status:
            filtered = [d for d in filtered if d.status.value.lower() == status.lower()]
            
        return filtered

    def get_by_id(self, deployment_id: str) -> Optional[Deployment]:
        """Find a single deployment by ID."""
        for d in self._deployments:
            if d.id == deployment_id:
                return d
        return None
