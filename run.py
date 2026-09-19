from app.utils.config import show_config
from app.llms.model_factory import get_model
from app.agents.researcher import research
from app.tools.tavily_search import search_web

from app.agents.report_writer import WriterAgent

def main():
   
    topic = "Artificial Intelligence"

    print("Researching topic...\n")\
    
    research_result = research(topic)

    print("Generating report...\n")

    writer_agent = WriterAgent()

    report = writer_agent.writer(research_result)

    print("\nFINAL REPORT\n")
    print(report)


if __name__ == "__main__":
    main()