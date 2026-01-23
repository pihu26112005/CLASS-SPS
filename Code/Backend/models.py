import threading
from datetime import datetime
from config import Config


class ParkingLot:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self.parking_lot = Config.INITIAL_PARKING_DATA.copy()
        self.booking_history = []
        self._initialized = True
    
    def get_all_slots(self):
        """Get all parking slots"""
        with self._lock:
            return self.parking_lot.copy()
    
    def get_slot(self, slot_id):
        """Get a specific parking slot"""
        with self._lock:
            return self.parking_lot.get(slot_id)
    
    def slot_exists(self, slot_id):
        """Check if a slot exists"""
        with self._lock:
            return slot_id in self.parking_lot
    
    def is_slot_available(self, slot_id):
        """Check if a slot is available"""
        with self._lock:
            slot = self.parking_lot.get(slot_id)
            return slot["status"] if slot else False
    
    def get_vehicle_slot(self, vehicle_id):
        """Find which slot a vehicle is parked in"""
        with self._lock:
            for slot_id, data in self.parking_lot.items():
                if data["vehicle_id"] == vehicle_id:
                    return slot_id
            return None
    
    def book_slot(self, slot_id, vehicle_id):
        """Book a parking slot"""
        with self._lock:
            timestamp = datetime.now().isoformat()
            self.parking_lot[slot_id]["status"] = False
            self.parking_lot[slot_id]["vehicle_id"] = vehicle_id
            self.parking_lot[slot_id]["booked_at"] = timestamp
            
            # Add to history
            self.booking_history.append({
                "action": "book",
                "slot_id": slot_id,
                "vehicle_id": vehicle_id,
                "timestamp": timestamp
            })
            
            return timestamp
    
    def release_slot(self, slot_id):
        """Release a parking slot"""
        with self._lock:
            vehicle_id = self.parking_lot[slot_id]["vehicle_id"]
            timestamp = datetime.now().isoformat()
            
            self.parking_lot[slot_id]["status"] = True
            self.parking_lot[slot_id]["vehicle_id"] = None
            self.parking_lot[slot_id]["booked_at"] = None
            
            # Add to history
            self.booking_history.append({
                "action": "release",
                "slot_id": slot_id,
                "vehicle_id": vehicle_id,
                "timestamp": timestamp
            })
            
            return vehicle_id
    
    def get_statistics(self):
        """Get parking lot statistics"""
        with self._lock:
            total = len(self.parking_lot)
            available = sum(1 for data in self.parking_lot.values() if data["status"])
            occupied = total - available
            
            return {
                "total": total,
                "available": available,
                "occupied": occupied
            }
    
    def get_available_slots(self):
        """Get list of available slot IDs"""
        with self._lock:
            return [slot_id for slot_id, data in self.parking_lot.items() if data["status"]]
    
    def get_history(self, limit=None):
        """Get booking history"""
        with self._lock:
            if limit:
                return self.booking_history[-limit:]
            return self.booking_history.copy()
