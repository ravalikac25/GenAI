from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain.output_parsers import OutputFixingParser
from prompts import make_explainer_prompt, make_structured_parser

llm = OllamaLLM(model="llama3")

def run_explainer():
    prompt = make_explainer_prompt()
    query = prompt.format(topic="quantum computing")
    print("User:", query)
    print("LLM:", llm.invoke(query))

def run_structured():
    parser = make_structured_parser()
    fixing_parser = OutputFixingParser.from_llm(parser=parser, llm=llm)
    format_instructions = fixing_parser.get_format_instructions()

    prompt = PromptTemplate(
        template="Summarize the following text.\n{text}\n{format_instructions}",
        input_variables=["text"],
        partial_variables={"format_instructions": format_instructions},
    )

    query = prompt.format(text="LangChain makes it easy to work with LLMs.")
    print("User:", query)
    response = llm.invoke(query)
    print("LLM [raw]:", response)
    print("LLM [parsed]:", fixing_parser.parse(response))

if __name__ == "__main__":
    # run_explainer()
    run_structured()