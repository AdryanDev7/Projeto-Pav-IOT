# 🌐 Projeto PAV - Sistema de Análise de Dados de Sensores IoT

Trabalho prático académico desenvolvido para a disciplina de Programação de Aplicações Visuais (PAV), focado na construção de uma API REST robusta em arquitetura em camadas para recolha, monitorização e análise de dados de sensores IoT.

---

## 🚀 Tecnologias Utilizadas
* **Linguagem:** Python 3.13.7
* **Framework Web:** Flask
* **Mapeamento Objeto-Relacional (ORM):** Flask-SQLAlchemy
* **Base de Dados Relacional:** PostgreSQL (rodando em contentor Docker, porta mapeada `5433:5432`)
* **Ferramenta de Base de Dados:** DBeaver
* **Testes de API:** Postman / Insomnia

---

## 📂 Arquitetura em Camadas
O projeto segue estritamente os princípios de separação de responsabilidades e camadas:
* **`config/`**: Configurações de conexão e inicialização da base de dados.
* **`entities/`**: Modelos de dados e mapeamento ORM das tabelas (`localizacoes`, `sensores`, `leituras_sensores`, `anomalias`).
* **`repositories/`**: Camada de persistência e interceção direta com a base de dados.
* **`services/`**: Camada de lógica de negócio e validações estruturais.
* **`controllers/`**: Camada de controlo para tratamento de requisições HTTP e formatação de respostas.
* **`routes/`**: Definição de Blueprints e mapeamento de *endpoints* da API.

---

## 📊 Modelo de Dados (4 Tabelas)
1. **`localizacoes`**: Armazena os setores, fábricas e coordenadas geográficas (latitude/longitude).
2. **`sensores`**: Regista os dispositivos IoT, códigos seriais, tipos e níveis de bateria.
3. **`leituras_sensores`**: Guarda o histórico temporal das medições efetuadas pelos sensores.
4. **`anomalias`**: Regista alertas e falhas críticas geradas automaticamente pelo sistema.

---

## 📋 Regras de Negócio Implementadas (10 RNs)

1. **RN01 - Validação de Coordenadas Geográficas:** A latitude deve estar entre $-90$ e $90$ e a longitude entre $-180$ e $180$.
2. **RN02 - Unicidade do Código Serial:** Cada sensor deve possuir um `codigo_serial` único no sistema.
3. **RN03 - Obrigatoriedade de Associação:** Nenhum sensor pode ser cadastrado sem uma localização pré-existente válida.
4. **RN04 - Validação do Nível de Bateria:** O nível de bateria deve obrigatoriamente situar-se entre $0$ e $100$.
5. **RN05 - Controlo de Status Operacional:** Gestão de estados do sensor (*Ativo*, *Inativo*, *Em Manutenção*).
6. **RN06 - Integridade de Referência nas Leituras:** O sensor associado a uma leitura deve existir obrigatoriamente.
7. **RN07 - Obrigatoriedade de Parâmetros de Medição:** O valor da leitura e o nível da bateria são de preenchimento obrigatório.
8. **RN08 - Deteção Automática de Anomalias Críticas:** Valores de leituras superiores a $90.0$ geram automaticamente um alerta na tabela de anomalias com severidade alta.
9. **RN09 - Rastreabilidade Temporal:** Carimbo automático de data e hora em todas as leituras recebidas (`data_hora`).
10. **RN10 - Consistência Relacional (Deleção Segura):** Validação de chaves estrangeiras para evitar registos órfãos na base de dados relacional.

---

## ⚙️ Como Executar o Projeto

1. **Subir o PostgreSQL via Docker:**
   ```bash
   docker-compose up -d

2. **Instalar as Dependências:**
   pip install flask flask-sqlalchemy psycopg2-binary

3. **Executar a Aplicação:**
   python app.py