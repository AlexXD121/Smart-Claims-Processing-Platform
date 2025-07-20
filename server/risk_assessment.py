import re

def assess_risk(text):
    """
    Assess risk based on presence of certain keywords in the text.
    Returns risk score, risk level, and reasons.
    """

    risk_score = 0
    reasons = []

    # Define risk rules with keywords and their scores
    # Use regex patterns to ensure whole word matching, case insensitive
    risk_rules = {
        r"\bcrack(s|ed)?\b": 2,
        r"\bleak(age|ing)?\b": 3,
        r"\bdamp\b": 2,
        r"\bfire\b": 4,
        r"\bold building\b": 1,
        r"\bshort[- ]circuit\b": 3,
    }

    text_lower = text.lower()

    try:
        for pattern, score in risk_rules.items():
            if re.search(pattern, text_lower):
                keyword = re.findall(pattern, text_lower)
                # For reasons, use simplified readable form of keyword from pattern keys
                reason_keyword = pattern.strip(r"\b").replace(r"(s|ed)?", "").replace(r"(age|ing)?", "").replace(r"\\b", "").replace(r"\\", "")
                reasons.append(f"Detected risk factor: '{reason_keyword}' (+{score} points)")
                risk_score += score

        # Determine risk level
        if risk_score >= 5:
            status = "High"
        elif risk_score >= 3:
            status = "Medium"
        else:
            status = "Low"

    except Exception as e:
        # Return error info in reasons in case of failure
        return {
            "risk_score": risk_score,
            "risk_level": "Unknown",
            "reasons": [f"Error assessing risk: {str(e)}"]
        }

    return {
        "risk_score": risk_score,
        "risk_level": status,
        "reasons": reasons if reasons else ["No significant risk factors detected."]
    }
