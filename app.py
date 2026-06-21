from flask import Flask, request, jsonify
from repository import DeploymentRepository
from models import DeploymentStatus
from werkzeug.exceptions import HTTPException


app = Flask(__name__)
# Initialize the repository which loads seed_data.json
repo = DeploymentRepository()

@app.route("/deployments", methods=["GET"])
def list_deployments():
    """List deployments with optional filtering by service and/or status."""
    service = request.args.get("service")
    status = request.args.get("status")

    # Validate status parameter if provided
    if status:
        valid_statuses = {s.value for s in DeploymentStatus}
        status = status.lower()
        if status not in valid_statuses:
            return jsonify({
                "error": f"Invalid status parameter. Must be one of: {', '.join(sorted(valid_statuses))}"
            }), 400

    deployments = repo.get_all(service=service, status=status)
    return jsonify([d.to_dict() for d in deployments]), 200

@app.route("/deployments/<string:deployment_id>", methods=["GET"])
def get_deployment(deployment_id):
    """Retrieve details for a single deployment by its ID."""
    deployment = repo.get_by_id(deployment_id)
    if not deployment:
        return jsonify({
            "error": f"Deployment with ID '{deployment_id}' not found"
        }), 404

    return jsonify(deployment.to_dict()), 200

@app.errorhandler(HTTPException)
def handle_http_exception(e):
    return jsonify({"error": e.description}), e.code

@app.errorhandler(Exception)
def handle_unexpected_exception(e):
    app.logger.error(f"Unexpected error: {e}", exc_info=True)
    return jsonify({"error": "An unexpected error occurred"}), 500

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
