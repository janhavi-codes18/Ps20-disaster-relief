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


def reassess_situation(
    disaster_data,
    current_allocations,
    new_reports
):
    """
    Reallocation Agent.

    Detects new emergencies, recalculates the affected
    zone's priority using the SAME priority engine used
    by the Priority Agent, and recommends safe resource
    reallocation.

    No external AI/API call is required.
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

    # --------------------------------------------------
    # If there are no new reports
    # --------------------------------------------------

    if not new_reports:

        return {
            "disaster_id": disaster_id,
            "reallocation_needed": False,
            "priority_changes": [],
            "reallocations": [],
            "duplicate_efforts": [],
            "alerts": [],
            "explanation": {
                "summary": "No new emergency reports detected.",
                "key_factors": []
            }
        }

    # --------------------------------------------------
    # Create independent copies of zone data
    # --------------------------------------------------

    updated_zones = [
        dict(zone)
        for zone in zones
    ]

    zone_lookup = {
        zone.get("zone_id"): zone
        for zone in updated_zones
    }

    priority_changes = []
    reallocations = []
    duplicate_efforts = []
    alerts = []

    # ==================================================
    # 1. PROCESS NEW EMERGENCY REPORTS
    # ==================================================

    for report in new_reports:

        zone_id = report.get("zone_id")

        if zone_id not in zone_lookup:
            continue

        zone = zone_lookup[zone_id]

        # ----------------------------------------------
        # Save old zone state
        # ----------------------------------------------

        old_zone = dict(zone)

        old_score = calculate_priority_score(
            old_zone
        )

        old_priority = get_priority_level(
            old_score
        )

        # ----------------------------------------------
        # Apply emergency changes
        # ----------------------------------------------

        severity_change = report.get(
            "severity_change",
            0
        )

        zone["severity"] = min(
            zone.get("severity", 0) + severity_change,
            10
        )

        # Optional additional emergency information
        if "people_trapped" in report:

            zone["people_trapped"] = max(
                zone.get("people_trapped", 0),
                report["people_trapped"]
            )

        if "additional_medical_needed" in report:

            zone["people_needing_medical"] = (
                zone.get(
                    "people_needing_medical",
                    0
                )
                + report["additional_medical_needed"]
            )

        # ----------------------------------------------
        # Calculate NEW priority using shared engine
        # ----------------------------------------------

        new_score = calculate_priority_score(
            zone
        )

        # A NEW_EMERGENCY itself is an additional
        # urgency signal.
        if report.get("type") == "NEW_EMERGENCY":

            new_score = min(
                new_score + 25,
                100
            )

        new_priority = get_priority_level(
            new_score
        )

        # ----------------------------------------------
        # Detect priority change
        # ----------------------------------------------

        if (
            new_score > old_score
            or new_priority != old_priority
        ):

            priority_changes.append({
                "zone_id": zone_id,
                "old_priority": old_priority,
                "new_priority": new_priority,
                "reason": (
                    f"New emergency report detected. "
                    f"Priority score changed from "
                    f"{old_score}/100 to "
                    f"{new_score}/100."
                )
            })

            alerts.append({
                "alert_id": f"A{len(alerts) + 1:03d}",
                "type": "NEW_EMERGENCY",
                "severity": new_priority,
                "zone_id": zone_id,
                "message": (
                    f"New emergency detected in {zone_id}. "
                    f"Priority increased from "
                    f"{old_priority} to "
                    f"{new_priority}."
                )
            })

    # ==================================================
    # 2. DETERMINE IF REALLOCATION IS REQUIRED
    # ==================================================

    reallocation_needed = (
        len(priority_changes) > 0
    )

    # ==================================================
    # 3. DYNAMIC RESOURCE REALLOCATION
    # ==================================================

    if reallocation_needed:

        for change in priority_changes:

            target_zone_id = change["zone_id"]

            target_zone = zone_lookup.get(
                target_zone_id,
                {}
            )

            new_priority = change["new_priority"]

            # Only redirect resources for HIGH
            # or CRITICAL emergencies.
            if new_priority not in [
                "HIGH",
                "CRITICAL"
            ]:
                continue

            # ------------------------------------------
            # Search current allocations
            # ------------------------------------------

            for allocation in current_allocations:

                source_zone_id = allocation.get(
                    "zone_id"
                )

                resource_type = allocation.get(
                    "resource_type"
                )

                quantity = allocation.get(
                    "quantity",
                    0
                )

                resource_id = allocation.get(
                    "resource_id"
                )

                unit = allocation.get(
                    "unit",
                    ""
                )

                # Never move resources inside same zone
                if source_zone_id == target_zone_id:
                    continue

                if quantity <= 0:
                    continue

                # --------------------------------------
                # Check resource suitability
                # --------------------------------------

                suitable = False

                if resource_type == "Food":

                    suitable = (
                        target_zone.get(
                            "people_needing_food",
                            0
                        ) > 0
                    )

                elif resource_type == "Medical":

                    suitable = (
                        target_zone.get(
                            "people_needing_medical",
                            0
                        ) > 0
                    )

                elif resource_type == "Shelter":

                    suitable = (
                        target_zone.get(
                            "people_needing_shelter",
                            0
                        ) > 0
                    )

                if not suitable:
                    continue

                # --------------------------------------
                # Move 20% of source allocation
                # --------------------------------------

                move_quantity = max(
                    1,
                    round(quantity * 0.20)
                )

                move_quantity = min(
                    move_quantity,
                    quantity
                )

                reallocations.append({
                    "resource_id": resource_id,
                    "from_zone_id": source_zone_id,
                    "to_zone_id": target_zone_id,
                    "quantity": move_quantity,
                    "unit": unit,
                    "reason": (
                        f"20% of the existing "
                        f"{resource_type} allocation is "
                        f"redirected to {target_zone_id} "
                        f"because a new "
                        f"{new_priority.lower()} "
                        f"emergency was reported."
                    ),
                    "urgency": new_priority
                })

                # One controlled reallocation per
                # priority change for demo clarity.
                break

    # ==================================================
    # 4. DUPLICATE EFFORT DETECTION
    # ==================================================

    seen = set()

    for allocation in current_allocations:

        key = (
            allocation.get("zone_id"),
            allocation.get("resource_type")
        )

        if key in seen:

            duplicate_efforts.append({
                "zone_id": allocation.get(
                    "zone_id"
                ),
                "resource_type": allocation.get(
                    "resource_type"
                ),
                "description": (
                    "Multiple allocation entries detected "
                    "for the same zone and resource type."
                ),
                "recommended_action": (
                    "Review and consolidate overlapping "
                    "resource allocations."
                )
            })

        else:

            seen.add(key)

    # ==================================================
    # 5. REALLOCATION ALERT
    # ==================================================

    if reallocations:

        target_zone = reallocations[0][
            "to_zone_id"
        ]

        alerts.append({
            "alert_id": f"A{len(alerts) + 1:03d}",
            "type": "REALLOCATION_REQUIRED",
            "severity": "HIGH",
            "zone_id": target_zone,
            "message": (
                f"Resources should be dynamically "
                f"redirected to {target_zone} because "
                "of the new emergency."
            )
        })

    # ==================================================
    # 6. EXPLANATION
    # ==================================================

    if reallocations:

        summary = (
            "A new emergency changed zone priorities. "
            "The system identified existing resources "
            "that can be partially redirected toward "
            "the newly urgent zone."
        )

    elif reallocation_needed:

        summary = (
            "A new emergency changed zone priority, "
            "but no suitable existing resource "
            "allocation was available for safe "
            "reallocation."
        )

    else:

        summary = (
            "New reports were processed, but no "
            "priority change requiring reallocation "
            "was detected."
        )

    key_factors = []

    for change in priority_changes:

        key_factors.append(
            f"{change['zone_id']} changed from "
            f"{change['old_priority']} to "
            f"{change['new_priority']}"
        )

    if reallocations:

        key_factors.append(
            f"{len(reallocations)} resource "
            "reallocation recommendation generated"
        )

    if duplicate_efforts:

        key_factors.append(
            f"{len(duplicate_efforts)} duplicate "
            "effort(s) detected"
        )

    # ==================================================
    # FINAL RESULT
    # ==================================================

    return {
        "disaster_id": disaster_id,
        "reallocation_needed": reallocation_needed,
        "priority_changes": priority_changes,
        "reallocations": reallocations,
        "duplicate_efforts": duplicate_efforts,
        "alerts": alerts,
        "explanation": {
            "summary": summary,
            "key_factors": key_factors
        }
    }


# ======================================================
# LOCAL TEST
# ======================================================

if __name__ == "__main__":

    sample_disaster = {

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

    sample_allocations = [

        {
            "resource_id": "R001",
            "zone_id": "Z001",
            "resource_type": "Food",
            "quantity": 4000,
            "unit": "packets"
        },

        {
            "resource_id": "R002",
            "zone_id": "Z001",
            "resource_type": "Medical",
            "quantity": 800,
            "unit": "kits"
        },

        {
            "resource_id": "R003",
            "zone_id": "Z001",
            "resource_type": "Shelter",
            "quantity": 2000,
            "unit": "kits"
        }
    ]

    sample_reports = [

        {
            "report_id": "REP001",
            "zone_id": "Z002",
            "type": "NEW_EMERGENCY",
            "description": (
                "A bridge has collapsed in Zone B. "
                "150 people are trapped and emergency "
                "medical assistance is required."
            ),
            "severity_change": 3,
            "people_trapped": 150,
            "additional_medical_needed": 300,
            "timestamp": "2026-09-11T11:15:00Z"
        }
    ]

    result = reassess_situation(
        sample_disaster,
        sample_allocations,
        sample_reports
    )

    print("\n======================================")
    print("       REALLOCATION ASSESSMENT")
    print("======================================")

    print(
        json.dumps(
            result,
            indent=2
        )
    )