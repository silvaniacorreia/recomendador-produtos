# Projeto de Recomendação com Vertex AI 

Este repositório contém um projeto de ponta a ponta de recomendação de produtos em um marketplace, utilizando técnicas de aprendizagem de máquina.

## Etapa 1 — ELT dos dados da Olist

Nesta etapa, realizei o processo de Transform dos dados brutos extraídos do dataset público da Olist. O pipeline executado:

- Carregamento múltiplos arquivos CSV do Google Cloud Storage (GCS)
- Junção de tabelas relevantes: `orders`, `order_items`, `products`
- Remoção de registros com valores nulos críticos para o modelo
- Conversão de datas
- Resultado salvo como `historico_compras_clientes.csv`, pronto para ser utilizado na modelagem de recomendação

🗂️ Arquivos relacionados:
- `elt_dados_projeto.ipynb`: Notebook da transformação
- `historico_compras_clientes.csv`: Dataset unificado
- `data/readme_dataset.md`: Documentação dos dados de origem
