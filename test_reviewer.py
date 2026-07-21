from app.agents.reviewer import ReviewerAgent

reviewer = ReviewerAgent()

report = """

# Artificial Intelligence 

AI is very useful technology.
AI helps many fields.

AI is used in healthcare.
AI is used in healthcare.
It can do many things.

"""

improved_report = reviewer.review(report)

print("\n============REVIEWED REPORT==========\n")
print(improved_report)