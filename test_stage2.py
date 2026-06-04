from stages.stage1_intent import extract_intent
from stages.stage2_system_design import generate_system_design

prompt = """
Build a CRM application.

Features:
- Authentication
- Contact management
- Dashboard
- Premium subscription
- Analytics
"""

intent, _ = extract_intent(prompt)

design = generate_system_design(intent)

print(design.model_dump_json(indent=2))