
from flask import Flask, request, jsonify, send_from_directory
import urllib.request
import json

app = Flask(__name__)

@app.get("/")
def home():
    return send_from_directory(".", "index.html")

@app.post("/chat")
def chat():
    data = request.get_json(silent=True) or {}
    mensagem = data.get("message", "").strip()

    if not mensagem:
        return jsonify({"reply": "Digite uma mensagem primeiro."}), 400

    payload = json.dumps({
        "model": "qwen2.5:3b",
        "messages": [
            {
                "role": "system",
                "content": (
                    "Seu nome é NEXUS. Você é um assistente pessoal "
                    "inteligente, educado, objetivo e responde em português."
                )
            },
            {"role": "user", "content": mensagem}
        ],
        "stream": False
    }).encode("utf-8")

    req = urllib.request.Request(
        "http://127.0.0.1:11434/api/chat",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=180) as resposta:
            resultado = json.loads(resposta.read().decode("utf-8"))

        texto = resultado.get("message", {}).get(
            "content", "Não consegui gerar uma resposta."
        )
        return jsonify({"reply": texto})

    except Exception as erro:
        print("Erro ao consultar Ollama:", erro)
        return jsonify({
            "reply": "Não consegui acessar a IA. Confira se o Ollama está aberto."
        }), 502

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
