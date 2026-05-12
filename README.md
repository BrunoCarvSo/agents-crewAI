# Pipeline de Engenharia de Requisitos com IA (CrewAI + Gemini)

Este projeto implementa uma ferramenta de automação focada no refinamento ágil de requisitos. Através de um pipeline sequencial de **3 agentes de Inteligência Artificial** (orquestrados via CrewAI e alimentados pelo Google Gemini), o sistema processa transcrições brutas de reuniões (*briefings*) e entrega **User Stories auditadas e cenários BDD/TDD**, prontos para a esteira de desenvolvimento.

---

# 🏗️ Como Funciona o Pipeline

O processo é estritamente sequencial e simula um time de engenharia de requisitos:

## 1. Extractor (Agente 1)

Analisa a transcrição bruta e rascunha:

* User Stories
* Critérios de aceite
* Requisitos funcionais e não funcionais

---

## 2. Critic (Agente 2)

Atua como QA da especificação:

* Audita a saída do Extractor contra o texto original
* Aplica notas de qualidade (0–10)
* Categoriza problemas encontrados

### Categorias de Correção

* `[Descartar alucinação]`
* `[Melhorar clareza]`
* `[Adicionar feature]`

---

## 3. Refactorer (Agente 3)

Consome:

* As stories brutas
* O relatório do QA

E gera:

* Documento final consolidado
* Stories refinadas
* Cenários BDD/TDD consistentes
* Artefato pronto para backlog técnico

---

# 📁 Estrutura do Repositório

A estrutura esperada do projeto é:

```text
├── Agents/
│   └── transcript.txt       # Texto bruto/transcrição da reunião (entrada do pipeline)
│
├── .env                     # Variáveis de ambiente (criado pelo usuário)
├── .env.example             # Template das variáveis de ambiente
├── agents.md                # Personas e prompts dos agentes
├── main.py                  # Orquestrador principal do CrewAI
└── requirements.txt         # Dependências Python
```

---

# 🛠️ 1. Instalação e Preparação do Ambiente

Para evitar conflitos de dependências e problemas como `ModuleNotFoundError`, o uso de um ambiente virtual (`venv`) é obrigatório.

---

## 1.1 Criar o Ambiente Virtual

Abra o terminal na raiz do projeto:

```bash
python -m venv .venv
```

---

## 1.2 Ativar o Ambiente Virtual

### Git Bash / MINGW64 (Recomendado)

```bash
source .venv/Scripts/activate
```

### Windows PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Após ativar, o terminal exibirá:

```text
(.venv)
```

---

## 1.3 Instalar as Dependências

### Instalação direta

```bash
pip install crewai python-dotenv
```

### Ou utilizando requirements.txt

```bash
pip install -r requirements.txt
```

---

# ⚙️ 2. Configurações Necessárias

Antes da execução, configure:

* API Key
* Personas dos agentes
* Arquivo de entrada

---

## 2.1 Configurando a API Key (`.env`)

O projeto utiliza `python-dotenv` para carregar variáveis de ambiente de forma segura.

### Copie o arquivo de exemplo

```bash
cp .env.example .env
```

### Configure sua chave da API do Google Gemini

```env
GOOGLE_API_KEY="sua_chave_api_aqui"
```

---

## 2.2 Configurando as Personas (`agents.md`)

O arquivo `agents.md` é carregado dinamicamente pelo `main.py`.

A estrutura deve seguir rigorosamente este formato:

```markdown
## Agent 1
**Role:** Analista de Requisitos Sênior
**Goal:** Extrair requisitos funcionais e não funcionais do texto...
**Backstory:** Você possui 10 anos de experiência...

## Agent 2
**Role:** Auditor de Qualidade Ágil (QA)
**Goal:** Revisar as User Stories...
**Backstory:** Especialista em validação e alucinações de IA...

## Agent 3
**Role:** Engenheiro de Software Refatorador
**Goal:** Aplicar as correções sugeridas pelo QA...
**Backstory:** Especialista em clean code e arquitetura...
```

---

## 2.3 Configurando a Entrada (`Agents/transcript.txt`)

Crie a pasta `Agents/` na raiz do projeto e adicione:

```text
Agents/transcript.txt
```

Dentro desse arquivo, cole:

* Transcrição da reunião
* Briefing do cliente
* Conversa de levantamento de requisitos
* Texto bruto relacionado ao sistema

---

# 🚀 3. Como Executar o Pipeline

Com:

* `.venv` ativado
* Dependências instaladas
* `.env` configurado
* `transcript.txt` preenchido

Execute:

```bash
python main.py
```

---

## Fluxo Esperado

Durante a execução, o terminal exibirá logs detalhados:

* Inicialização dos agentes
* Execução das Tasks
* Auditoria de qualidade
* Refatoração das User Stories
* Geração dos artefatos finais

---

# 📊 4. Saídas Geradas

Ao final da execução, o pipeline produzirá três arquivos Markdown na raiz do projeto:

---

## 📄 1_user_stories_brutas.md

Primeira extração gerada pelo Agente 1.

Contém:

* User Stories iniciais
* Critérios de aceite
* Requisitos extraídos diretamente da transcrição

---

## 📄 2_relatorio_critica.md

Relatório produzido pelo Agente 2.

Contém:

* Notas de qualidade
* Inconsistências detectadas
* Possíveis alucinações
* Sugestões de melhoria

---

## 📄 3_user_stories_finais.md

Artefato final consolidado pelo Agente 3.

Contém:

* Stories refinadas
* Cenários BDD/TDD
* Requisitos padronizados
* Documento pronto para backlog técnico

---

# 🧠 Tecnologias Utilizadas

| Tecnologia    | Finalidade                             |
| ------------- | -------------------------------------- |
| Python        | Linguagem principal                    |
| CrewAI        | Orquestração multiagente               |
| Google Gemini | Processamento de linguagem natural     |
| python-dotenv | Gerenciamento de variáveis de ambiente |
| Markdown      | Persistência dos artefatos gerados     |

---

# 🎯 Objetivo do Projeto

O objetivo é automatizar parte do processo de Engenharia de Requisitos, reduzindo:

* Ambiguidade
* Alucinações de IA
* Falhas de interpretação
* Retrabalho técnico

Ao mesmo tempo em que:

* Padroniza User Stories
* Melhora rastreabilidade
* Aumenta a qualidade dos requisitos
* Acelera a geração de backlog técnico para times ágeis
