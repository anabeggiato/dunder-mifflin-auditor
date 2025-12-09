import os
import google.generativeai as genai
from dotenv import load_dotenv

# 1. IMPORTAÇÃO ATUALIZADA
from src.compliance_rag import consultar_politica_compliance
from src.data_analyst import (
    analisar_gastos_por_categoria, 
    listar_maiores_gastos, 
    calcular_estatisticas_categoria
)

load_dotenv()
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# 2. LISTA DE FERRAMENTAS ATUALIZADA
tools = [
    consultar_politica_compliance,
    analisar_gastos_por_categoria,
    listar_maiores_gastos,
    calcular_estatisticas_categoria
]

# 3. MODELO COM SYSTEM PROMPT MELHORADO
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash", 
    tools=tools,
    system_instruction="""
    Você é o 'Auditor IA' da Dunder Mifflin. 
    
    SUAS FERRAMENTAS:
    1. 'consultar_politica_compliance': Para regras e leis.
    2. 'analisar_gastos_por_categoria': Para verificar LIMITES (ex: "gastou mais de 100").
    3. 'listar_maiores_gastos': Para ver o TOP X gastos gerais.
    4. 'calcular_estatisticas_categoria': USE SEMPRE que pedirem SOMA, TOTAL, MÉDIA, MÍNIMO ou CONTAGEM de uma categoria específica (ex: "total de correio", "menor viagem").
    5. 'investigar_emails': Para ler conversas.

    DICA: Se perguntarem "qual o menor gasto", use a métrica 'minimo'. Se perguntarem "quanto gastamos no total", use 'total'.
    """
)

chat = model.start_chat(enable_automatic_function_calling=True)

def main():
    print(f"👔 Auditoria 2.0 Iniciada...")
    
    while True:
        user_input = input("\n📝 Toby/Usuário: ")
        if user_input.lower() in ["sair", "exit", "quit"]:
            break
            
        try:
            response = chat.send_message(user_input)
            print(f"Auditor: {response.text}")
            
        except Exception as e:
            print(f"Erro: {e}")

if __name__ == "__main__":
    main()