from typing import Dict


def provision_database_access(request_id: int, dataset_name: str, provision_details: Dict) -> Dict:
    # Simulated provisioning payload for a warehouse
    return {
        "request_id": request_id,
        "dataset": dataset_name,
        "status": "PROVISIONED",
        "details": {
            "warehouse": provision_details.get("warehouse", "snowflake") ,
            "grant_type": provision_details.get("grant_type", "READ"),
            "expires_in_days": provision_details.get("expires_in_days", 30)
        }
    }


def revoke_database_access(request_id: int, dataset_name: str) -> Dict:
    return {
        "request_id": request_id,
        "dataset": dataset_name,
        "status": "REVOKED"
    }
