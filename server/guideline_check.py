import re

def check_guideline_compliance(text):
    """
    Check underwriting guideline compliance in the extracted text.
    Returns:
      - overall_status: 'Compliant', 'Non-Compliant', or 'Partial'
      - details: dict with rule keys and their compliance status/messages
    """

    text_lower = text.lower()

    # Define rules with expected patterns or checks
    rules = {
        "fire extinguisher": {
            "description": "Must be present",
            "pattern": r"fire extinguisher",
            "check": lambda txt: bool(re.search(r"fire extinguisher", txt)),
        },
        "electrical inspection": {
            "description": "Must be recent (within last 12 months)",
            # Looking for "electrical inspection" + recent year or date
            "pattern": r"electrical inspection.*(20\d{2}|recent|last\s+\d+\s+months?)",
            "check": lambda txt: bool(re.search(r"electrical inspection.*(20\d{2}|recent|last\s+\d+\s+months?)", txt)),
        },
        "construction type": {
            "description": "Should be 'Masonry' or 'Frame'",
            "pattern": r"construction type[:\-]?\s*(masonry|frame)",
            "check": lambda txt: bool(re.search(r"construction type[:\-]?\s*(masonry|frame)", txt)),
        },
        "roof condition": {
            "description": "Should not be 'Poor'",
            "pattern": r"roof condition[:\-]?\s*(poor)",
            # Check returns True if condition is NOT poor
            "check": lambda txt: not bool(re.search(r"roof condition[:\-]?\s*poor", txt)),
        },
    }

    compliance_results = {}
    compliant_count = 0
    total_rules = len(rules)

    for key, rule in rules.items():
        try:
            if rule["check"](text_lower):
                compliance_results[key] = f"✅ Compliant - {rule['description']}"
                compliant_count += 1
            else:
                compliance_results[key] = f"⚠️ Non-compliant or missing: {rule['description']}"
        except Exception as e:
            compliance_results[key] = f"❌ Error checking rule: {str(e)}"

    # Determine overall status
    if compliant_count == total_rules:
        overall_status = "Compliant"
    elif compliant_count == 0:
        overall_status = "Non-Compliant"
    else:
        overall_status = "Partial Compliance"

    return {
        "overall_status": overall_status,
        "details": compliance_results
    }
