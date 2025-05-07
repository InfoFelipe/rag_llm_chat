from rag_pipeline import RagSystem

class App_System:

        # Inicializar o sitema
        rag_system = RagSystem()
        
        # Carrega os documentos
        rag_system.load_and_process_documents("/home/felipe/Área de trabalho/rag_teste/src/data/teste.txt")
        
        print("Olá! Sou o seu Assistente Virtual. Faça sua pergunta.")
        while True:
            user_input = input("Você: ")
            if user_input.lower() in ["sair", "exit"]:
                print("Tchau! Obrigado! Estou à disposição.")
                break
                
            # Usa o método query() para obter a resposta
            response = rag_system.query(user_input)
            print(f"Bot: {response['answer']}")  # Acessa a chave 'answer' da resposta