import os
import json
from dotenv import load_dotenv
from google import genai

# ============================================
# 1. LOAD GEMINI API KEY
# ============================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)


# ============================================
# 2. SAMPLE DISASTER DATA
# ============================================

disaster_data = {
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
            "population_affected": 2500,
            "severity": 6,
            "people_needing_medical": 200,
            "people_needing_food": 1800,
            "people_needing_shelter": 1000,
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

    "previous_allocations": [],
    "new_reports": []
}


# ============================================
# 3. AI INSTRUCTIONS
# ============================================

prompt = f"""
You are the AI decision engine for an Agentic Disaster Relief
and Emergency Resource Coordinator.

Analyze the disaster situation, affected zones, and available resources.

Perform these tasks:

1. Assess the needs of every affected zone.
2. Calculate a priority score from 0 to 100.
3. Assign one priority level:
   CRITICAL, HIGH, MEDIUM, or LOW.
4. Allocate available resources to the highest-priority zones.
5. Detect resource shortages.
6. Determine whether reallocation is required.
7. Detect possible duplicate relief efforts.
8. Explain the important factors behind your decisions.

IMPORTANT RULES:

- Return ONLY valid JSON.
- Do NOT use Markdown.
- Do NOT add ```json.
- Do NOT add explanations outside the JSON.
- Do not invent resources that are not provided.
- Do not allocate more resources than are available.
- Use the exact field names specified below.

REQUIRED OUTPUT STRUCTURE:

{{
  "disaster_id": "string",

  "prioritized_zones": [
    {{
      "zone_id": "string",
      "priority": "CRITICAL | HIGH | MEDIUM | LOW",
      "priority_score": 0,
      "reason": "string"
    }}
  ],

  "allocations": [
    {{
      "resource_id": "string",
      "zone_id": "string",
      "resource_type": "string",
      "quantity": 0,
      "unit": "string",
      "reason": "string",
      "urgency": "CRITICAL | HIGH | MEDIUM | LOW"
    }}
  ],

  "alerts": [
    {{
      "alert_id": "string",
      "type": "RESOURCE_SHORTAGE | CRITICAL_ZONE | ACCESS_BLOCKED | NEW_EMERGENCY | DUPLICATE_EFFORT | REALLOCATION_REQUIRED",
      "severity": "CRITICAL | HIGH | MEDIUM | LOW",
      "zone_id": "string",
      "message": "string"
    }}
  ],

  "reallocation_needed": false,

  "reallocations": [],

  "duplicate_efforts": [],

  "explanation": {{
    "summary": "string",
    "key_factors": [
      "string"
    ]
  }}
}}

Here is the disaster data:

{json.dumps(disaster_data, indent=2)}
"""


# ============================================
# 4. CALL GEMINI
# ============================================

response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=prompt,
    config={
        "response_mime_type": "application/json"
    }
)


# ============================================
# 5. VALIDATE JSON RESPONSE
# ============================================

print("\n========== AI RESPONSE ==========\n")

try:
    result = json.loads(response.text)

    print(json.dumps(result, indent=2))

    print("\n=================================")
    print("SUCCESS: AI returned valid JSON.")
    print("=================================")

except json.JSONDecodeError:
    print("ERROR: AI did not return valid JSON.")
    print("\nRaw response:")
    print(response.text)