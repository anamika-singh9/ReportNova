import os
from app.agents.pdf_generator import PDFGeneratorAgent


generator = PDFGeneratorAgent()

report = """
# Artificial Intelligence

## Introduction

Artificial Intelligence enables machines to perform intelligent tasks.

## Applications

AI is used in healthcare, education and automation.

## Conclusion

AI continues to transform industries.
"""


file_path = generator.generate(
    report,
    "AI_Report.pdf"
)


print("PDF Created:", file_path)

print("Current Location:")
print(os.getcwd())

print("Files in folder:")
print(os.listdir())