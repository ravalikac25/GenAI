from langchain.prompts import PromptTemplate
from langchain.output_parsers import StructuredOutputParser, ResponseSchema

def make_explainer_prompt():
    return PromptTemplate(
        input_variables=["topic"],
        template="Explain {topic} in simple terms, in 3 sentences."
    )

def make_structured_parser():
    schemas = [
        ResponseSchema(name="summary", description="One-sentence summary"),
        ResponseSchema(name="keywords", description="Important keywords as a list")
    ]
    return StructuredOutputParser.from_response_schemas(schemas)
