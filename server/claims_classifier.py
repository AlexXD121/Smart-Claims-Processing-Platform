import spacy
from datetime import datetime

nlp = spacy.load("en_core_web_sm")

def classify_claim(text: str):
    categories = {
        "Health": ["hospital", "surgery", "medical", "doctor", "treatment", "illness", "clinic"],
        "Vehicle": ["car", "accident", "garage", "repair", "vehicle", "driver", "insurance"],
        "Property": ["house", "flood", "fire", "earthquake", "theft", "damage", "storm"],
        "Travel": ["flight", "luggage", "travel", "visa", "passport", "cancelled", "trip", "hotel"],
        "Life": ["life", "death", "funeral", "survivor", "beneficiary", "claimant"]
    }

    urgency_keywords = ["urgent", "immediately", "emergency", "critical", "asap", "fast-track"]
    lowered_text = text.lower()

    claim_type = "Unknown"
    priority = "Low"
    explanation = "No matching keywords found."
    confidence = 0.4
    confidence_score = 40
    routing_action = "Send to General Claims Queue"
    routing_log = []

    for type_, keywords in categories.items():
        for kw in keywords:
            if kw in lowered_text:
                claim_type = type_
                explanation = f"Matched keyword '{kw}' under '{type_}' category"
                if any(urg in lowered_text for urg in urgency_keywords):
                    priority = "High"
                    confidence = 0.95
                    confidence_score = 95
                else:
                    priority = "Medium"
                    confidence = 0.75
                    confidence_score = 75
                break
        if claim_type != "Unknown":
            break

    doc = nlp(text)
    entities = [{"text": ent.text, "label": ent.label_} for ent in doc.ents]

    routing_table = {
        "Health": "Route to Health Department",
        "Vehicle": "Send to Vehicle Claims Team",
        "Property": "Forward to Property Evaluation Unit",
        "Travel": "Escalate to Travel Support Unit",
        "Life": "Send to Life Insurance Review Desk"
    }

    if claim_type in routing_table:
        routing_action = routing_table[claim_type]

    if priority == "High":
        routing_action += " (Priority Fast-track)"
    elif priority == "Medium":
        routing_action += " (Standard Processing)"
    else:
        routing_action += " (Low Priority Review)"

    routing_log.append({
        "timestamp": datetime.utcnow().isoformat(),
        "action": routing_action,
        "status": "Routed",
        "priority": priority
    })

    violations = check_policy_compliance(text)

    return {
        "type": claim_type,
        "priority": priority,
        "confidence": confidence,
        "confidence_score": confidence_score,
        "rule_explanation": explanation,
        "routing_action": routing_action,
        "routing_log": routing_log,
        "entities": entities,
        "policy_violations": violations
    }

def check_policy_compliance(text):
    violations = []
    policy_rules = {
        "health": {
            "rules": [
                {"id": "H1", "text": "cosmetic surgery"},
                {"id": "H2", "text": "weight loss treatment"},
                {"id": "H3", "text": "experimental treatment"}
            ]
        },
        "vehicle": {
            "rules": [
                {"id": "V1", "text": "drunk driving"},
                {"id": "V2", "text": "no valid license"},
                {"id": "V3", "text": "racing"}
            ]
        },
        "property": {
            "rules": [
                {"id": "P1", "text": "natural disaster"},
                {"id": "P2", "text": "earthquake"},
                {"id": "P3", "text": "flood not covered"}
            ]
        },
        "travel": {
            "rules": [
                {"id": "T1", "text": "non-refundable booking"},
                {"id": "T2", "text": "invalid visa"}
            ]
        },
        "life": {
            "rules": [
                {"id": "L1", "text": "pre-existing condition"},
                {"id": "L2", "text": "suicide clause"}
            ]
        }
    }

    lowered_text = text.lower()
    for category, data in policy_rules.items():
        for rule in data["rules"]:
            if rule["text"] in lowered_text:
                violations.append({
                    "category": category,
                    "violation": rule["text"],
                    "rule_id": rule["id"]
                })

    return violations
