import os
import json
from typing import Dict, Callable


class Agent:
    """Simple rule-based agent with pluggable actions.

    Rules are simple lambdas that take metrics dict and return boolean.
    Actions are callables that will be executed when rule matches.
    """

    def __init__(self):
        self.rules = []  # list of (name, predicate, action)

    def add_rule(self, name: str, predicate: Callable[[Dict], bool], action: Callable[[Dict], None]):
        self.rules.append((name, predicate, action))

    def evaluate(self, metrics: Dict):
        decisions = []
        for name, pred, action in self.rules:
            try:
                if pred(metrics):
                    action(metrics)
                    decisions.append({"rule": name, "action": getattr(action, "__name__", "<action>")})
            except Exception as e:
                decisions.append({"rule": name, "error": str(e)})
        return decisions


def dedupe_action(metrics: Dict):
    # Placeholder: write a flag file that dedupe was requested
    out = metrics.get("__out_dir", "./data/agent")
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, "dedupe.trigger"), "w", encoding="utf-8") as f:
        json.dump({"triggered_at": metrics.get("run_at"), "reason": "high_duplicate_rate"}, f)


def alert_action(metrics: Dict):
    out = metrics.get("__out_dir", "./data/agent")
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, "alert.trigger"), "w", encoding="utf-8") as f:
        json.dump({"triggered_at": metrics.get("run_at"), "reason": "schema_drift"}, f)


def investigation_action(metrics: Dict):
    out = metrics.get("__out_dir", "./data/agent")
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, "investigation.trigger"), "w", encoding="utf-8") as f:
        json.dump({"triggered_at": metrics.get("run_at"), "reason": "anomaly_spike"}, f)


def default_agent_setup() -> Agent:
    a = Agent()
    # Rule: duplicate rate > 0.2
    a.add_rule("high_duplicate_rate", lambda m: (m.get("duplicate_pct", 0) > 0.2), dedupe_action)
    # Rule: schema drift flag
    a.add_rule("schema_drift", lambda m: m.get("schema_drift", False), alert_action)
    # Rule: anomaly spike
    a.add_rule("anomaly_spike", lambda m: (m.get("anomalies", 0) > m.get("anomaly_baseline", 100)), investigation_action)
    return a


if __name__ == "__main__":
    a = default_agent_setup()
    metrics = {"duplicate_pct": 0.25, "run_at": "now", "anomalies": 5, "anomaly_baseline": 1}
    print(a.evaluate(metrics))
