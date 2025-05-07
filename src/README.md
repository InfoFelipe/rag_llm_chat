# Projeto

Este é um projeto para criação de chatbots com RAG usando LangChain e o modelo de linguagem Mistral. Nele você poderá arquivos em uma pasta e fazer com que o chatbot responda com informações obtidades dele.
* **Porque utilizei o o modelo de linguagem Mistral:**
  1. Mistral é um modelo open-source.
  2. Ele é leve, gratuito e eficiente.
  3. Roda bem localmente com Ollama.
  4. Oferece bom desempenho com RAG.

1. **Pré-requisitos**
   * Certifique-se de ter o Python 3.12.5 instalado em seu Sistema Operacional.
   * Instale o Git se ainda não tiver, para clonar repositórios e gerenciar o código (opcional).

2. **Estrutura de Arquivos e Pastas**
    * src/app.py: Contém a lógica do chatbot.
    * src/main.py: Ponto de entrada do projeto.
    * src/rag_pipeline.py: Lida com a pipeline RAG (Retrieval-Augmented Generation).
    * src/data/teste.txt/: Arquivo usado para análise ou busca.
      
3. **Explicação sobre o código**
   
    1.  **src/rag_pipeline.py**:
     
       Este código implementa um sistema RAG (Retrieval-Augmented Generation) usando a biblioteca LangChain. O objetivo do sistema é responder a perguntas com base em documentos fornecidos, combinando recuperação de informações (vectorstore) e geração de linguagem natural (LLM). Abaixo está uma explicação das principais partes do código:
       
       Importações:
          
          Essas bibliotecas são utilizadas para:
  
            * FAISS: armazenamento vetorial eficiente para busca semântica.
            
            * HuggingFaceEmbeddings: modelo para gerar vetores de embeddings (representação numérica do texto).
            
            * TextLoader: carrega textos brutos de arquivos.
            
            * RecursiveCharacterTextSplitter: divide o texto em partes menores (chunks).
            
            * ChatPromptTemplate: define o prompt que será usado pela LLM.
            
            * create_retrieval_chain, create_stuff_documents_chain: criam as cadeias RAG.
            
            * Ollama: integra um LLM local ou em container (ex: Mistral).
            
            * logging, os, typing: utilitários do Python.

   **`class RagSystem`**: Responsável por organizar e encapsular todo o fluxo do sistema RAG.

   `__init__`
        
          * Inicializa o modelo de linguagem (Ollama) e o modelo de embeddings (HuggingFaceEmbeddings).
          
          * Define variáveis para o banco vetorial e o mecanismo de recuperação (retriever).
          
   `load_and_process_documents`
        
          * Valida o caminho do arquivo.
          
          * Carrega o texto com TextLoader.
          
          * Divide o texto em trechos com RecursiveCharacterTextSplitter (para processar melhor com embeddings).
          
          * Cria o vetorstore FAISS, indexando os chunks com seus embeddings.
          
          * Cria um retriever, que permitirá buscar os chunks mais relevantes para uma pergunta.
          
   `_create_prompt_template (estático)`
        
          * Define o prompt usado pela LLM, com instruções sobre como responder.
          
          * Usa placeholders `{context}` e `{input}` para inserir o contexto recuperado e a pergunta do usuário.
          
   `query`
        
          * Verifica se o retriever foi inicializado (ou seja, se os documentos foram carregados).
          
          * Cria a cadeia RAG:
          
            * A retrieval_chain combina a recuperação de documentos com a geração da resposta.
          
          * Executa a cadeia passando a pergunta e retorna a resposta e o contexto utilizado.
            
      ### Resumo do fluxo de execução
          1. Inicialização: define o modelo de linguagem e o modelo de embeddings.
          
          2. Carregamento de documentos: lê um arquivo de texto, divide-o e cria um índice vetorial.
          
          3. Consulta: ao receber uma pergunta, busca trechos relevantes no vetorstore e gera uma resposta com base neles.

     2.  **src/app.py**
        
     3.  **src/main.py**
        
   O código fornecido configura o ambiente de logging, inicializa a aplicação e gerencia o encerramento adequado da aplicação.
   
        Importações:
        
        Essas bibliotecas são utilizadas para: 

          *  App_System: Importa a classe App_System que você definiu anteriormente, responsável por gerenciar a interação com o usuário e o sistema RAG.
          
          * logging:Módulo usado para configurar o logging e registrar mensagens de eventos ou erros da aplicação.
          
          * sys:  Módulo usado para interagir com o sistema operacional, no caso, para encerrar a aplicação.
          
          * NoReturn: Tipo de retorno do Python para indicar que a função não retorna um valor (usado em funções que encerram o programa).
   
**`Função configure_logging`**
   
  * **Objetivo**: Configurar o sistema de logging da aplicação.

  * level=logging.INFO: Define que as mensagens de log a partir do nível INFO (informações gerais) e acima (como ERROR) serão registradas.
    
  * format: Define o formato das mensagens de log, incluindo a data/hora (%(asctime)s), nome do logger (%(name)s), nível do log (%(levelname)s) e a mensagem (%(message)s).
    
  * handlers: Especifica os manipuladores de saída para os logs:
    
  * logging.FileHandler('app.log'): Escreve as mensagens de log no arquivo app.log.
    
  * logging.StreamHandler(): Exibe as mensagens de log no console (fluxo padrão de saída).
      
**`Função configure_logging`**
   
  * **Objetivo**: Finalizar a execução da aplicação de forma controlada, registrando uma mensagem e, se necessário, fornecendo um código de saída.
    
  * message: A mensagem de log que será registrada antes de encerrar a aplicação.
    
  * exit_code: O código de saída do sistema. O valor padrão é 0, indicando sucesso. Se for diferente de zero, indica erro.
    
  * sys.exit(exit_code): Encerra a aplicação e retorna o código de saída ao sistema operacional.

**`if __name__ == "__main__`**: 
  * Este bloco é executado apenas quando o script é executado diretamente, e não quando importado como módulo em outro código.

### Resumo do fluxo de execução
  * A aplicação começa configurando o sistema de logging.
  
  * Em seguida, tenta executar a aplicação RAG (através de App_System()).
  
  * Se tudo correr bem, a aplicação será encerrada de forma controlada com uma mensagem de sucesso.
  
  * Se o usuário interromper a execução ou se ocorrer algum erro, a aplicação é encerrada de maneira controlada, com mensagens apropriadas registradas no log.

