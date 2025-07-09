from crewai import Crew, Process
from scripts.agents import doctor
from scripts.task import help_patients

async def run_crew(query: str, fileContent: str="Some content"):
    """To run the whole crew"""
    medical_crew = Crew(
        agents=[doctor],
        tasks=[help_patients],
        process=Process.sequential,
    )
    result = medical_crew.kickoff({'query': query, 'fileData': fileContent })
    return result