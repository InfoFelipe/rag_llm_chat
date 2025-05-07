from rag_pipeline import RagSystem

def app_system():
    """
    Inicializa o sistema RAG, carrega os documentos e interage com o usuário via terminal.
    """
    # Inicializa o sistema RAG
    rag_system = RagSystem()
    
    # Caminho do arquivo de dados
    document_path = "/home/felipe/Área de trabalho/rag_teste/src/data/teste.txt"
    
    try:
        # Carrega e processa os documentos
        rag_system.load_and_process_documents(document_path)
        print("Documentos carregados com sucesso.")
    except Exception as e:
        print(f"Erro ao carregar documentos: {e}")
        return

    print("\nOlá! Sou o seu Assistente Virtual. Faça sua pergunta.")
    print("Digite 'sair' ou 'exit' para encerrar.\n")

    while True:
        user_input = input("Você: ").strip()
        
        if user_input.lower() in {"sair", "exit"}:
            print("Tchau! Obrigado! Estou à disposição.")
            break

        try:
            # Consulta o sistema com a entrada do usuário
            response = rag_system.query(user_input)
            print(f"Bot: {response.get('answer', 'Desculpe, não consegui encontrar uma resposta.')}")
        except Exception as e:
            print(f"Erro ao processar a consulta: {e}")