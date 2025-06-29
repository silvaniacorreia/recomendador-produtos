# Documentação do Dataset - Olist E-commerce

## Descrição Geral

Este projeto utiliza o **Brazilian E-Commerce Public Dataset by Olist**, disponível gratuitamente no [Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce). O conjunto de dados reflete transações reais de um marketplace no Brasil entre 2016 e 2018.

O dataset original contém múltiplas tabelas que cobrem o ciclo de vida completo de um pedido: desde o cadastro do cliente e do produto até o pagamento, entrega e avaliação do consumidor.

---

## 📂 Arquivos Utilizados

Foram utilizados os seguintes arquivos `.csv` da base original:

- `olist_orders_dataset.csv` — Informações dos pedidos
- `olist_order_items_dataset.csv` — Itens por pedido
- `olist_products_dataset.csv` — Atributos dos produtos
- `olist_customers_dataset.csv` — Localização dos clientes

---

## 🔗 Estratégia de Junção

As tabelas foram unificadas utilizando as seguintes chaves:

- `order_id` entre `orders`, `order_items`
- `product_id` entre `order_items` e `products`
- `customer_id` entre `orders` e `customers`
- 
---

## 🧹 Tratamentos Aplicados

Durante o processo de transformação:

- Foram **removidas linhas com valores nulos essenciais**, como `product_category_name`, para garantir a qualidade do modelo.
- Foi feita a **conversão do campo `order_purchase_timestamp` para datetime**, utilizando `pandas.to_datetime`.
- A base resultante foi salva como `historico_compras_clientes.csv`, com uma linha por produto comprado, associando atributos do cliente, produto e pedido.

---

## 🧠 Objetivo da Modelagem

O objetivo final é criar um modelo de **recomendação de produtos** com base no histórico de compras dos usuários. Esta base unificada servirá como ponto de partida para feature engineering, treino e avaliação de modelos no Vertex AI.

---

## 📌 Observações

- As informações de clientes, pedidos e produtos foram anonimizadas.
- A granularidade da base final é **pedido-produto**.
- Os textos de avaliação foram desconsiderados nesta etapa inicial, mas podem ser explorados futuramente como **features de NLP**.

---

*Última atualização: junho de 2025.*
