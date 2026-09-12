import json


def detect_duplicate_efforts(current_allocations):
    """
    Detects when the same type of resource is allocated
    multiple times to the same zone.
    """

    seen = {}
    duplicates = []

    for allocation in current_allocations:
        zone_id = allocation.get("zone_id")
        resource_type = allocation.get("resource_type")

        if not zone_id or not resource_type:
            continue

        key = (zone_id, resource_type)

        if key in seen:
            duplicates.append({
                "zone_id": zone_id,
                "resource_type": resource_type,
                "first_allocation": seen[key],
                "duplicate_allocation": allocation,
                "reason": (
                    f"Multiple allocations of {resource_type} "
                    f"were detected for {zone_id}."
                )
            })
        else:
            seen[key] = allocation

    return {
        "duplicate_efforts": duplicates
    }


if __name__ == "__main__":

    test_allocations = [
        {
            "resource_id": "R001",
            "zone_id": "Z002",
            "resource_type": "Food",
            "quantity": 1000,
            "unit": "packets"
        },
        {
            "resource_id": "R004",
            "zone_id": "Z002",
            "resource_type": "Food",
            "quantity": 800,
            "unit": "packets"
        },
        {
            "resource_id": "R002",
            "zone_id": "Z002",
            "resource_type": "Medical",
            "quantity": 200,
            "unit": "kits"
        }
    ]

    result = detect_duplicate_efforts(test_allocations)

    print("=" * 50)
    print("       DUPLICATE EFFORT DETECTION")
    print("=" * 50)
    print(json.dumps(result, indent=2))