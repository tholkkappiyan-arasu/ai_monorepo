from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts.prompt import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent

def ice_break_with(name: str) -> str:
    linkedin_url = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_url)

    summary_template = """
        given the linkedin information {information} about a person I want you to create:
        1. A short summary
        2. two interesting facts about them
    """

    summary_prompt_template = PromptTemplate(
        input_variable=["information"], template=summary_template
    )

    llm = ChatOpenAI(temperature=1, model_name="gpt-4o-2024-08-06")
    # llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=1, top_p=0.85)

    chain = summary_prompt_template | llm

    response = chain.invoke(input={"information": linkedin_data})

    print(response)

if __name__ == "__main__":
    load_dotenv()
    ice_break_with(name="Tholkkappiyan linkedin")


