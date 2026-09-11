import json


def assess_needs(disaster_data):
    """
    Deterministic Needs Assessment Agent.

    Converts reported zone conditions into clear resource requirements.
    No external AI/API call is required.
    """

    disaster_id = disaster_data.get("disaster", {}).get("disaster_id", "UNKNOWN")
    zones = disaster_data.get("zones", [])

    zone_needs = []

    for zone in zones:
        zone_id = zone.get("zone_id", "UNKNOWN")

        population = zone.get("population_affected", 0)
        medical = zone.get("people_needing_medical", 0)
        food = zone.get("people_needing_food", 0)
        shelter = zone.get("people_needing_shelter", 0)
        trapped = zone.get("people_trapped", 0)
        accessibility = zone.get("accessibility", "Unknown")
        severity = zone.get("severity", 0)

        critical_needs = []

        if trapped > 0:
            critical_needs.append("Rescue")

        if medical > 0:
            critical_needs.append("Medical assistance")

        if food > 0:
            critical_needs.append("Food")

        if shelter > 0:
            critical_needs.append("Shelter")

        if accessibility.lower() == "blocked":
            critical_needs.append("Access clearance")

        if severity >= 8:
            critical_needs.append("Immediate emergency response")

        reasons = []

        if population > 0:
            reasons.append(f"{population} people are affected")

        if medical > 0:
            reasons.append(f"{medical} people need medical assistance")

        if food > 0:
            reasons.append(f"{food} people need food")

        if shelter > 0:
            reasons.append(f"{shelter} people need shelter")

        if trapped > 0:
            reasons.append(f"{trapped} people are trapped")

        if accessibility.lower() == "blocked":
            reasons.append("access to the zone is blocked")

        if severity >= 8:
            reasons.append(f"severity is {severity}/10")

        assessment_reason = "; ".join(reasons) + "."

        zone_needs.append({
            "zone_id": zone_id,
            "food_required": food,
            "medical_required": medical,
            "shelter_required": shelter,
            "rescue_required": trapped,
            "critical_needs": critical_needs,
            "assessment_reason": assessment_reason
        })

    return {
        "disaster_id": disaster_id,
        "zone_needs": zone_needs
    }


# --------------------------------------------------
# LOCAL TEST
# --------------------------------------------------

if __name__ == "__main__":

    sample_data = {
        "disaster": {
            "disaster_id": "D001",
            "type": "Flood",
            "location": "Pune",
            "severity": 8,
            "description": "Heavy flooding has affected multiple areas",
            "timestamp": "2026-09-11T10:30:00Z"
        },

        "zones": [
            {
                "zone_id": "Z001",
                "name": "Zone A",
                "population_affected": 5000,
                "severity": 9,
                "people_needing_medical": 800,
                "people_needing_food": 4000,
                "people_needing_shelter": 3000,
                "people_trapped": 200,
                "accessibility": "Blocked"
            },
            {
                "zone_id": "Z002",
                "name": "Zone B",
                "population_affected": 3000,
                "severity": 6,
                "people_needing_medical": 200,
                "people_needing_food": 2500,
                "people_needing_shelter": 1500,
                "people_trapped": 20,
                "accessibility": "Accessible"
            }
        ]
    }

    result = assess_needs(sample_data)

    print("\n===== NEEDS ASSESSMENT =====")
    print(json.dumps(result, indent=2))