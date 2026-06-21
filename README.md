# Deployments Backend Project

A lightweight backend service built with Flask to manage, filter, and retrieve deployment history.

## Setup

Follow these steps to set up and run the project locally:

```bash
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

## Regenerating Seed Data

There is already a file `seed_data.json` with mock data. This generation script is just for reference purpose. If you want to regenerate the seed data, run:

```bash
python generate_seed_data.py
```

This will run [generate_seed_data.py](generate_seed_data.py) and output the results directly to `seed_data.json` which the repository loads at startup.

## API Reference

### 1. List Deployments

Retrieve a list of all deployments with optional filters.

- **URL:** `/deployments`
- **Method:** `GET`
- **Query Parameters:**
  - `service` (optional): Filter deployments by service name.
    - Example values: `billing-api`, `auth-service`, `frontend-app`, `notifications-worker`
  - `status` (optional): Filter deployments by current status.
    - Expected values: `queued`, `in_progress`, `success`, `failed`
- **Response Examples:**
  - **Success (`200 OK`):**
    ```json
    [
      {
        "commit_sha": "3766e4",
        "duration": 191,
        "id": "deploy_131",
        "service": "billing-api",
        "status": "success",
        "timestamp": "2026-06-02T07:04:57Z"
      }
    ]
    ```
  - **Error (`400 Bad Request`):**
    ```json
    {
      "error": "Invalid status parameter. Must be one of: failed, in_progress, queued, success"
    }
    ```

### 2. Get Single Deployment

Retrieve detailed information about a specific deployment by its ID.

- **URL:** `/deployments/<deployment_id>`
- **Method:** `GET`
- **Path Parameters:**
  - `deployment_id` (string): The ID of the deployment.
- **Response Examples:**
  - **Success (`200 OK`):**
    ```json
    {
      "commit_sha": "3766e4",
      "duration": 191,
      "id": "deploy_131",
      "service": "billing-api",
      "status": "success",
      "timestamp": "2026-06-02T07:04:57Z"
    }
    ```
  - **Error (`404 Not Found`):**
    ```json
    {
      "error": "Deployment with ID 'deploy_999' not found"
    }
    ```
