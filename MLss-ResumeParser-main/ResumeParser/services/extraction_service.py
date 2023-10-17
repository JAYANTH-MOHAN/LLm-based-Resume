
import json
from typing import Sequence
from langchain.prompts import (
    PromptTemplate
)
from langchain.llms import OpenAI
from pydantic import BaseModel
from langchain.output_parsers import PydanticOutputParser
from ResumeParser.models import ParserOutput
from ResumeParser.config import settings


class Information(BaseModel):
    """Identifying information about all people in a text."""
    field: Sequence[ParserOutput]


class ExtractionService:
    """Extraction Service for resume files."""

    def __init__(self) -> None:
        """Initialize the PostProcessingService."""
        self.llm_model = OpenAI(
            model="text-davinci-003",
            temperature=0,
            openai_api_key=settings.openai_key,
            max_tokens=-1)

    def __call__(self, text) -> dict:
        # template = """
        #         Your task is to act as a information extractor. Given a resume as a multiline text \n{query} your task is to extact the following information [Name, Communication, Number, Education, Eperience, Skills] as given in {format_instructions}. Description about each field to be extracted are given below.
        #         "Name" (usually in the beginning; if not present, leave the field as ["None"])
        #         "PointOfCommunication" (could contain an email id or other social media links like LinkedIn; if not, leave the field as ["None"])
        #         "PhoneNumber" (if not present, leave the field as ["None"])
        #         "EducationQualification" (if schools and colleges are present, output as a list with year and degree; otherwise, leave this field as ["None"])
        #         "WorkExperience" (if present, provide it as a list with years, including job titles and descriptions; if not, leave this field as ["None"])
        #         "Skills" (include technical skills, programming skills, data management skills, and operating system skills; if not, leave this field as ["None"])
        #         If any of the field is empty use ["None"] as placeholder. """

        template = """
        Your task is to act as a information extractor for extracting information from resume or curriculum vitae (cv) 
        in text format. Given a resume as a multiline text \n{query} your task is to extract the following information 
        [Name, Communication, Number, Education, Experience, Skills] as given in {format_instructions}.If some fileds are "null" return it as "None" dont give null name it as None always"""

        # Set up a parser + inject instructions into the prompt template.
        parser = PydanticOutputParser(pydantic_object=Information)

        # Prompt
        prompt = PromptTemplate(
            template=template,
            input_variables=["query"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        # Run
        number=2500
        _input = prompt.format_prompt(query=text[:number])
        #print(_input.to_string())
        output = self.llm_model(_input.to_string())
        print(output)
        result = parser.parse(output)
        response = result.dict()["field"][0]
        if type(response) == str:
            response = json.loads(result.dict()["field"][0])
        return response

