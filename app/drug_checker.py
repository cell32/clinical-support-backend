# app/drug_checker.py

def check_interactions(drugs):
    known_interactions = {
        ("aspirin", "ibuprofen"): "Increased risk of bleeding",
        ("lisinopril", "potassium supplements"): "Risk of high potassium levels",
        ("metformin", "alcohol"): "Increased risk of lactic acidosis",
        ("warfarin", "antibiotics"): "May increase bleeding risk",
    }

    interactions_found = []

    # Normalize and clean drug names
    drug_list = [d.strip().lower() for d in drugs]

    for (drug1, drug2), interaction in known_interactions.items():
        if drug1 in drug_list and drug2 in drug_list:
            interactions_found.append({
                "drugs": f"{drug1} + {drug2}",
                "interaction": interaction
            })

    return interactions_found
