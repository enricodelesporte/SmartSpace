from flask import Blueprint, jsonify

api_status_bp = Blueprint("api_status", __name__, url_prefix="/api")


@api_status_bp.get("")
def status_da_aplicacao():
    return jsonify({"aplicacao": "SmartSpace", "status": "online"})
