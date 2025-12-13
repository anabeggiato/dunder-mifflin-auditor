import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

try:
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    
    print("🔍 Buscando modelos disponíveis para sua chave API...\n")
    found_flash = False
    
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
            if "flash" in m.name:
                found_flash = True

    print("\n" + "="*30)
    if found_flash:
        print("✅ Ótimo! O modelo Flash está disponível.")
    else:
        print("⚠️ O modelo Flash não apareceu na lista.")
        print("Tente usar 'models/gemini-pro' ou 'models/gemini-1.5-pro-latest'")

except Exception as e:
    print(f"❌ Erro de autenticação ou conexão: {e}")