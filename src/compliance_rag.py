import os
import google.generativeai as genai
import chromadb
from chromadb.utils import embedding_functions

# Configurações iniciais
DATA_PATH = os.path.join("data", "politica_compliance.txt")

class ComplianceRAG:
    def __init__(self):
        # Inicializa o cliente do ChromaDB (banco vetorial temporário na memória ou disco)
        self.chroma_client = chromadb.PersistentClient(path="./chroma_db")
        self.collection_name = "dunder_policy"
        
        # Tenta pegar a coleção existente ou cria uma nova
        self.collection = self.chroma_client.get_or_create_collection(name=self.collection_name)
        
        # Se a coleção estiver vazia, fazemos a ingestão dos dados
        if self.collection.count() == 0:
            print("Indexando política de compliance pela primeira vez...")
            self.ingest_data()

    def ingest_data(self):
        """Lê o arquivo de texto, quebra em pedaços e salva no ChromaDB."""
        if not os.path.exists(DATA_PATH):
            raise FileNotFoundError(f"Arquivo não encontrado em: {DATA_PATH}")

        with open(DATA_PATH, "r", encoding="utf-8") as f:
            text = f.read()

        # split por parágrafos
        chunks = [chunk for chunk in text.split("\n\n") if chunk.strip()]
        
        # Cria IDs únicos para cada chunk
        ids = [f"id_{i}" for i in range(len(chunks))]
        
        self.collection.add(
            documents=chunks,
            ids=ids
        )
        print(f"{len(chunks)} trechos da política indexados com sucesso!")

    def retrieve_context(self, query: str, n_results: int = 3):
        """Busca os trechos mais relevantes para a pergunta."""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        # Retorna apenas a lista de textos encontrados
        return results["documents"][0]

# Função auxiliar para ser usada como Tool pelo Gemini
def consultar_politica_compliance(pergunta: str):
    """
    Use esta ferramenta para responder dúvidas sobre as regras, leis e 
    diretrizes da empresa Dunder Mifflin.
    Args:
        pergunta: A dúvida específica sobre a política.
    """
    rag = ComplianceRAG()
    contextos = rag.retrieve_context(pergunta)
    return "\n\n".join(contextos)