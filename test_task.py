from models import Session, Policy
from run_worker import process_ai
from time import sleep

session = Session()
policy = Policy(name="Test Policy 2", ai_result=None)
session.add(policy)
session.commit()
policy_id = policy.id
session.close()

process_ai.delay(policy_id, "Generate a summary for a fire insurance policy")
print("Task queued!")

sleep(8)

session = Session()
p = session.get(Policy, policy_id)
print("AI Result:", p.ai_result)
session.close()
