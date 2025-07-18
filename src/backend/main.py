import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi_mcp import FastApiMCP
from routes import document, storage, llm

# Carrega variáveis de ambiente do .env na raiz do backend
backend_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(backend_dir, '.env')
load_dotenv(dotenv_path=env_path)

"""
 Configuração da aplicação FastAPI 
"""
app = FastAPI(title="Documento RAG API", version="2.0.0")

"""
Configurar CORS
- Permitir todas as origens, métodos e cabeçalhos
"""
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

app.include_router(document.router)
app.include_router(storage.router)
app.include_router(llm.router)

"""
Rota de health check
"""


@app.get("/health")
def health_check():
    return {"status": "ok"}


"""
Configuração do MCP (Multi-Client Protocol)
"""
mcp = FastApiMCP(
    app,
    name="Documento RAG - MCP",
    description="Server MCP para a aplicação Documento RAG",
    include_operations=["list_documents", "search_documents", "list_files", "ask_question"]
)
mcp.mount()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8002, reload=True)
