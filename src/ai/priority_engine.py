def calculate_priority_score(zone, emergency_boost=0):
    """
    Shared priority scoring engine.

    Maximum normal score = 100.

    Components:
    - Severity           = 50 points
    - Population        = 15 points
    - Trapped people    = 20 points
    - Medical need      = 10 points
    - Blocked access    = 5 points

    emergency_boost is used only when a NEW_EMERGENCY
    report is received.
    """

    severity = zone.get("severity", 0)
    population = zone.get("population_affected", 0)
    trapped = zone.get("people_trapped", 0)
    medical = zone.get("people_needing_medical", 0)
    accessibility = zone.get("accessibility", "")

    # ---------------------------------------------
    # Individual scoring components
    # ---------------------------------------------

    severity_score = severity * 5

    population_score = min(
        population / 5000,
        1
    ) * 15

    trapped_score = min(
        trapped / 200,
        1
    ) * 20

    medical_score = min(
        medical / 800,
        1
    ) * 10

    access_score = (
        5
        if accessibility.lower() == "blocked"
        else 0
    )

    # ---------------------------------------------
    # Final score
    # ---------------------------------------------

    score = (
        severity_score
        + population_score
        + trapped_score
        + medical_score
        + access_score
        + emergency_boost
    )

    return min(round(score), 100)


def get_priority_level(score):
    """
    Convert numerical score into priority level.
    """

    if score >= 80:
        return "CRITICAL"

    elif score >= 60:
        return "HIGH"

    elif score >= 40:
        return "MEDIUM"

    else:
        return "LOW"