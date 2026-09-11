import sys
import json

from agents.needs_agent import assess_needs
from agents.priority_agent import calculate_priorities
from agents.allocation_agent import allocate_resources
from agents.reallocation_agent import reassess_situation
from agents.duplicate_effort_agent import detect_duplicate_efforts


def run_ai(disaster_data):
    """
    Main AI entry point for the PS20 Disaster Relief System.

    Input:
        Complete disaster information as a Python dictionary.

    Output:
        Flat structured JSON compatible with Backend + Frontend.
    """

    # ---------------------------------------------------------
    # 1. NEEDS ASSESSMENT
    # ---------------------------------------------------------
    needs_data = assess_needs(disaster_data)

    # ---------------------------------------------------------
    # 2. PRIORITY ASSESSMENT
    # ---------------------------------------------------------
    priority_data = calculate_priorities(
        disaster_data,
        needs_data
    )

    # ---------------------------------------------------------
    # 3. RESOURCE ALLOCATION
    # ---------------------------------------------------------
    allocation_data = allocate_resources(
        disaster_data,
        needs_data,
        priority_data
    )

    # ---------------------------------------------------------
    # 4. DUPLICATE EFFORT DETECTION
    # ---------------------------------------------------------
    current_allocations = disaster_data.get(
        "previous_allocations",
        []
    )

    duplicate_data = detect_duplicate_efforts(
        current_allocations
    )

    duplicate_efforts = duplicate_data.get(
        "duplicate_efforts",
        []
    )

    # ---------------------------------------------------------
    # 5. DYNAMIC REALLOCATION
    # ---------------------------------------------------------
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

        disaster_id = disaster_data.get(
            "disaster",
            {}
        ).get(
            "disaster_id",
            "UNKNOWN"
        )

        reallocation_data = {
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

    # ---------------------------------------------------------
    # 6. COMBINE ALL ALERTS
    # ---------------------------------------------------------
    alerts = []

    # Allocation alerts
    allocation_alerts = allocation_data.get(
        "alerts",
        []
    )

    alerts.extend(allocation_alerts)

    # Reallocation alerts
    reallocation_alerts = reallocation_data.get(
        "alerts",
        []
    )

    alerts.extend(reallocation_alerts)

    # Duplicate effort alerts
    for duplicate in duplicate_efforts:

        alerts.append({
            "alert_id": "",
            "type": "DUPLICATE_EFFORT",
            "severity": "HIGH",
            "zone_id": duplicate.get(
                "zone_id"
            ),
            "message": duplicate.get(
                "reason",
                "Duplicate resource allocation detected."
            )
        })

    # ---------------------------------------------------------
    # 7. GENERATE UNIQUE ALERT IDs
    # ---------------------------------------------------------
    #
    # Important:
    # Every alert receives a new sequential ID.
    #
    # A001
    # A002
    # A003
    # ...
    #
    # This prevents duplicate alert IDs when alerts come
    # from both allocation and reallocation agents.
    # ---------------------------------------------------------

    for index, alert in enumerate(
        alerts,
        start=1
    ):

        alert["alert_id"] = f"A{index:03d}"

    # ---------------------------------------------------------
    # 8. GENERATE EXPLANATION
    # ---------------------------------------------------------
    explanation = reallocation_data.get(
        "explanation",
        {}
    )

    if not explanation:

        explanation = {
            "summary": (
                "AI analyzed disaster zones, "
                "resource requirements and "
                "available resources."
            ),
            "key_factors": []
        }

    # Make a copy so we don't accidentally modify
    # the original list from another agent.
    key_factors = list(
        explanation.get(
            "key_factors",
            []
        )
    )

    # Add duplicate-effort information
    if duplicate_efforts:

        key_factors.append(
            f"{len(duplicate_efforts)} "
            f"duplicate effort(s) detected"
        )

    # Add allocation-alert information
    if allocation_alerts:

        key_factors.append(
            f"{len(allocation_alerts)} "
            f"allocation alert(s) generated"
        )

    # Add reallocation information
    reallocations = reallocation_data.get(
        "reallocations",
        []
    )

    if reallocations:

        key_factors.append(
            f"{len(reallocations)} "
            f"resource reallocation recommendation(s) generated"
        )

    explanation["key_factors"] = key_factors

    # ---------------------------------------------------------
    # 9. FINAL FLAT OUTPUT
    # ---------------------------------------------------------
    #
    # This structure matches the AI output contract:
    #
    # prioritized_zones
    # allocations
    # alerts
    # reallocation_needed
    # reallocations
    # duplicate_efforts
    # explanation
    #
    # ---------------------------------------------------------

    result = {

        "disaster_id": disaster_data.get(
            "disaster",
            {}
        ).get(
            "disaster_id",
            "UNKNOWN"
        ),

        "prioritized_zones": priority_data.get(
            "prioritized_zones",
            []
        ),

        "allocations": allocation_data.get(
            "allocations",
            []
        ),

        "alerts": alerts,

        "reallocation_needed": reallocation_data.get(
            "reallocation_needed",
            False
        ),

        "reallocations": reallocations,

        "duplicate_efforts": duplicate_efforts,

        "explanation": explanation
    }

    return result


# =============================================================
# COMMAND-LINE ENTRY POINT
# =============================================================

if __name__ == "__main__":

    try:

        # Read JSON from stdin
        input_data = sys.stdin.read()

        # Make sure input was provided
        if not input_data.strip():

            raise ValueError(
                "No JSON input received."
            )

        # Convert JSON → Python dictionary
        disaster_data = json.loads(
            input_data
        )

        # Run complete AI pipeline
        result = run_ai(
            disaster_data
        )

        # Print ONLY JSON
        # Backend will read this output.
        print(
            json.dumps(
                result
            )
        )

    except Exception as error:

        # Always return valid JSON even when
        # something goes wrong.
        print(
            json.dumps({
                "success": False,
                "error": str(error)
            })
        )