import json
import random
from datetime import datetime, timezone, timedelta
from faker import Faker
from models import DeploymentStatus

# Initialize Faker and seed for reproducibility
fake = Faker()
Faker.seed(42)
random.seed(42)

SERVICES = ["billing-api", "auth-service", "frontend-app", "notifications-worker"]

def generate_deployments(count: int = 40) -> list:
    deployments = []
    
    # Start time for fake deployments (incrementing within June 2026)
    start_time = datetime(2026, 6, 1, tzinfo=timezone.utc)
    
    for i in range(count):
        dep_id = f"deploy_{100 + i}"
        
        # Select service
        service = random.choice(SERVICES)
        
        # High failure rate for "auth-service" (~60%), low for others (~10%)
        if service == "auth-service":
            status = random.choices(
                [DeploymentStatus.SUCCESS, DeploymentStatus.FAILED, DeploymentStatus.IN_PROGRESS, DeploymentStatus.QUEUED],
                weights=[25, 60, 10, 5],
                k=1
            )[0]
        else:
            status = random.choices(
                [DeploymentStatus.SUCCESS, DeploymentStatus.FAILED, DeploymentStatus.IN_PROGRESS, DeploymentStatus.QUEUED],
                weights=[80, 10, 5, 5],
                k=1
            )[0]
            
        # Determine duration
        # We will make the 25th deployment (index 24) a clear duration outlier for "billing-api"
        if i == 24:
            service = "billing-api"
            status = DeploymentStatus.SUCCESS
            duration = 7200  # 2 hours (outlier)
        else:
            if status in (DeploymentStatus.QUEUED, DeploymentStatus.IN_PROGRESS):
                duration = random.randint(5, 30)
            else:
                # normal average is around 30 to 240 seconds
                duration = random.randint(30, 240)
                
        # Generate timestamp within the first 20 days of June
        time_offset = timedelta(
            days=random.randint(0, 19), 
            hours=random.randint(0, 23), 
            minutes=random.randint(0, 59),
            seconds=random.randint(0, 59)
        )
        timestamp = (start_time + time_offset).isoformat().replace("+00:00", "Z")
        
        # 6-character commit hash
        commit_sha = fake.hexify(text="^^^^^^")
        
        deployments.append({
            "id": dep_id,
            "service": service,
            "status": status.value,
            "duration": duration,
            "timestamp": timestamp,
            "commit_sha": commit_sha
        })
        
    # Sort deployments by timestamp so they are in chronological order
    deployments.sort(key=lambda x: x["timestamp"])
    
    return deployments

def main():
    data = generate_deployments(40)
    output_file = "seed_data.json"
    
    with open(output_file, "w") as f:
        json.dump(data, f, indent=2)
        
    print(f"Successfully generated {len(data)} deployments and saved to {output_file}")

if __name__ == "__main__":
    main()
