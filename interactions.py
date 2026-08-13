# Known dangerous drug interaction pairs (educational/demo dataset)
# In a real product, this would come from a verified medical database
KNOWN_INTERACTIONS = {
    frozenset(["Ibuprofen", "Aspirin"]): "Increased risk of stomach bleeding when combined.",
    frozenset(["Paracetamol", "Warfarin"]): "May increase bleeding risk with prolonged use.",
    frozenset(["Amoxicillin", "Metformin"]): "May reduce effectiveness of Metformin.",
    frozenset(["Ibuprofen", "Metformin"]): "May affect kidney function when combined.",
    frozenset(["Omeprazole", "Amoxicillin"]): "Generally safe, but monitor for reduced absorption.",
    frozenset(["Cetirizine", "Amlodipine"]): "May cause increased drowsiness or low blood pressure.",
}


def check_interactions(medicine_names):
    """
    Given a list of medicine names in a prescription,
    checks every possible pair against known dangerous combinations.
    Returns a list of warning messages.
    """
    warnings = []
    medicine_names = list(set(medicine_names))  # remove duplicates

    for i in range(len(medicine_names)):
        for j in range(i + 1, len(medicine_names)):
            pair = frozenset([medicine_names[i], medicine_names[j]])
            if pair in KNOWN_INTERACTIONS:
                warnings.append({
                    "medicines": f"{medicine_names[i]} + {medicine_names[j]}",
                    "warning": KNOWN_INTERACTIONS[pair]
                })

    return warnings