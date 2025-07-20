import re
import traceback

def extract_relevant_info(text):
    try:
        extracted = {}

        # Define regex patterns for each field
        patterns = {
            "Name": r"Name[:\-]?\s*([A-Za-z ,.'-]+)",
            "Date": r"Date[:\-]?\s*((?:[0-9]{2}[/\-][0-9]{2}[/\-][0-9]{4})|(?:[0-9]{4}[/\-][0-9]{2}[/\-][0-9]{2}))",
            "Claim Amount": r"Claim Amount[:\-]?\s*₹?\s*([\d,]+(?:\.\d{1,2})?)",
            "Policy Number": r"Policy Number[:\-]?\s*(\w+)",
        }

        for key, pattern in patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                value = match.group(1).strip()

                # Normalize Claim Amount by removing commas
                if key == "Claim Amount":
                    value = value.replace(',', '')

                extracted[key] = value

        # If nothing found, return error dict
        return extracted if extracted else {"error": "No relevant data extracted"}

    except Exception as e:
        print("❌ Info extraction error:", str(e))
        traceback.print_exc()
        return {"error": f"Regex parsing failed: {str(e)}"}
