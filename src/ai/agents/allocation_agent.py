import json


def allocate_resources(disaster_data, needs_data, priority_data):
    """
    Deterministic Resource Allocation Agent.

    Allocates available resources to zones according to:
    1. Zone priority
    2. Resource requirement
    3. Available quantity

    Never allocates more than the available resource quantity.
    No external AI/API call is required.
    """

    disaster_id = disaster_data.get("disaster", {}).get(
        "disaster_id", "UNKNOWN"
    )

    resources = disaster_data.get("resources", [])
    zones = disaster_data.get("zones", [])

    zone_needs = needs_data.get("zone_needs", [])
    prioritized_zones = priority_data.get("prioritized_zones", [])

    # --------------------------------------------------
    # Create lookup tables
    # --------------------------------------------------

    needs_by_zone = {
        item["zone_id"]: item
        for item in zone_needs
    }

    zone_info = {
        zone["zone_id"]: zone
        for zone in zones
    }

    # Highest priority first
    sorted_zones = sorted(
        prioritized_zones,
        key=lambda x: x.get("priority_score", 0),
        reverse=True
    )

    allocations = []
    alerts = []

    # Track how much of each resource has already been allocated
    remaining_resources = {}

    for resource in resources:

        resource_id = resource.get("resource_id")
        resource_type = resource.get("type", "")
        quantity = resource.get("quantity", 0)
        available = resource.get("available", False)

        if available:
            remaining_resources[resource_id] = quantity
        else:
            remaining_resources[resource_id] = 0

    # Track allocated quantity by zone and resource type
    allocated = {}

    # --------------------------------------------------
    # Resource → Need mapping
    # --------------------------------------------------

    need_mapping = {
        "Food": "food_required",
        "Medical": "medical_required",
        "Shelter": "shelter_required",
        "Rescue": "rescue_required"
    }

    # --------------------------------------------------
    # ALLOCATION PROCESS
    # --------------------------------------------------

    for priority_zone in sorted_zones:

        zone_id = priority_zone.get("zone_id")
        priority = priority_zone.get("priority", "LOW")
        priority_score = priority_zone.get("priority_score", 0)

        zone_need = needs_by_zone.get(zone_id, {})

        for resource in resources:

            resource_id = resource.get("resource_id")
            resource_type = resource.get("type", "")
            unit = resource.get("unit", "")

            if not resource.get("available", False):
                continue

            # Find corresponding requirement
            need_field = need_mapping.get(resource_type)

            if not need_field:
                continue

            required_quantity = zone_need.get(need_field, 0)

            # Already allocated for this zone/resource type
            already_allocated = allocated.get(
                (zone_id, resource_type), 0
            )

            remaining_need = max(
                required_quantity - already_allocated,
                0
            )

            available_quantity = remaining_resources.get(
                resource_id,
                0
            )

            if remaining_need <= 0 or available_quantity <= 0:
                continue

            # Allocate only what is needed and available
            allocation_quantity = min(
                remaining_need,
                available_quantity
            )

            allocations.append({
                "resource_id": resource_id,
                "zone_id": zone_id,
                "resource_type": resource_type,
                "quantity": allocation_quantity,
                "unit": unit,
                "reason": (
                    f"Allocated to {zone_id} because it has "
                    f"{priority} priority "
                    f"(score {priority_score}/100)."
                ),
                "urgency": priority
            })

            # Update remaining stock
            remaining_resources[resource_id] -= allocation_quantity

            # Update zone allocation
            allocated[(zone_id, resource_type)] = (
                already_allocated + allocation_quantity
            )

    # --------------------------------------------------
    # SHORTAGE DETECTION
    # --------------------------------------------------

    alert_number = 1

    for priority_zone in sorted_zones:

        zone_id = priority_zone.get("zone_id")
        priority = priority_zone.get("priority", "LOW")

        zone_need = needs_by_zone.get(zone_id, {})

        for resource_type, need_field in need_mapping.items():

            required = zone_need.get(need_field, 0)

            allocated_quantity = allocated.get(
                (zone_id, resource_type),
                0
            )

            shortage = required - allocated_quantity

            if shortage > 0:

                alerts.append({
                    "alert_id": f"A{alert_number:03d}",
                    "type": "RESOURCE_SHORTAGE",
                    "severity": priority,
                    "zone_id": zone_id,
                    "message": (
                        f"{resource_type} shortage in {zone_id}: "
                        f"{shortage} units still required."
                    )
                })

                alert_number += 1

    # --------------------------------------------------
    # ACCESSIBILITY ALERTS
    # --------------------------------------------------

    for zone in zones:

        if zone.get("accessibility", "").lower() == "blocked":

            zone_id = zone.get("zone_id")

            alerts.append({
                "alert_id": f"A{alert_number:03d}",
                "type": "ACCESS_BLOCKED",
                "severity": "CRITICAL",
                "zone_id": zone_id,
                "message": (
                    f"Access to {zone_id} is blocked. "
                    "Resource delivery or rescue operations "
                    "may require access clearance."
                )
            })

            alert_number += 1

    return {
        "disaster_id": disaster_id,
        "allocations": allocations,
        "alerts": alerts
    }


# --------------------------------------------------
# LOCAL TEST
# --------------------------------------------------

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
        ],

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
                "location": "Warehouse B",
                "available": True
            },
            {
                "resource_id": "R003",
                "type": "Shelter",
                "quantity": 2000,
                "unit": "kits",
                "location": "Warehouse C",
                "available": True
            }
        ]
    }

    sample_needs = {
        "disaster_id": "D001",
        "zone_needs": [
            {
                "zone_id": "Z001",
                "food_required": 4000,
                "medical_required": 800,
                "shelter_required": 3000,
                "rescue_required": 200
            },
            {
                "zone_id": "Z002",
                "food_required": 2500,
                "medical_required": 200,
                "shelter_required": 1500,
                "rescue_required": 20
            }
        ]
    }

    sample_priority = {
        "disaster_id": "D001",
        "prioritized_zones": [
            {
                "zone_id": "Z001",
                "priority": "CRITICAL",
                "priority_score": 95,
                "reason": "Critical emergency"
            },
            {
                "zone_id": "Z002",
                "priority": "MEDIUM",
                "priority_score": 42,
                "reason": "Moderate emergency"
            }
        ]
    }

    result = allocate_resources(
        sample_disaster,
        sample_needs,
        sample_priority
    )

    print("\n===== RESOURCE ALLOCATION =====")
    print(json.dumps(result, indent=2))