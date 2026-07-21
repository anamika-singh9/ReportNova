from app.agents.fact_checker import FactCheckerAgent

fact_checker = FactCheckerAgent()

sample_notes = """

Artificial Intelligence is the simulation of human intelligence.

AI is used in healthcare for diagnosis.

Artificial Intelligence is the simulation of human intelligence.

AI helps detect diseases earlier.

Some websites claim AI can completely replace doctors.

"""

verified_notes = fact_checker.verify(sample_notes)

print("\n==========VERIFIED RESEARCH NOTES ================\n")
print(verified_notes)