# Projeto de Recomendação com Vertex AI 

Este repositório apresenta uma solução de recomendação de produtos em um marketplace, utilizando técnicas de aprendizado de máquina com foco em pipelines escaláveis via Google Cloud (Vertex AI). O projeto foi idealizado para fins de estudo, visando consolidar conhecimentos em MLOps, AutoML, deploy, monitoramento e boas práticas em projetos de dados.

---

## Objetivo

Criar um sistema que recomende produtos personalizados para usuários de e-commerce com base em seu histórico de compras. O objetivo do modelo é prever a **categoria de produto mais provável** que o cliente pode se interessar, utilizando dados tabulares.

---

## Etapa 1 — ELT dos dados da Olist

Nesta etapa, foi realizado o processo de transformação dos dados brutos (Olist Public Dataset), com foco na unificação de múltiplas tabelas para gerar um histórico de comportamento por cliente.

### Pipeline:
- Carregamento de múltiplos arquivos `.csv` do GCS
- Junção das tabelas: `orders`, `order_items`, `products`, `customers`
- Conversão de colunas de data
- Exclusão de registros com campos nulos críticos
- Definição da variável-alvo (`categoria_mais_frequente`) por cliente
- Salvo em: `historico_compras_clientes.csv`
- Enriquecimento da base com features agregadas, com arquivo final salvo em: `base_modelo.csv`

**Arquivos:**
- `elt_dados_projeto.ipynb`: Notebook com a transformação
- `historico_compras_clientes.csv`: Dataset final para enriquecimento
- `readme_dataset.md`: Descrição dos campos e tabelas
- `base_modelo.csv`: Dataset enriquecido, pronto para modelagem.
---

## Etapa 2 — Modelagem com Vertex AI AutoML

O dataset foi carregado na plataforma Vertex AI como dado **tabular**. A modelagem utilizou o AutoML, que testou algoritmos automaticamente e escolheu o melhor baseado nas métricas de classificação.

### Features usadas:
- `estado_cliente` (categorical)
- `cidade_cliente` (categorical)
- `recencia_compra` (numeric)
- `product_id` (text/categorical)
- `categoria_mais_frequente` (target)

### Principais métricas:

| Métrica               | Valor    |
|-----------------------|----------|
| ROC AUC               | 0.958    |
| PR AUC                | 0.632    |
| Log Loss              | 1.65     |
| F1 Score (micro)      | 0.66     |
| F1 Score (macro)      | 0.50     |
| Precisão (micromédia) | 100%     |
| Recall (micromédia)   | 49,6%    |

**Feature mais relevante segundo o AutoML:** `product_id`  
**Risco de *data leakage*:** O `product_id` guarda informações muito próximas da variável alvo (`categoria_mais_frequente`) e pode viciar o modelo. Essa feature foi mantida apenas para fins exploratórios nesta etapa.

---

## Etapa 3 — Deploy e Monitoramento

- Modelo implantado em um **endpoint gerenciado do Vertex AI**
- Criado serviço para realizar **predições em tempo real**
- Configurado monitoramento do modelo com foco em **data drift (deslocamento de distribuição dos dados de entrada)**

O monitoramento garante que o modelo continue válido mesmo com a mudança de comportamento dos usuários ao longo do tempo.

---

## Etapa 4 — Geração da Recomendação

A previsão da categoria por cliente é utilizada para sugerir produtos dentro dessa categoria com maior relevância histórica.

Integração com um **dicionário de ranking de produtos por categoria**, criado a partir do histórico de vendas.

**Arquivos:**
- `ranking_produtos.json`: Produtos mais vendidos por categoria
- `testa_endpoint_vertex.py`: Script para:
  - Chamar o endpoint do Vertex AI
  - Interpretar a resposta da predição
  - Retornar top-N produtos recomendados com base na categoria

---

## Limitações e Possíveis Melhorias

**Sobre o dataset e modelagem atual:**
- **Recall ainda baixo (~49%)**: apesar da precisão alta, o modelo deixa de identificar corretamente muitas categorias reais. Para casos de recomendação, **recall é mais importante** — é melhor sugerir mais do que não sugerir nada.
- **Classe desbalanceada**: certas categorias possuem muito mais registros, o que dificulta a predição correta das menos frequentes.
- **Feature `product_id` introduz vazamento de dados**: o modelo pode estar se apoiando em informações que não estariam disponíveis no momento real da predição, por exemplo, casos em que o produto é sugerido sem considerar o histórico de compras do usuário.
- **Poucas features contextuais**, devido a limmitações da base utilizada. Por este motivo, não consideramos informações como:
  - Frequência de compra
  - Ticket médio do cliente
  - Sazonalidade (mês, feriado, Black Friday etc.)
  - Similaridade entre produtos
- **Modelo treinado com abordagem de classificação**: não usamos modelos colaborativos nem embeddings, que seriam mais adequados para recomendação personalizada.

**Melhorias propostas:**
- Remover `product_id` e testar impacto na generalização
- Adicionar mais features como preço, mês da compra, entre outras que possam ser relevantes ao modelo
- Agrupar categorias semelhantes para mitigar sparsidade
- Explorar modelos personalizados com TensorFlow ou PyTorch
- Utilizar técnicas clássicas de recomendação:
  - *Matrix Factorization*
  - *Item-based KNN*
  - *Neural Collaborative Filtering*
- Implementar retreinamento automático via **Vertex Pipelines**
- Realizar avaliação com conjuntos de validação externos

---

## Próximos Passos

- Implementar agendamento de retreinamento baseado em detecção de *drift*
- Testar recomendadores personalizados fora do AutoML
- Avaliar modelos com mais foco em *recall* e *diversidade* de recomendações
- Integrar modelo com front-end de vitrine simulada (ex: Streamlit)
