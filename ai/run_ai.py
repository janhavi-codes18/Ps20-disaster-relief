import sys
import json

from agents.needs_agent import assess_needs
from agents.priority_agent import calculate_priorities
from agents.allocation_agent import allocate_resources
from agents.reallocation_agent import reassess_situation
from agents.duplicate_effort_agent import detect_duplicate_efforts


def run_ai(disaster_data):
    """
    Main entry point for the Node.js backend.

    Input:
        Complete disaster data as a Python dictionary.

    Output:
        Complete PS20 AI decision as a Python dictionary.
    """

    # --------------------------------------------------
    # 1. NEEDS ASSESSMENT
    # --------------------------------------------------

    needs_data = assess_needs(disaster_data)

    # --------------------------------------------------
    # 2. PRIORITY ASSESSMENT
    # --------------------------------------------------

    priority_data = calculate_priorities(
        disaster_data,
        needs_data
    )

    # --------------------------------------------------
    # 3. RESOURCE ALLOCATION
    # --------------------------------------------------

    allocation_data = allocate_resources(
        disaster_data,
        needs_data,
        priority_data
    )

    # --------------------------------------------------
    # 4. DUPLICATE EFFORT DETECTION
    # --------------------------------------------------

    current_allocations = disaster_data.get(
        "previous_allocations",
        []
    )

    duplicate_data = detect_duplicate_efforts(
        current_allocations
    )

    # --------------------------------------------------
    # 5. REALLOCATION
    # --------------------------------------------------

    new_reports = disaster_data.get(
        "new_reports",
        []
    )

    if new_reports:

        reallocation_data = reassess_situation(
            disaster_data,
            current_allocations,
            new_reports
        )

    else:

        reallocation_data = {
            "disaster_id": disaster_data.get(
                "disaster", {}
            ).get(
                "disaster_id",
                "UNKNOWN"
            ),
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
    # 6. COMBINE DUPLICATE-EFFORT ALERTS
    # --------------------------------------------------

    duplicate_efforts = duplicate_data.get(
        "duplicate_efforts",
        []
    )

    # Add duplicate-effort alerts to the reallocation alerts
    # so the final result contains all important alerts.
    if duplicate_efforts:

        for duplicate in duplicate_efforts:

            reallocation_data["alerts"].append({
                "alert_id": f"A_DUP_{len(reallocation_data['alerts']) + 1}",
                "type": "DUPLICATE_EFFORT",
                "severity": "HIGH",
                "zone_id": duplicate.get("zone_id"),
                "message": duplicate.get(
                    "reason",
                    "Duplicate resource allocation detected."
                )
            })

    # --------------------------------------------------
    # FINAL RESULT
    # --------------------------------------------------

    return {
        "disaster_id": disaster_data.get(
            "disaster", {}
        ).get(
            "disaster_id",
            "UNKNOWN"
        ),

        "needs_assessment": needs_data,

        "priority_assessment": priority_data,

        "allocation": allocation_data,

        "reallocation": {
            **reallocation_data,
            "duplicate_efforts": duplicate_efforts
        }
    }


# ======================================================
# COMMAND LINE INTERFACE
# ======================================================

if __name__ == "__main__":

    try:

        # Read JSON sent by Node.js
        input_data = sys.stdin.read()

        if not input_data.strip():
            raise ValueError("No JSON input received.")

        disaster_data = json.loads(input_data)

        # Run AI pipeline
        result = run_ai(disaster_data)

        # Return ONLY JSON
        print(json.dumps(result))

    except Exception as error:

        error_response = {
            "success": False,
            "error": str(error)
        }

        print(json.dumps(error_response))