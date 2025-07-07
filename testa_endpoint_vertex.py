from google.cloud import aiplatform
from google.cloud.aiplatform.gapic.schema import predict
import json
import os
from dotenv import load_dotenv


load_dotenv()

# Carregando variáveis de ambiente
PROJECT_ID = os.getenv("PROJECT_ID")
LOCATION = os.getenv("LOCATION")
ENDPOINT_ID = os.getenv("ENDPOINT_ID")

aiplatform.init(
    project=PROJECT_ID,
    location=LOCATION,
)

def chamar_endpoint(endpoint_id, instancia_input):
    endpoint = aiplatform.Endpoint(endpoint_name=endpoint_id)

    prediction = endpoint.predict(
        instances=[instancia_input],
        parameters={}
    )

    return prediction

def recomendar_produtos(resposta_modelo, dicionario_produtos, top_n_categorias=1):
    predictions = resposta_modelo.predictions[0]

    categorias_conf = list(zip(predictions["classes"], predictions["scores"]))
    categorias_conf.sort(key=lambda x: x[1], reverse=True)
    categorias_top = categorias_conf[:top_n_categorias]

    recomendacoes = {}
    for categoria, confianca in categorias_top:
        produtos = dicionario_produtos.get(categoria, [])
        recomendacoes[categoria] = {
            "confiança": round(confianca, 2),
            "produtos": produtos
        }

    return recomendacoes

def main():
    instancia = {
        "estado_cliente": "SP",
        "cidade_cliente": "sorocaba",
        "recencia_compra": "440",
        "product_id": "6522b16614da30655a6a5ce4c8f2fb8b"
    }

    json_path = os.path.join(os.path.dirname(__file__), "ranking_produtos.json")

    if not os.path.exists(json_path):
        print("Arquivo JSON não encontrado!")
        return

    with open(json_path, "r") as file:
        ranking_produtos_por_categoria = json.load(file)

    # Previsão
    try:
        resposta = chamar_endpoint(ENDPOINT_ID, instancia)
        recomendacoes = recomendar_produtos(resposta, ranking_produtos_por_categoria, top_n_categorias=2)

        for categoria, dados in recomendacoes.items():
            print(f"Categoria recomendada: {categoria} (confiança: {dados['confiança']})")

            for produto in dados["produtos"] [:3]:
                print(f" - {produto}")
    except Exception as e:
        print("Erro:", e)

if __name__ == "__main__":
    try:
        aiplatform.init(project=PROJECT_ID, location=LOCATION)

        main()
    except Exception as e:
        print("Erro na inicialização ou execução:", e)
