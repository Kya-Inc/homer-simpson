import streamlit as st
from typing import Literal
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import StreamlitChatMessageHistory
from langchain.prompts import PromptTemplate, ChatPromptTemplate, FewShotChatMessagePromptTemplate, MessagesPlaceholder

## chat model

user_name="fielding"
character_name="homer"

from homer_example_selector import HomerExampleSelector

from prompt_templates import MAIN_TEMPLATE, SYSTEM_NOTE_TEMPLATE, NSFW_TEMPLATE, TASK_TEMPLATE, EXAMPLES_PREFACE_TEMPLATE
from character_data import character_data

if "sidebar_state" not in st.session_state:
    st.session_state.sidebar_state = "expanded"

st.set_page_config(
    page_title="Mimicking a Character via Explicit and Implicit Instructions",
    initial_sidebar_state=st.session_state.sidebar_state,
)
st.title("Homer Simpson")
st.caption("Mimicking a Character via Explicit and Implicit Instructions")

openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")

if not openai_api_key:
    st.session_state.sidebar_state = "expanded"
    st.error("Please add your OpenAI API key to the sidebar.")
    st.stop()
else:
    st.session_state.sidebar_state = "collapsed"

view_info = st.expander("What's this all about?", expanded=True)

with view_info:
    """
    This builds on a previous demonstration where we instructed a pre-trained model to mimic a character implicitly through semantically similar few-shot examples. In this demo, we will explore how to combine explicit instructions with implicit instructions to further improve the model's ability to mimic a character.
    """

msgs = StreamlitChatMessageHistory(key="langchain_messages")
memory = ConversationBufferMemory(
    chat_memory=msgs, ai_prefix="Homer", human_prefix="Fielding", input_key="human_input", return_messages=True
)

example_selector = HomerExampleSelector()

examples_prompt = FewShotChatMessagePromptTemplate(
    example_selector=example_selector,
    example_prompt=ChatPromptTemplate.from_messages([
        ("human", "{prompt}"),
        ("ai", "{response}")
    ]),
    input_variables=["human_input"],
)

system_note_template = PromptTemplate.from_template(SYSTEM_NOTE_TEMPLATE)
nsfw_template = PromptTemplate.from_template(NSFW_TEMPLATE)
main_prompt = PromptTemplate.from_template(MAIN_TEMPLATE.format(**character_data))

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_NOTE_TEMPLATE),
    ("system", NSFW_TEMPLATE),
    ("system", MAIN_TEMPLATE.format(**character_data)),
    ("system", EXAMPLES_PREFACE_TEMPLATE.format(user_name=user_name, character_name=character_name)),
    examples_prompt,
    ("system", TASK_TEMPLATE.format(character_name=character_name, user_name=user_name)),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{human_input}"),
])

llm_chain = LLMChain(
    llm=ChatOpenAI(openai_api_key=openai_api_key, model="gpt-4"),
    prompt=chat_prompt,
    memory=memory,
    verbose=True,
)


for msg in msgs.messages:
    AVATAR: Literal['img/homer.png', 'img/anon.png'] = "img/homer.png" if msg.type == "ai" else "img/anon.png"
    st.chat_message(msg.type, avatar=AVATAR).write(msg.content)

if prompt := st.chat_input():
    st.chat_message("human", avatar="img/anon.png").write(prompt)
    response = llm_chain.run(prompt)
    st.chat_message("ai", avatar="img/homer.png").write(response)
