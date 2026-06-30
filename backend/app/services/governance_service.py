from typing import Dict

from ..utils import is_sensitive_dataset


def determine_approval_path(dataset_metadata: Dict) -> Dict[str, str]:
    sensitivity = dataset_metadata.get("sensitivity", "public").lower()
    access_level = dataset_metadata.get("access_level", "read").lower()

    if sensitivity == "public":
        return {"approval_required": "none", "workflow": "auto_approve"}
    if sensitivity in ["confidential", "restricted", "pii", "sensitive"]:
        if access_level == "read":
            return {
                "approval_required": "manager_and_de",
                "workflow": "governance_review",
            }
        return {"approval_required": "security_and_de", "workflow": "security_review"}

    return {"approval_required": "manager", "workflow": "standard_review"}


def evaluate_access_request(request_meta: Dict) -> Dict[str, bool]:
    return {
        "is_sensitive": is_sensitive_dataset(request_meta.get("sensitivity", "public")),
        "requires_approval": request_meta.get("sensitivity", "public").lower()
        != "public",
        "requires_data_governance": request_meta.get("sensitivity", "public").lower()
        in ["pii", "restricted", "confidential"],
    }
