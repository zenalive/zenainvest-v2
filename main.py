from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS liberado para funcionar com o frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simula status e lucro (você pode importar valores reais do robô depois)
status_do_robo = "ativo"  # ou "erro"
lucro_total = 0.0         # valor atualizado pelo robô futuramente

@app.get("/status")
def status():
    return {
        "status": status_do_robo,
        "lucro": lucro_total
    }
