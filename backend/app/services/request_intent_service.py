from typing import Any, Dict, List
from pydantic import BaseModel
from ..utils import normalize_text


class RequestIntent(BaseModel):
    business_domain: str
    requested_resource: str
    time_granularity: str | None = None
    customer_type: str | None = None
    recommended_datasets: List[str] = []
    suggested_query: str | None = None


def parse_request_text(request_text: str) -> RequestIntent:
    normalized = normalize_text(request_text)

    # structured prompt-style extraction based on common request patterns
    business_domain = "general"
    if "retention" in normalized:
        business_domain = "retention"
    elif "churn" in normalized:
        business_domain = "churn"
    elif "sales" in normalized:
        business_domain = "sales"
    elif "customer" in normalized:
        business_domain = "customer"
    elif "marketing" in normalized:
        business_domain = "marketing"

    time_granularity = None
    for token in ["daily", "weekly", "monthly", "quarterly", "yearly"]:
        if token in normalized:
            time_granularity = token
            break

    customer_type = None
    for token in ["enterprise", "small business", "consumer", "vip", "premium"]:
        if token in normalized:
            customer_type = token
            break

    # recommended query template
    suggested_query = (
        f"SELECT * FROM dataset WHERE business_domain = '{business_domain}'"
    )
    if time_granularity:
        suggested_query += (
            f" AND date_trunc('{time_granularity}', event_timestamp) AS period"
        )
    if customer_type:
        suggested_query += f" AND customer_type = '{customer_type}'"

    return RequestIntent(
        business_domain=business_domain,
        requested_resource=request_text,
        time_granularity=time_granularity,
        customer_type=customer_type,
        recommended_datasets=[],
        suggested_query=suggested_query,
    )
