import os
import google.generativeai as genai
from dotenv import load_dotenv

# --- IMPORTAÇÃO DAS 3 FERRAMENTAS ---
from src.compliance_rag import consultar_politica_compliance
from src.data_analyst import (
    analisar_gastos_por_categoria, 
    listar_maiores_gastos,
    calcular_estatisticas_categoria
)

from src.email_forensics import investigar_emails

load_dotenv()
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# --- LISTA DE FERRAMENTAS ---
tools = [
    consultar_politica_compliance,
    analisar_gastos_por_categoria,
    listar_maiores_gastos,
    calcular_estatisticas_categoria,
    investigar_emails  # <--- Adicionado
]

# --- CONFIGURAÇÃO DO MODELO E DO AGENTE ---
system_instruction = """
Você é o Agente de Auditoria Inteligente da Dunder Mifflin.
Sua missão é auxiliar Toby Flenderson a encontrar erros, fraudes e quebras de compliance.

VOCÊ TEM ACESSO ÀS SEGUINTES FERRAMENTAS:O Michael Scott está planejando algo contra o Toby? O que dizem os e-mails?
1. 'consultar_politica_compliance': Use para tirar dúvidas sobre REGRAS (ex: limites de valor, o que é permitido).
2. Ferramentas Financeiras ('analisar_gastos...', 'listar_maiores...', 'calcular_estatisticas...'): Use para ver NÚMEROS e EXTRATOS.
3. 'investigar_emails': Use para ler conversas, detectar CONLUIOS, SENTIMENTOS ou INTENÇÕES.

COMO RESOLVER PROBLEMAS COMPLEXOS (RACIOCÍNIO):
- Se o usuário perguntar sobre FRAUDE COMPLEXA (ex: "Eles combinaram desviar dinheiro?"):
  Passo A: Use 'investigar_emails' para achar a conversa suspeita e identificar valores ou datas.
  Passo B: Use as ferramentas financeiras para confirmar se aquele gasto realmente aconteceu na planilha.
  Passo C: Responda citando o e-mail (evidência de intenção) e a transação (evidência material).

- Se perguntarem sobre a RELAÇÃO MICHAEL vs TOBY:
  Use 'investigar_emails' focando em hostilidade ou planos secretos.

SEMPRE justifique suas respostas com os dados encontrados.
"""

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    tools=tools,
    system_instruction=system_instruction
)

chat = model.start_chat(enable_automatic_function_calling=True)

def main():
    print("🕵️  Auditor Dunder Mifflin - Sistema Completo Ativo")
    print("---------------------------------------------------")
    
    while True:
        try:
            user_input = input("\n📝 Toby: ")
            if user_input.lower() in ["sair", "exit"]:
                break
            
            print("⏳ Investigando...")
            response = chat.send_message(user_input)
            print(f"🤖 Auditor: {response.text}")
            
        except Exception as e:
            print(f"❌ Erro: {e}")

if __name__ == "__main__":
    main()