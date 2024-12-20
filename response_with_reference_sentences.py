from prompts import PROMPT_TO_GENERATE_RESPONSE_FROM_CONTEXT, PROMPT_TO_GENERATE_FACTS, PROMPT_TO_GENERATE_REFERENCES_FROM_FACTS
import re
import json
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
import re
import json
from groq import Groq
import os
import ast
import traceback
from typing import List, Tuple, Union

class response_with_references:
    def __init__(self):
        """
        Initialize the response_with_references class with the LLM client.
        """
        # emumba locally deployed LLM
        # self.client = OpenAI( 
        #     base_url="http://genie.emumba.com/v1/", 
        #     default_headers={
        #         "Authorization": "Bearer genie-vllm-secure-key"
        #         }
        # )

        # OpenAI llm
        # self.client = OpenAI(api_key="your-openai-api-key")


        # Groq llm
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))


        self.llm_model_name = "llama-3.3-70b-versatile"
        self.openai_api_key = "only-needed-for-validation"


    def generate_response_and_references(self, question:str, context:str) -> Union[Tuple[str, List[str]], Tuple[str, List]]:
        
        """
        Generate a response and references from the LLM based on the given question and context.

        Args:
            question (str): The question to ask the LLM.
            context (str): The context from which the question is to be answered.

        Returns:
            Union[Tuple[str, List[str]], Tuple[str, List]]: A tuple containing the generated answer and a list of references.
        """

        try:
            # add the user question and context in the prompt template
            prompt_template = PROMPT_TO_GENERATE_RESPONSE_FROM_CONTEXT.format(query=question, context=context)

            messages = [{"role": "user", "content": prompt_template}]
            
            # generate answer from llm
            print("Generating response and references from the LLM ...")
            chat_completions = self.client.chat.completions.create(
                model=self.llm_model_name,
                temperature=0.1,
                top_p=0.1,
                messages=messages
            )
            
            # parse response and references from the generated response
            response = chat_completions.choices[0].message.content.strip() 
            match = re.search(r'\{(?:[^{}]*|\{(?:[^{}]*|\{[^{}]*\})*\})*\}', response)

            if match:
                
                json_str = match.group() 
                
                json_obj = json.loads(json_str)

                answer = json_obj.get("answer")
                references = json_obj.get("reference")

                return answer,references

            return "Either the LLM failed to generate the response or the response,references could no be extracted from the LLM response through regex", []
        
        except Exception as error:
            print("Error in function generate_response_and_references")
            error_trace = traceback.format_exc()
            print(error_trace)
            print(f"Type: {type(error).__name__}")
            print(f"Message: {str(error)}")

            return f"An error occured: {error}", []


    def generate_facts(self, llm_response:str, context:str) -> Union[str, None]:
        
        """
        Generate facts from the LLM based on the given response and context.

        Args:
            llm_response (str): The response from the LLM.
            context (str): The context from which the response is generated.

        Returns:
            Union[str, None]: The generated facts as a string, or None if an error occurs.
        """

        try:
            # add the user question and context in the prompt template
            prompt_template = PROMPT_TO_GENERATE_FACTS.format(question=llm_response, response=context)

            messages = [{"role": "user", "content": prompt_template}]

            # generate answer from llm
            print("Generating facts from the LLM ...")
            chat_completions = self.client.chat.completions.create(
                model=self.llm_model_name,
                temperature=0.1,
                top_p=0.1,
                messages=messages
            )
            
            # parse response and references from the generated response
            response_str = chat_completions.choices[0].message.content.strip() 
               
            return response_str

        except Exception as error:
            print("Error in function generate_facts")
            error_trace = traceback.format_exc()
            print(error_trace)
            print(f"Type: {type(error).__name__}")
            print(f"Message: {str(error)}")

            return None
    
    
    def generate_references_from_facts(self, facts, context:str) -> Union[List[dict], str]:
        
        """
        Generate references from facts using the LLM based on the given facts and context.

        Args:
            facts (List[str]): The list of facts.
            context (str): The context from which the response is generated.

        Returns:
            Union[List[dict], str]: A list of dictionaries containing facts and their references, or an error message if an error occurs.
        """

        try:
            
            # create a list of strings 
            facts_str = ""
            for fact in facts:
                facts_str += fact + "\n"
                
            # add the user question and context in the prompt template
            prompt_template = PROMPT_TO_GENERATE_REFERENCES_FROM_FACTS.format(facts=facts, context=context)

            messages = [{"role": "user", "content": prompt_template}]
            
            # generate answer from llm
            print("Generating references from facts using the LLM ...")
            chat_completions = self.client.chat.completions.create(
                model=self.llm_model_name,
                temperature=0.1,
                top_p=0.1,
                messages=messages
            )
            
            # parse response and references from the generated response
            response_str = chat_completions.choices[0].message.content.strip() 
            response_json = json.loads(response_str)
            required_response = response_json.get("response")

            # extract facts and references only
            extracted_facts_and_references = []

            for dictionary in required_response:
                extracted_facts_and_references.append({ dictionary.get("Fact") : dictionary.get("Reference") })

            return extracted_facts_and_references

        except Exception as error:
            print("Error in function generate_references_from_facts")
            error_trace = traceback.format_exc()
            print(error_trace)
            print(f"Type: {type(error).__name__}")
            print(f"Message: {str(error)}")

            return f"An error occured: {error}"


    def generate_facts_and_references(self, llm_response:str, context:str) -> Union[List[dict], Tuple[str, List]]:

        """
        Generate facts and references from the LLM based on the given response and context.

        Args:
            llm_response (str): The response from the LLM.
            context (str): The context from which the response is generated.

        Returns:
            Union[List[dict], Tuple[str, List]]: A list of dictionaries containing facts and their references, or a tuple with an error message and an empty list if no facts could be generated.
        """

        facts = self.generate_facts(llm_response=llm_response, context=context)

        if facts:

            facts_and_references = self.generate_references_from_facts(facts=facts, context=context)    

            return facts_and_references
        
        else:
            return "No facts could be generated from the LLM", []
       