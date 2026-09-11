import json
import sys
from pathlib import Path

# --------------------------------------------------
# Allow this file to find priority_engine.py
# located in the parent ai folder.
# --------------------------------------------------

AI_FOLDER = Path(__file__).resolve().parent.parent

if str(AI_FOLDER) not in sys.path:
    sys.path.insert(0, str(AI_FOLDER))


from priority_engine import (
    calculate_priority_score,
    get_priority_level
)


def calculate_priorities(disaster_data, needs_data):
    """
    Priority Assessment Agent.

    Uses the shared priority engine so that
    priority calculations remain consistent
    across the entire PS20 system.
    """

    disaster_id = disaster_data.get(
        "disaster",
        {}
    ).get(
        "disaster_id",
        "UNKNOWN"
    )

    zones = disaster_data.get(
        "zones",
        []
    )

    prioritized_zones = []

    # --------------------------------------------------
    # Calculate priority for every zone
    # --------------------------------------------------

    for zone in zones:

        zone_id = zone.get(
            "zone_id",
            "UNKNOWN"
        )

        # Use shared scoring engine
        score = calculate_priority_score(zone)

        # Convert score to priority level
        priority = get_priority_level(score)

        # --------------------------------------------------
        # Build explanation
        # --------------------------------------------------

        factors = []

        severity = zone.get(
            "severity",
            0
        )

        population = zone.get(
            "population_affected",
            0
        )

        trapped = zone.get(
            "people_trapped",
            0
        )

        medical = zone.get(
            "people_needing_medical",
            0
        )

        accessibility = zone.get(
            "accessibility",
            ""
        )

        if severity >= 8:
            factors.append(
                f"high disaster severity ({severity}/10)"
            )

        if population > 0:
            factors.append(
                f"{population} people affected"
            )

        if trapped > 0:
            factors.append(
                f"{trapped} people trapped"
            )

        if medical > 0:
            factors.append(
                f"{medical} people need medical assistance"
            )

        if accessibility.lower() == "blocked":
            factors.append(
                "zone access is blocked"
            )

        if factors:

            reason = (
                f"Priority score {score}/100 based on "
                + ", ".join(factors)
                + "."
            )

        else:

            reason = (
                f"Priority score {score}/100 based on "
                "available zone information."
            )

        prioritized_zones.append({
            "zone_id": zone_id,
            "priority": priority,
            "priority_score": score,
            "reason": reason
        })

    # --------------------------------------------------
    # Sort highest priority first
    # --------------------------------------------------

    prioritized_zones.sort(
        key=lambda x: x["priority_score"],
        reverse=True
    )

    return {
        "disaster_id": disaster_id,
        "prioritized_zones": prioritized_zones
    }


# ==================================================
# LOCAL TEST
# ==================================================

if __name__ == "__main__":

    sample_data = {
        "disaster": {
            "disaster_id": "D001",
            "type": "Flood",
            "location": "Pune",
            "severity": 8
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

    result = calculate_priorities(
        sample_data,
        {}
    )

    print("\n======================================")
    print("      PRIORITY ASSESSMENT")
    print("======================================")

    print(
        json.dumps(
            result,
            indent=2
        )
    )