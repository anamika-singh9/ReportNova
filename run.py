from app.utils.config import show_config
from app.llms.model_factory import get_model
from app.agents.researcher import research
from app.tools.tavily_search import search_web

from app.agents.report_writer import WriterAgent

def main():
    # print("\nStarting Project...\n")
    # show_config()
    # print("Initializing LLM...\n")

    # try:
    #     model =get_model()
    #     response= model.invoke("Learing jobs realeated to AI is realy worthit in next 10 to 15 years? insipite of i have less interest...")
    #     print("LLM Response:\n")
    #     if isinstance(response.content, list):
    #         print(response.content[0]["text"])
    #     else:
    #         print(response.content)

    # except Exception as e:
    #     print(f"Error: {e}")
#==============================================================
    # print("\n===== AI Research Report Generator =====\n")
    # topic = input("Enter a research topic: ")
    # print("\nResearching...\n")
    # result= research(topic)

    # print("=" * 60)
    # print("Research Result:\n")
    # print(result)
    # print("=" * 60)
#====================================================================
    # result = search_web("Artificial Intelligence")
    # print(result)
#====================================================================

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