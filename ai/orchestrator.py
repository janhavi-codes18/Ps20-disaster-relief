import json

from agents.needs_agent import assess_needs
from agents.priority_agent import calculate_priorities
from agents.allocation_agent import allocate_resources
from agents.reallocation_agent import reassess_situation


# ============================================
# AI ORCHESTRATOR
# ============================================

def run_disaster_analysis(disaster_data):
    """
    Run the complete AI disaster-response pipeline.

    Flow:
    Disaster Data
        ↓
    Needs Assessment
        ↓
    Priority Assessment
        ↓
    Resource Allocation
        ↓
    Reallocation if new emergency reports exist
    """

    print("\n========================================")
    print("        PS20 AI ORCHESTRATOR")
    print("========================================")


    # ========================================
    # STEP 1: NEEDS ASSESSMENT
    # ========================================

    print("\n[1/4] Running Needs Assessment Agent...")

    needs_result = assess_needs(disaster_data)

    print("✓ Needs assessment completed.")


    # ========================================
    # STEP 2: PRIORITY ASSESSMENT
    # ========================================

    print("\n[2/4] Running Priority Agent...")

    priority_result = calculate_priorities(
        disaster_data,
        needs_result
    )

    print("✓ Priority assessment completed.")


    # ========================================
    # STEP 3: RESOURCE ALLOCATION
    # ========================================

    print("\n[3/4] Running Resource Allocation Agent...")

    allocation_result = allocate_resources(
        disaster_data,
        needs_result,
        priority_result
    )

    print("✓ Resource allocation completed.")


    # ========================================
    # STEP 4: DYNAMIC REALLOCATION
    # ========================================

    new_reports = disaster_data.get(
        "new_reports",
        []
    )

    reallocation_result = None

    if new_reports:

        print(
            "\n[4/4] New emergency reports detected."
        )

        print(
            "Running Reallocation Agent..."
        )

        reallocation_result = reassess_situation(
            disaster_data,
            allocation_result["allocations"],
            new_reports
        )

        print(
            "✓ Reallocation analysis completed."
        )

    else:

        print(
            "\n[4/4] No new emergency reports."
        )

        print(
            "Reallocation Agent skipped."
        )


    # ========================================
    # FINAL RESULT
    # ========================================

    final_result = {

        "disaster_id":
            disaster_data["disaster"]["disaster_id"],

        "needs_assessment":
            needs_result,

        "priority_assessment":
            priority_result,

        "allocation":
            allocation_result,

        "reallocation":
            reallocation_result
    }


    return final_result


# ============================================
# TEST DATA
# ============================================

if __name__ == "__main__":

    disaster_data = {

        # ------------------------------------
        # DISASTER
        # ------------------------------------

        "disaster": {

            "disaster_id": "D001",

            "type": "Flood",

            "location": "Pune",

            "severity": 8,

            "description":
                "Heavy flooding has affected multiple areas",

            "timestamp":
                "2026-09-11T10:30:00Z"
        },


        # ------------------------------------
        # AFFECTED ZONES
        # ------------------------------------

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

                "population_affected": 2500,

                "severity": 6,

                "people_needing_medical": 200,

                "people_needing_food": 1800,

                "people_needing_shelter": 1000,

                "people_trapped": 20,

                "accessibility": "Accessible"
            }
        ],


        # ------------------------------------
        # AVAILABLE RESOURCES
        # ------------------------------------

        "resources": [

            {
                "resource_id": "R001",

                "type": "Food",

                "quantity": 5000,

                "unit": "packets",

                "location": "Warehouse A",

                "available": True
            },


            {
                "resource_id": "R002",

                "type": "Medical",

                "quantity": 1000,

                "unit": "kits",

                "location": "Hospital A",

                "available": True
            },


            {
                "resource_id": "R003",

                "type": "Shelter",

                "quantity": 2000,

                "unit": "spaces",

                "location": "Shelter Center",

                "available": True
            }
        ],


        # ====================================
        # CURRENT ALLOCATIONS
        # ====================================

        "previous_allocations": [

            {
                "resource_id": "R001",
                "zone_id": "Z001",
                "resource_type": "Food",
                "quantity": 4000,
                "unit": "packets",
                "urgency": "CRITICAL"
            },

            {
                "resource_id": "R001",
                "zone_id": "Z002",
                "resource_type": "Food",
                "quantity": 1000,
                "unit": "packets",
                "urgency": "HIGH"
            },

            {
                "resource_id": "R002",
                "zone_id": "Z001",
                "resource_type": "Medical",
                "quantity": 800,
                "unit": "kits",
                "urgency": "CRITICAL"
            },

            {
                "resource_id": "R002",
                "zone_id": "Z002",
                "resource_type": "Medical",
                "quantity": 200,
                "unit": "kits",
                "urgency": "HIGH"
            },

            {
                "resource_id": "R003",
                "zone_id": "Z001",
                "resource_type": "Shelter",
                "quantity": 2000,
                "unit": "spaces",
                "urgency": "CRITICAL"
            }
        ],


        # ====================================
        # 🚨 NEW EMERGENCY REPORT
        # ====================================

        "new_reports": [

            {
                "report_id": "REP001",

                "zone_id": "Z002",

                "type": "NEW_EMERGENCY",

                "description":
                    "A bridge has collapsed in Zone B. "
                    "150 people are trapped and emergency "
                    "medical assistance is required.",

                "severity_change": 3,

                "timestamp":
                    "2026-09-11T11:15:00Z"
            }
        ]
    }


    # ========================================
    # RUN COMPLETE AI SYSTEM
    # ========================================

    result = run_disaster_analysis(
        disaster_data
    )


    # ========================================
    # DISPLAY FINAL RESULT
    # ========================================

    print("\n\n========================================")
    print("          FINAL AI RESULT")
    print("========================================\n")

    print(
        json.dumps(
            result,
            indent=2
        )
    )


    print("\n========================================")
    print("   SUCCESS: AI ORCHESTRATOR WORKED.")
    print("========================================")