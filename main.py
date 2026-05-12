"""
main.py

Implementação baseada em CrewAI de um pipeline sequencial de 3 agentes.
Este código utiliza a API do Google Gemini (gemini-3.1-flash-lite) 
para extrair, auditar e refatorar User Stories a partir de texto bruto.
As personas dos agentes são carregadas dinamicamente do arquivo agents.md.
"""

import os
import logging
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process

load_dotenv()

logger = logging.getLogger("ai_pipeline")
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def ler_personas_do_md(caminho_arquivo: str) -> dict:
    """
    Lê o arquivo agents.md e extrai o Role, Goal e Backstory de cada agente.
    """
    if not os.path.exists(caminho_arquivo):
        logger.error(f"Arquivo de personas não encontrado: {caminho_arquivo}")
        raise SystemExit(1)

    agents_data = {}
    current_agent = None

    with open(caminho_arquivo, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            # Identifica qual agente estamos lendo
            if line.startswith("## Agent 1"):
                current_agent = "extractor"
                agents_data[current_agent] = {}
            elif line.startswith("## Agent 2"):
                current_agent = "critic"
                agents_data[current_agent] = {}
            elif line.startswith("## Agent 3"):
                current_agent = "refactorer"
                agents_data[current_agent] = {}
            
            # Extrai os dados se já estivermos dentro do bloco de um agente
            elif current_agent and line.startswith("**Role:**"):
                agents_data[current_agent]["role"] = line.replace("**Role:**", "").strip()
            elif current_agent and line.startswith("**Goal:**"):
                agents_data[current_agent]["goal"] = line.replace("**Goal:**", "").strip()
            elif current_agent and line.startswith("**Backstory:**"):
                agents_data[current_agent]["backstory"] = line.replace("**Backstory:**", "").strip()

    return agents_data


def run_crewai_pipeline() -> None:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        logger.error("GOOGLE_API_KEY is not set in the environment; see .env.example")
        raise SystemExit(1)

    # Carrega as configurações dos agentes do arquivo Markdown
    caminho_agents_md = "agents.md"
    personas = ler_personas_do_md(caminho_agents_md)

    # Caminho fixo para o arquivo de transcrição utilizado pelo Extractor e Critic
    transcript_path = r"transcript.txt"
    
    if not os.path.exists(transcript_path):
        logger.error(f"Arquivo de entrada não encontrado no caminho: {transcript_path}")
        raise SystemExit(1)

    with open(transcript_path, "r", encoding="utf-8") as f:
        input_text = f.read()

    modelo_llm = "gemini/gemini-3.1-flash-lite"

    # ==========================================
    # 1. Criação dos Agentes dinamicamente
    # ==========================================
    extractor_agent = Agent(
        role=personas["extractor"]["role"],
        goal=personas["extractor"]["goal"],
        backstory=personas["extractor"]["backstory"],
        llm=modelo_llm,
        verbose=True,
        allow_delegation=False
    )

    critic_agent = Agent(
        role=personas["critic"]["role"],
        goal=personas["critic"]["goal"],
        backstory=personas["critic"]["backstory"],
        llm=modelo_llm,
        verbose=True,
        allow_delegation=False
    )

    refactorer_agent = Agent(
        role=personas["refactorer"]["role"],
        goal=personas["refactorer"]["goal"],
        backstory=personas["refactorer"]["backstory"],
        llm=modelo_llm,
        verbose=True,
        allow_delegation=False
    )

    # ==========================================
    # 2. Criação das Tasks
    # ==========================================
    task1 = Task(
        description=(
            f"Leia o texto bruto abaixo e gere as User Stories e cenários TDD.\n\n"
            f"Texto original:\n{input_text}\n\n"
            f"IMPORTANTE: Entregue APENAS o código/texto Markdown. Nenhuma palavra de saudação."
        ),
        expected_output="Documento puro em Markdown contendo exclusivamente User Stories e cenários.",
        agent=extractor_agent,
        output_file="1_user_stories_brutas.md"
    )

    task2 = Task(
        description=(
            f"Audite a saída gerada pela Task 1 comparando-a estritamente com o Texto original abaixo:\n\n"
            f"Texto original:\n{input_text}\n\n"
            f"Para CADA User Story ou Cenário, atribua uma nota de 0 a 10. "
            f"Se a nota for menor que 7, escreva uma instrução clara para o próximo agente usando as categorias OBRIGATÓRIAS: "
            f"[Descartar alucinação], [Melhorar clareza], ou [Adicionar feature]."
        ),
        expected_output="Relatório de auditoria estruturado indicando notas e apontamentos de correção categorizados.",
        agent=critic_agent,
        output_file="2_relatorio_critica.md"
    )

    task3 = Task(
        description=(
            "Reescreva o documento inicial da Task 1 aplicando rigorosamente as diretrizes categorizadas do relatório da Task 2. "
            "Entregue o documento final de requisitos.\n"
            "IMPORTANTE: Entregue APENAS o código/texto Markdown final. Nenhuma palavra de saudação."
        ),
        expected_output="Documento final de requisitos em Markdown, puramente técnico e livre de falas paralelas.",
        agent=refactorer_agent,
        context=[task1, task2],
        output_file="3_user_stories_finais.md"
    )

    # ==========================================
    # 3. Configuração e Execução do Crew
    # ==========================================
    crew = Crew(
        agents=[extractor_agent, critic_agent, refactorer_agent],
        tasks=[task1, task2, task3],
        process=Process.sequential,
        verbose=True
    )
    
    logger.info("Iniciando o pipeline do CrewAI...")
    crew.kickoff()
    logger.info("Processo finalizado com sucesso! Verifique os arquivos Markdown gerados.")

if __name__ == "__main__":
    run_crewai_pipeline()