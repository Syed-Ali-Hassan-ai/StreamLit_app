from prompt_template import memory_prompt_template
from langchain.chains import StuffDocumentsChain, LLMChain, ConversationalRetrievalChain
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate
from langchain.llms import CTransformers
from langchain.vectorstores import Chroma
import chromadb
import yaml

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

def create_llm(model_path = config["model_path"]["large"], model_type = config["model_type"], model_config = config["model_config"]):
    llm = CTransformers(model = model_path, model_type = model_type,config = model_config)
    return llm

def create_chat_memory(chat_history):
    return ConversationBufferWindowMemory(memory_key="history", chat_memory=chat_history, k=3)

def create_embeddings(embeddings_path = config["embeddings_path"]):
    return HuggingFaceInstructEmbeddings(embeddings_path)

def create_llm_chain(llm, chat_prompt, memory):
    return LLMChain(llm = llm, prompt = chat_prompt, memory = memory)

def create_prompt_from_template(template):
    prompt_template = PromptTemplate.from_template(template)
    return prompt_template

def normal_chain(chat_history):
    return chat_chain(chat_history)

class chat_chain():
    def __init__(self, chat_history):
        # initialization code
        self.chat_history = chat_history
        llm = create_llm()
        self.memory = create_chat_memory(chat_history)
        chat_prompt = create_prompt_from_template(memory_prompt_template)
        self.llm_chain = create_llm_chain(llm, chat_prompt, self.memory)

    def run(self, user_input):
        return self.llm_chain.invoke(input={"human_input" : user_input, "history" : self.chat_history} ,stop=["Human:"])["text"]
