import os

# Caminho para o arquivo de e-mails
EMAIL_PATH = os.path.join("data", "emails.txt")

def carregar_emails():
    if not os.path.exists(EMAIL_PATH):
        return "ERRO: O arquivo 'emails_internos.txt' não foi encontrado na pasta data/."
    
    with open(EMAIL_PATH, "r", encoding="utf-8") as f:
        return f.read()

def investigar_emails(topico_investigacao: str):
    conteudo = carregar_emails()
    
    return f"""
    --- INÍCIO DO DUMP DE EMAILS ---
    {conteudo}
    --- FIM DO DUMP DE EMAILS ---

    O USUÁRIO SOLICITOU UMA ANÁLISE SOBRE: '{topico_investigacao}'.
    Analise as conversas acima e extraia as evidências relevantes para esse tópico.
    CITE OS REMETENTES E AS DATAS (se houver) DAS MENSAGENS SUSPEITAS.
    """