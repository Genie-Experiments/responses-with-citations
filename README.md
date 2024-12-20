# Responses with References/Citations

This project is designed to generate responses to questions based on a given context and provide reference sentences from the context that support the response. It uses a combination of OpenAI's GPT-4 model and Streamlit for the frontend interface.

## Project Structure
```bash
__pycache__/
.env
prompts.py
response_with_reference_sentences.py
streamlit_test_app.py
test_data/
    __pycache__/
    sample_long_response.py
utils.py
```

## Installation

1. Clone the repository:
   ```bash
   git clone [https://github.com/yourusername/Agentic-RAG.git](https://github.com/Genie-Experiments/responses-with-citations.git)

2. Create and activate a virtual environment:
  ```bash
  python -m venv venv
  source venv/bin/activate  # On Windows use `venv\Scripts\activate`
  ```

3. Install the required packages:
  ```bash
  pip install -r requirements.txt
```

4. Set up environment variables:
  Create a .env file in the root directory and add the following variables:
  ```bash
  OPENAI_API_KEY="your_openai_api_key"
  GROQ_API_KEY="your_groq_api_key"
  ```
## Usage
To start the Streamlit application, run:
  ```bash
  streamlit run streamlit_test_app.py
  ```

## Key Files
  - .env: Contains API keys for OpenAI and Groq.
  - prompts.py: Contains prompt templates used to generate responses, facts, and references.
  - response_with_reference_sentences.py: Implements the response_with_references class that interacts with the LLM to generate responses, facts, and references.
  - streamlit_test_app.py: Streamlit application to test the reference generation on short and long responses.
  - test_data/sample_long_response.py: Contains sample long context and response data used for testing.
  - utils.py: Utility functions for extracting text from PDFs, counting tokens, and highlighting sentences in the context.

## Functions

  **response_with_reference_sentences.py**
  
  - generate_response_and_references: Generates a response and reference sentences from the LLM based on the given question and context.
  - generate_facts: Generates facts from the LLM based on the given response and context.
  - generate_references_from_facts: Generates references from facts using the LLM based on the given facts and context.
  - generate_facts_and_references: Generates facts and references from the LLM based on the given response and context.

**streamlit_test_app.py**
  - retrieve_context: Retrieves text from a PDF file.
  - count_tokens_tiktoken: Counts the number of tokens in a text using the tiktoken library.
  - highlight_sentence: Highlights sentences in the context.
  - test_reference_generation_on_short_responses: Tests reference generation on short responses.
  - test_reference_generation_on_long_responses: Tests reference generation on long responses.
  - main: Main function to run the Streamlit app.

**utils.py**
  - retrieve_context: Extracts text from a PDF file.
  - count_tokens_tiktoken: Counts the number of tokens in a text using the tiktoken library.
  - highlight_sentence: Highlights sentences in the context.
