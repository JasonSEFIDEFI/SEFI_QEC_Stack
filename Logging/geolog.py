import time

def log_event(event_type, details):
    """
    SEFI Geometric Log
    Records events with timestamps and structured details.
    """
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {event_type}: {details}")
