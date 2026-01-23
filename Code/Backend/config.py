class Config:
    # Flask Configuration
    DEBUG = True
    HOST = '0.0.0.0'
    PORT = 5000
    
    # CORS Configuration
    CORS_ORIGINS = '*'
    
    # Parking Lot Configuration
    INITIAL_PARKING_DATA = {
        "A1": {"status": True, "vehicle_id": None, "booked_at": None},
        "A2": {"status": True, "vehicle_id": None, "booked_at": None},
        "B1": {"status": True, "vehicle_id": None, "booked_at": None},
        "B2": {"status": True, "vehicle_id": None, "booked_at": None},
        "C1": {"status": True, "vehicle_id": None, "booked_at": None},
        "C2": {"status": True, "vehicle_id": None, "booked_at": None},
    }
    
    # History Configuration
    MAX_HISTORY_ENTRIES = 20
