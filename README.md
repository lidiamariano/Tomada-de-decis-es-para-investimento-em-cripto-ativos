# 📊 Sistema de Auxílio à Decisão para Investimento em Criptoativos

![Vídeo sem título ‐ Feito com o Clipchamp](https://github.com/user-attachments/assets/220c7f7a-ca72-42a5-8bba-91e0b7b5725d)

## 🔍 Descrição

Este repositório contém um projeto desenvolvido individualmente que visa construir um sistema de auxílio à tomada de decisões para investimento em criptoativos. O sistema analisa o histórico de preços e utiliza modelos de machine learning para indicar os melhores momentos de compra e venda. 

## ⚙️ Instruções de Execução

### ✅ Pré-requisitos

- Python 3.8 ou superior
- Docker e Docker Compose instalados

### 📥 Instalação

1. **Clonar o repositório:**

   ```bash
   https://github.com/lidiamariano/modelo_investimento_criptos_ativos.git
   ```

2. **Ir até a pasta que contém o docker-compose:**

   ```bash
   cd src
   ```

3. **Rodar o docker:**

   ```bash
   docker-compose up -d --build
   ```
   ou
   ```bash
   docker-compose up --build
   ```

### ▶️ Execução

1. **Swagger do Backend:**

   ```bash
   localhost:8080/docs
   ```


2. **Frontend:**

   ```bash
   localhost:5000
   ```
----------------------------------------------------------**Ponderada do Rafael🫨**---------------------------------------------------------
## Faria sentido utilizar um Data Lake para esse projeto?

1. **Variedade de Dados**: O mercado de criptoativos é influenciado por uma ampla gama de fatores, desde dados estruturados (preços, volumes de negociação) até dados não estruturados (notícias, sentimentos em redes sociais). Um data lake permite armazenar todos esses tipos de dados em um único repositório.

2. **Escalabilidade**: Criptoativos geram uma grande quantidade de dados em alta velocidade. Um data lake é capaz de lidar com grandes volumes de dados, facilitando o armazenamento histórico que pode ser útil para análises futuras e re-treinamento de modelos.

3. **Flexibilidade Analítica**: Cientistas de dados podem explorar e analisar os dados de diferentes maneiras sem a necessidade de estruturações prévias, o que é útil na fase de exploração e teste de modelos de machine learning.

4. **Integração de Dados**: Facilita a integração de dados provenientes de diversas fontes e em diferentes formatos, enriquecendo as análises e potencialmente melhorando a precisão dos modelos preditivos.

### **Considerações a Serem Feitas**

- **Complexidade e Custo**: Implementar e manter um data lake pode ser mais complexo e custoso em comparação com soluções mais simples, como bancos de dados relacionais.

- **Governança de Dados**: É crucial estabelecer políticas de governança para evitar que o data lake se transforme em um "data swamp", onde os dados são desorganizados e difíceis de encontrar.

- **Necessidade Real**: Se o projeto é de pequena escala ou foca em um ou dois criptoativos com dados bem estruturados, um banco de dados relacional como o PostgreSQL pode ser suficiente e mais prático.

### **Conclusão**

Para um projeto que:

- Envolve **grandes volumes de dados**;
- Necessita de **flexibilidade** para armazenar diferentes tipos de dados;
- Planeja **escalar** e incorporar mais fontes de dados no futuro;

Utilizar um **data lake** faz sentido e pode agregar valor significativo ao sistema de auxílio à decisão. No entanto, é importante pesar os benefícios contra os custos e a complexidade adicional. Se o escopo atual do projeto é mais limitado, uma solução baseada em bancos de dados relacionais pode ser mais adequada. Nesse sentido, para este projeto optou-se por não utilizar um Data Lake.
