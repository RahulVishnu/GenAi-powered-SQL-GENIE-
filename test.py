import streamlit as st
from output import output_res

# st.set_page_config(layout="wide")
hide_menu_style = """<style>#MainMenu {visibility: hidden;}</style>"""
st.markdown(hide_menu_style, unsafe_allow_html=True)

st.image('image.svg', width=50)
st.title('Gen-AI Powered SQl Genie')
st.caption('This demo is powered by OpenAI Service')
st.write('This demo shows how OpenAI Service can be used to answer questions on structured data stored in a SQL database. ')

tab1, tab2, tab3 = st.tabs(["Demo", "Sample questions", "How does this demo work?"])

with tab1:
    #st.write('Try asking a question like:\n\nWhat is Azure? Give me a long answer!')
    question = st.text_input("Question:")

    if question != '':
        answer, prompt = output_res(question)

        st.write(f"**SQL Statement:** {prompt}")
        st.dataframe(answer)
        with st.expander("Click here to see the prompt we've used to generate the answer", expanded=False):
            prompt = prompt.replace('$', '\$')
            st.markdown(f":star: **Short explanation**\n1. The first part of the prompt is the retrieved documents that were likely to contain the answer\n1. The second part is the actual prompt to answer our question\n\n:star: **Prompt:**\n{prompt}")
with tab2:
    st.write('Try asking questions like:')
    col1, col2 = st.columns(2, gap="medium")
    with col1:
        st.markdown("""
* Which company received the highest number of complaints?
* What is the total number of entries in the dataset ?
* How many unique products are represented in the dataset?""")

    with col2:
        st.markdown("""
* What percentage of complaints have a timely response?
* Calculate the percentage of complaints where consumer consent is provided.
* What percentage of entries have a missing ZIP code?""")

    st.write("You can also ask questions in other languages, e.g., try to ask a question in German or Spanish.")

with tab3:
   st.header("How does this demo work?")
   st.markdown("""
               This demo leverages the following components to achieve a ChatGPT-like experience on unstructured documents:
               * **OpenAI Service** to generate answers to questions
               * **Langchain** to query a SQL database containing data to answer the questions
               """)
   #st.image("./architecture.png", caption="Solution Architecture")