from flask import Blueprint, request, jsonify
from services import ParkingService

# Create blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api')

# Initialize service
parking_service = ParkingService()


@api_bp.route('/parking/status', methods=['GET'])
def get_parking_status():
    """Get current status of all parking slots"""
    result = parking_service.get_parking_status()
    return jsonify({
        "success": True,
        "slots": result["slots"],
        "available_count": result["available_count"],
        "total_count": result["total_count"]
    }), 200


@api_bp.route('/parking/book', methods=['POST'])
def book_parking_slot():
    """Book a parking slot"""
    data = request.get_json()
    
    slot_id = data.get('slot_id') if data else None
    vehicle_id = data.get('vehicle_id') if data else None
    
    result = parking_service.book_parking_slot(slot_id, vehicle_id)
    status_code = result.pop('status_code', 200)
    
    return jsonify(result), status_code


@api_bp.route('/parking/release', methods=['POST'])
def release_parking_slot():
    """Release a parking slot"""
    data = request.get_json()
    
    slot_id = data.get('slot_id') if data else None
    
    result = parking_service.release_parking_slot(slot_id)
    status_code = result.pop('status_code', 200)
    
    return jsonify(result), status_code


@api_bp.route('/parking/history', methods=['GET'])
def get_booking_history():
    """Get booking history"""
    result = parking_service.get_booking_history()
    status_code = result.pop('status_code', 200)
    
    return jsonify(result), status_code


@api_bp.route('/parking/available', methods=['GET'])
def get_available_slots():
    """Get all available slots"""
    result = parking_service.get_available_slots()
    status_code = result.pop('status_code', 200)
    
    return jsonify(result), status_code


@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "success": True,
        "message": "Smart Parking System API is running"
    }), 200
