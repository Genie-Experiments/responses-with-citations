import pdfplumber
import tiktoken
import re

def retrieve_context(file_path:str) -> str:

    """
    Extracts text from a PDF file.

    Parameters:
    file_path (str): The path to the PDF file.

    Returns:
    str: The extracted text from the PDF.
    """

    with pdfplumber.open(file_path) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text()
    return text

    
def count_tokens_tiktoken(text:str) -> int:
        
    """
    Counts the number of tokens in a text using the tiktoken library.

    Parameters:
    text (str): The text to be tokenized.

    Returns:
    int: The number of tokens in the text.
    """

    model="gpt-4o"

    # Load the encoding for the specified model
    encoding = tiktoken.encoding_for_model(model)
    
    # Encode the text and return the number of tokens
    tokens = encoding.encode(text)
    
    return len(tokens)


def highlight_sentence(sentences: list[str], context: str) -> str:
    
    """
    Highlights sentences in the context.

    Parameters:
    sentences (list[str]): The list of sentences to be highlighted.
    context (str): The context from which the response and reference sentences are generated.

    Returns:
    str: The context with highlighted sentences.
    """

    print("Generating highlighted context ...")

    # normalize the context string
    context_normalized = re.sub(r'\s+', ' ', context)
    context_normalized = context_normalized.replace("“", '"').replace("”", '"')
    highlighted_context = context_normalized

    for sentence in sentences:
        # Escape special regex characters in the sentence to prevent regex interpretation
        normalized_sentence = re.sub(r'\s+', ' ', sentence)
        normalized_sentence = normalized_sentence.replace("“", '"').replace("”", '"')
        escaped_sentence = re.escape(normalized_sentence)

        # Create a regex pattern that matches the exact sentence
        pattern = r'([^\w]|^)' + escaped_sentence + r'([^\w]|$)'
        
        # Replace the sentence with marked version
        highlighted_context = re.sub(pattern, f'<mark style="background-color:yellow">{sentence}</mark>', highlighted_context, flags=re.IGNORECASE) 
    
    return highlighted_context