from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain 
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.llms import Ollama 
from typing import Dict, Any
import os
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RagSystem:

    def __init__(self, model_name: str = "mistral", embedding_model: str = "all-MiniLM-L6-v2"):
        """Inicializa o sistema RAG.
        
        Args:
            model_name: Nome do modelo LLM a ser usado via Ollama
            embedding_model: Nome do modelo de embeddings da HuggingFace
        """
        try:
            self.llm = Ollama(model=model_name)
            self.embeddings = HuggingFaceEmbeddings(model_name=embedding_model)
            self.vectorstore = None
            self.retriever = None
            logger.info("Sistema RAG inicializado com sucesso")
        except Exception as e:
            logger.error(f"Erro ao inicializar o sistema RAG: {e}")
            raise

    def load_and_process_documents(self, file_path: str, chunk_size: int = 500, chunk_overlap: int = 50) -> None:
        """Carrega e processa documentos para criar o vetorstore.
            
        Args:
            file_path: Caminho para o arquivo de texto
            chunk_size: Tamanho dos chunks para divisão do texto
            chunk_overlap: Sobreposição entre chunks
        """
        try:
        # Validação do caminho do arquivo
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
            
            # Carrega o documento
            loader = TextLoader(file_path)
            documents = loader.load()
            
            # Divide o texto
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap
            )
            splits = text_splitter.split_documents(documents)
            
            # Cria o banco vetorial
            self.vectorstore = FAISS.from_documents(
                documents=splits, 
                embedding=self.embeddings
            )
            self.retriever = self.vectorstore.as_retriever()
            logger.info(f"Documento {file_path} processado com sucesso")
            
        except Exception as e:
            logger.error(f"Erro ao processar documentos: {e}")
            raise

    @staticmethod
    def _create_prompt_template() -> ChatPromptTemplate:
        """Cria o template de prompt para a cadeia RAG."""
        system_prompt = (
            "Você é um assistente virtual para tarefas de perguntas e respostas. "
            "Use trechos de contexto recuperado para responder "
            "à pergunta. Se você não souber a resposta, diga que não sabe. "
            "Seja conciso e preciso em suas respostas.\n\n"
            "Contexto:\n{context}"
        )
        
        return ChatPromptTemplate.from_messages([
            ("system", system_prompt), 
            ("human", "{input}")
        ])
    
    def query(self, question: str) -> Dict[str, Any]:
        """Executa uma consulta no sistema RAG."""
        if not self.retriever:
            raise ValueError("O retriever não foi inicializado. Carregue documentos primeiro.")
        
        try:
            # Criação da cadeia RAG
            prompt = self._create_prompt_template()
            question_answer_chain = create_stuff_documents_chain(self.llm, prompt)
            rag_chain = create_retrieval_chain(self.retriever, question_answer_chain)
            
            # Execução
            response = rag_chain.invoke({"input": question})
            
            logger.info(f"Consulta processada: {question}")
            return {
                "answer": response["answer"],
                "context": response["context"],
                "question": question
            }
            
        except Exception as e:
            logger.error(f"Erro ao processar a consulta '{question}': {e}")
            return {
                "answer": "Desculpe, ocorreu um erro ao processar sua pergunta.",
                "error": str(e)
            }
