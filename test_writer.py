from app.agents.report_writer import WriterAgent

writer = WriterAgent()

verified_notes = """

Artificial Intelligence is the simulation of human intelligence.

AI is used in healthcare for diagnosis.

Artificial Intelligence is the simulation of human intelligence.

AI helps detect diseases earlier.

Some websites claim AI can completely replace doctors.


"""

report = writer.writer(verified_notes)

print("\n===========FINAL REPORT========\n")
print(report)