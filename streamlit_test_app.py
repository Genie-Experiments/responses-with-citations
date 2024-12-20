from dotenv import load_dotenv
load_dotenv()
from response_with_reference_sentences import response_with_references
import os
from test_data.sample_long_response import LONG_RESPONSE, LONG_CONTEXT
import streamlit as st
from utils import retrieve_context, highlight_sentence


def test_reference_generation_on_short_responses():

    st.title("A short Story")
    
    sample_questions = [
        "What is the name of the Emma's mother ?",
        "What is the story about ?",
        "What was the medical problem with grace ?",
        "Was the medical problem eradicated ?",
        "Was the medical problem advanced or early ?",
        "What was the age of emmma ?"
    ]

    # Dropdown for predefined questions
    query = st.selectbox("Select a question from here or write your own", [""] + sample_questions)


    if query:
        # Retrieve context
        context = retrieve_context(file_path=r"test_data\sample_story.pdf")

        response_object = response_with_references()

        # Generate response
        response,references = response_object.generate_response_and_references(question=query, context=context)

        # generate highlighted context to show on the frontend
        if references:               
            highlighted_context = highlight_sentence(sentences=references, context=context)

        # Create columns for response and context
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Response")
            st.markdown(
                f'<div style="height: 300px; overflow-y: scroll; border: 1px solid #ccc; padding: 10px;">{response}</div>', 
                unsafe_allow_html=True
            )

            with st.container():
                st.subheader("Reference Sentences")
                for i, reference in enumerate(references):
                    st.write(f"{i+1}. {reference}")
        
        with col2:
            st.subheader("Reference highlighted in Context")

            st.markdown(
                f'<div style="height: 300px; overflow-y: scroll; border: 1px solid #ccc; padding: 10px;">{highlighted_context}</div>', 
                unsafe_allow_html=True
            )
    

def test_reference_generation_on_long_responses():

    st.title("A sample response which is long")

    if st.button("Start Processing"):

        response_object = response_with_references()

        # Generate response
        facts_and_references_dictionary = response_object.generate_facts_and_references(context=LONG_CONTEXT, llm_response=LONG_RESPONSE)
        
        # separate facts and references
        facts = []
        references = []
        for dictionary in facts_and_references_dictionary:
            for fact,reference_sentences in dictionary.items():
                facts.append(fact)
                references.extend(reference_sentences)
        
        # generate highlighted context to show on the frontend
        highlighted_context = highlight_sentence(sentences=references, context=str(LONG_CONTEXT))

        # Create columns for response and context
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Response")
            st.markdown(
                f'<div style="height: 300px; overflow-y: scroll; border: 1px solid #ccc; padding: 10px;">{LONG_RESPONSE}</div>', 
                unsafe_allow_html=True
            )
                   
        with col2:
            st.subheader("Reference highlighted in Context")

            st.markdown(
                f'<div style="height: 300px; overflow-y: scroll; border: 1px solid #ccc; padding: 10px;">{highlighted_context}</div>', 
                unsafe_allow_html=True
            )

        with st.container():
            st.subheader("Reference Sentences")
            for dictionary in facts_and_references_dictionary:
                for fact,reference_sentences in dictionary.items():
                    st.write(f"**Fact: {fact}**")
                    st.write(f"**References:**")
                    for reference in reference_sentences:
                        st.write(f'- {reference}')


def main():

    st.set_page_config(layout="wide")
    st.title("Responses With References")

    if "button_clicked" not in st.session_state:
        st.session_state.button_clicked = ""

    if st.button("Example Short Response"):
        st.session_state.button_clicked = "short"

    if st.button("Example Long Response"):
        st.session_state.button_clicked = "long"

    if st.session_state.button_clicked == "short":
        test_reference_generation_on_short_responses()
    elif st.session_state.button_clicked == "long":
        test_reference_generation_on_long_responses()
            


if __name__ == "__main__":
    main()
    