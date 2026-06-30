from datetime import datetime
import uuid


def get_current_timestamp():
    """
    Returns current UTC timestamp
    """
    return datetime.utcnow()


def generate_unique_id():
    """
    Generate a unique request ID
    """
    return str(uuid.uuid4())


def normalize_text(text: str):
    """
    Clean and normalize user input
    """
    if not text:
        return ""

    return text.strip().lower()


def is_sensitive_dataset(sensitivity: str):
    """
    Check if dataset requires approval
    """

    sensitive_levels = ["pii", "restricted", "confidential", "sensitive"]

    return normalize_text(sensitivity) in sensitive_levels


def format_audit_message(action: str, user: str, resource: str):
    """
    Create standard audit log message
    """

    return (
        f"Action={action}, "
        f"User={user}, "
        f"Resource={resource}, "
        f"Time={get_current_timestamp()}"
    )


def validate_access_duration(days: int):
    """
    Validate temporary access duration
    """

    if days <= 0:
        raise ValueError("Access duration must be greater than zero")

    if days > 90:
        raise ValueError("Access duration cannot exceed 90 days")

    return True


def create_api_response(status: str, message: str, data=None):
    """
    Standard API response format
    """

    return {
        "status": status,
        "message": message,
        "data": data,
        "timestamp": str(get_current_timestamp()),
    }
