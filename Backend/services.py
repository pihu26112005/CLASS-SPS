from models import ParkingLot

class ParkingService:
    def __init__(self):
        self.parking_lot = ParkingLot()
    
    def get_parking_status(self):
        """Get current status of all parking slots"""
        slots = self.parking_lot.get_all_slots()
        stats = self.parking_lot.get_statistics()
        
        formatted_slots = []
        for slot_id, data in slots.items():
            formatted_slots.append({
                "slot_id": slot_id,
                "status": "available" if data["status"] else "occupied",
                "vehicle_id": data["vehicle_id"],
                "booked_at": data["booked_at"]
            })
        
        return {
            "slots": formatted_slots,
            "available_count": stats["available"],
            "total_count": stats["total"]
        }
    
    def book_parking_slot(self, slot_id, vehicle_id):
        """Book a parking slot with validation"""
        # Validate inputs
        if not slot_id or not vehicle_id:
            return {
                "success": False,
                "message": "Missing slot_id or vehicle_id",
                "status_code": 400
            }
        
        slot_id = slot_id.strip().upper()
        vehicle_id = vehicle_id.strip()
        
        if not vehicle_id:
            return {
                "success": False,
                "message": "Vehicle ID cannot be empty",
                "status_code": 400
            }
        
        # Check if slot exists
        if not self.parking_lot.slot_exists(slot_id):
            return {
                "success": False,
                "message": f"Slot '{slot_id}' does not exist",
                "status_code": 404
            }
        
        # Check if slot is available
        if not self.parking_lot.is_slot_available(slot_id):
            return {
                "success": False,
                "message": f"Slot '{slot_id}' is already occupied",
                "status_code": 409
            }
        
        # Check if vehicle is already parked
        existing_slot = self.parking_lot.get_vehicle_slot(vehicle_id)
        if existing_slot:
            return {
                "success": False,
                "message": f"Vehicle '{vehicle_id}' is already parked in slot '{existing_slot}'",
                "status_code": 409
            }
        
        # Book the slot
        timestamp = self.parking_lot.book_slot(slot_id, vehicle_id)
        
        return {
            "success": True,
            "message": f"Slot '{slot_id}' successfully booked for vehicle '{vehicle_id}'",
            "slot_id": slot_id,
            "vehicle_id": vehicle_id,
            "booked_at": timestamp,
            "status_code": 200
        }
    
    def release_parking_slot(self, slot_id):
        """Release a parking slot with validation"""
        # Validate input
        if not slot_id:
            return {
                "success": False,
                "message": "Missing slot_id",
                "status_code": 400
            }
        
        slot_id = slot_id.strip().upper()
        
        # Check if slot exists
        if not self.parking_lot.slot_exists(slot_id):
            return {
                "success": False,
                "message": f"Slot '{slot_id}' does not exist",
                "status_code": 404
            }
        
        # Check if slot is occupied
        if self.parking_lot.is_slot_available(slot_id):
            return {
                "success": False,
                "message": f"Slot '{slot_id}' is already available",
                "status_code": 409
            }
        
        # Release the slot
        vehicle_id = self.parking_lot.release_slot(slot_id)
        
        return {
            "success": True,
            "message": f"Slot '{slot_id}' has been released",
            "slot_id": slot_id,
            "vehicle_id": vehicle_id,
            "status_code": 200
        }
    
    def get_booking_history(self, limit=20):
        """Get booking history"""
        history = self.parking_lot.get_history(limit)
        
        return {
            "success": True,
            "history": history,
            "status_code": 200
        }
    
    def get_available_slots(self):
        """Get all available slots"""
        available_slots = self.parking_lot.get_available_slots()
        
        return {
            "success": True,
            "available_slots": available_slots,
            "count": len(available_slots),
            "status_code": 200
        }
