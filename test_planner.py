from app.agents.planner import PlannerAgent 

planner = PlannerAgent()

topic = "Artificial Intelligence in Healthcare"

plan = planner.plan(topic)

print("\n====RESEARCH PLAN=====\n")

print(plan)