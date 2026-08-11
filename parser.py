import re

def parse_dosage_info(text_line):
    text_line = text_line.lower()

    result = {
        "frequency": None,
        "food_timing": None,
        "duration_days": None
    }

    # --- Detect frequency pattern (e.g., "1 morning, 1 night") ---
    time_words = []
    if re.search(r'\bmorning\b|\bmorn\b', text_line):
        time_words.append("Morning")
    if re.search(r'\bafternoon\b|\baft\b', text_line):
        time_words.append("Afternoon")
    if re.search(r'\bevening\b|\beve\b', text_line):
        time_words.append("Evening")
    if re.search(r'\bnight\b', text_line):
        time_words.append("Night")

    if time_words:
        result["frequency"] = ", ".join(time_words)

    # --- Detect general frequency phrases like "twice daily", "once a day" ---
    if not result["frequency"]:
        if re.search(r'once\s+(a\s+)?day|once\s+daily', text_line):
            result["frequency"] = "Once daily"
        elif re.search(r'twice\s+(a\s+)?day|twice\s+daily', text_line):
            result["frequency"] = "Twice daily"
        elif re.search(r'thrice\s+(a\s+)?day|three\s+times\s+(a\s+)?day|thrice\s+daily', text_line):
            result["frequency"] = "Thrice daily"

    # --- Detect food timing ---
    if re.search(r'before\s+food', text_line):
        result["food_timing"] = "Before Food"
    elif re.search(r'after\s+food', text_line):
        result["food_timing"] = "After Food"

    # --- Detect duration (e.g., "10 days", "5 day") ---
    duration_match = re.search(r'(\d+)\s*day', text_line)
    if duration_match:
        result["duration_days"] = int(duration_match.group(1))

    return result