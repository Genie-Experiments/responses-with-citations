PROMPT_TO_GENERATE_RESPONSE_FROM_CONTEXT = """ Your task is to answer the question from the given context. Answer in complete sentences rather than just giving one word answers. Along with the answer, you are required to return a list of reference sentences from the context that you used to answer the question. There can be more than one reference sentences. If the answer to the question is not present in the context then return an empty list in the references. Return nothing but the following:
        {{
            "answer": "Your answer here as a string",
            "reference": ["Reference sentence 1", "Reference sentence 2", ...]
        }}

        Question: {query}\nContext: {context}
"""

PROMPT_TO_GENERATE_FACTS = """
You are given a response along with its question. For the given task data, please breakdown the response into independent facts. A fact is a sentence that is true and can only be stated from the response. Facts should not depend on each another and must not convey the same information. 

Example Data.
[Question]: Which is the tallest monument in Paris?
[Response]: The Eiffel Tower, located in Paris, is one of the most visited monuments in the world. It was named after the engineer Gustave Eiffel, whose company designed and built the tower. Constructed from 1887 to 1889, it was initially criticized by some of France's leading artists and intellectuals.
[Output]: 
[
    "The Eiffel Tower is located in Paris.",
    "The Eiffel Tower is the tallest structure in Paris.",
    "The Eiffel Tower is very old.",
    "The Eiffel Tower is very old.",
]

[Question]: Is Leaning Tower of Pisa, which is located in Italy, the oldest monument in Europe?
[Response]: No
[Output]: 
{{
    "Fact": "1. The Leaning Tower of Pisa is not the oldest monument in Europe.",
}}

Return the output only in the corresponding List of strings format. Do not output anything other than this List of facts as strings:
    [ # List of all the facts
        "1st Fact",  # 1st fact being analysed,
        "2nd Fact",  # 2nd fact being analysed,
        ... # Do for all the facts
    ]
In case of no facts, return an empty list, i.e. [].

Task Data.
[Question]: {question}
[Response]: {response}
[Output]: 
"""


PROMPT_TO_GENERATE_REFERENCES_FROM_FACTS = """
You are a detail-oriented LLM whose task is to determine if the given facts are supported by the given context. Each fact is separated by the following symbol: ", ". 
For the given task data, go over each fact sentence one by one, and write down your judgement.

Example Data.
[Facts]: ["1. The Eiffel Tower is located in Paris.", "2. The Eiffel Tower is the tallest structure in Paris.", "3. The Eiffel Tower is very old."]
[Context]: The Eiffel Tower, located in Paris, is one of the most visited monuments in the world. It was named after the engineer Gustave Eiffel, whose company designed and built the tower. Constructed from 1887 to 1889, it was initially criticized by some of France's leading artists and intellectuals.
[Output]: 
{{ "response":[
        {{
            "Fact": "1. The Eiffel Tower is located in Paris.",
            "Reasoning": "The context explicity states that Paris, one of the most visited monuments in the world is located in Paris. Hence, the fact can be verified by the context.",
            "Judgement": "yes"
        }},
        {{
            "Fact": "2. The Eiffel Tower is the tallest structure in Paris.",
            "Reasoning": "While the context speaks about the popularity of Effiel Tower, it has no mention about its height or whether it is tallest or not. Hence, the the fact can not be verified by the context.",
            "Judgement": "no"
        }},
        {{
            "Fact": "3. The Eiffel Tower is very old.",
            "Reasoning": "While the context mentions that the Eiffel Tower was built in 1880s, it doesn't clarify what very old means.",
            "Judgement": "unclear"
        }},
    ]
}}
    
Return the output only in the corresponding JSON object format. Do not include anything in your response other than this JSON object :

{{ "response":
    [  # List containing data for all the facts
        {{
            "Fact": [1st Fact],  # 1st fact being analysed,
            "Reasoning": [Reasoning for 1st Fact],  # Reasoning to determine if the 1st fact can be verified from the context or not,
            "Judgement": [Judgement for 1st Fact]   # Judgement for 1st fact. Select one of the three - "yes", "unclear" or "no",
            "Reference": [Reference to the context]  # list of one or more sentences from the context that support the fact
            
        }},
       {{
            "Fact": [2nd Fact],  # 2nd fact being analysed,
            "Reasoning": [Reasoning for 2nd Fact],  # Reasoning to determine if the 2nd fact can be verified from the context or not,
            "Judgement": [Judgement for 2nd Fact]   # Judgement for 2nd fact. Select one of the three - "yes", "unclear" or "no",
            "Reference": [Reference to the context]  # list of one or more sentences from the context that support the fact
        }},
        ... # Do for all the facts
    ]
}}
    
Task Data.
[Facts]: {facts}
[Context]: {context}
[Output]:
"""