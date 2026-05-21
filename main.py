import os
import sys
import logging
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process

load_dotenv()

logger = logging.getLogger("ai_pipeline")
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def ler_personas_do_md(caminho_arquivo: str) -> dict:
    if not os.path.exists(caminho_arquivo):
        logger.error(f"Arquivo de personas não encontrado: {caminho_arquivo}")
        raise SystemExit(1)

    agents_data = {}
    current_agent = None
    current_field = None

    with open(caminho_arquivo, "r", encoding="utf-8") as file:
        for line in file:
            clean_line = line.strip()
            
            if not clean_line:
                continue

            if clean_line.startswith("## Agent 1"):
                current_agent = "extractor"
                agents_data[current_agent] = {"role": "", "goal": "", "backstory": ""}
                current_field = None
            elif clean_line.startswith("## Agent 2"):
                current_agent = "critic"
                agents_data[current_agent] = {"role": "", "goal": "", "backstory": ""}
                current_field = None
            elif clean_line.startswith("## Agent 3"):
                current_agent = "refactorer"
                agents_data[current_agent] = {"role": "", "goal": "", "backstory": ""}
                current_field = None
            
            elif current_agent and clean_line.startswith("**Role:**"):
                agents_data[current_agent]["role"] = clean_line.replace("**Role:**", "").strip()
                current_field = None
            elif current_agent and clean_line.startswith("**Goal:**"):
                agents_data[current_agent]["goal"] = clean_line.replace("**Goal:**", "").strip()
                current_field = None
            elif current_agent and clean_line.startswith("**Backstory:**"):
                agents_data[current_agent]["backstory"] = clean_line.replace("**Backstory:**", "").strip()
                current_field = "backstory"
                
            elif current_agent and current_field == "backstory" and not clean_line.startswith("##"):
                agents_data[current_agent]["backstory"] += "\n" + clean_line

    return agents_data

def run_crewai_pipeline() -> None:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        logger.error("GOOGLE_API_KEY is not set in the environment; see .env.example")
        raise SystemExit(1)

    caminho_agents_md = "agents.md"
    personas = ler_personas_do_md(caminho_agents_md)
    transcript_path = r"transcript.txt"
    
    if not os.path.exists(transcript_path):
        logger.error(f"Arquivo de entrada não encontrado no caminho: {transcript_path}")
        raise SystemExit(1)

    with open(transcript_path, "r", encoding="utf-8") as f:
        input_text = f.read()

    modelo_llm = "gemini/gemini-3.1-flash-lite"

    # ==========================================
    # 1. Criação dos Agentes
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
    # 2. FASE 1: Tarefa de Extração e Guardrail
    # ==========================================
    task_extract_all = Task(
        description=(
            f"Leia o texto bruto abaixo e extraia TODAS as regras de negócio, requisitos funcionais "
            f"e não-funcionais (sistemas, arquitetura, restrições).\n\n"
            f"Texto original:\n{input_text}\n\n"
            f"ESTRATÉGIA OBRIGATÓRIA (Evite perder dados):\n"
            f"1. Mapeie mentalmente todas as seções e listas do documento.\n"
            f"2. Para cada bloco lógico identificado, extraia minuciosamente os requisitos.\n"
            f"3. Se houver listas numeradas ou com letras, você DEVE converter CADA item.\n"
        ),
        expected_output="Documento Markdown detalhado contendo todos os requisitos e cenários BDD acoplados, ou mensagem de aborto de Guardrail.",
        agent=extractor_agent,
        output_file="1_user_stories_completas.md"
    )

    crew_extractor = Crew(
        agents=[extractor_agent],
        tasks=[task_extract_all],
        verbose=True
    )

    logger.info("Fase 1: Iniciando Agente Extrator e verificação de Guardrails...")
    resultado_extracao = crew_extractor.kickoff()

    # CHECK DE GUARDRAIL - Interrompe se o texto for inválido (ex: Receita de bolo)
    saida_bruta = str(resultado_extracao).strip()
    if "Eu não sou capaz de criar um documento de requisitos a partir desta entrada" in saida_bruta:
        logger.warning("\n[GUARDRAIL ATIVADO]: A entrada não possui escopo de software ou tecnologia.")
        logger.warning("Execução finalizada precocemente. Agentes Crítico e Refatorador NÃO foram acionados.\n")
        return # Para a execução do pipeline aqui mesmo

    logger.info("Guardrail aprovado: A entrada é válida. Prosseguindo para QA e Refatoração...")

    # ==========================================
    # 3. FASE 2: Tarefas de Crítica e Refatoração
    # ==========================================
    task_critic = Task(
        description=(
            f"Audite o documento gerado pela tarefa anterior, comparando-o estritamente com o Texto original abaixo:\n\n"
            f"Texto original:\n{input_text}\n\n"
            f"Aplique as regras de cardinalidade e avalie de 0 a 5. Se a nota for menor que 3, use as tags OBRIGATÓRIAS."
        ),
        expected_output="Relatório de auditoria estruturado indicando notas e apontamentos de correção.",
        agent=critic_agent,
        context=[task_extract_all],
        output_file="2_relatorio_critica.md"
    )

    task_refactor = Task(
        description=(
            "Reescreva o documento de requisitos aplicando rigorosamente as diretrizes do relatório da crítica.\n"
            "Mantenha uma separação lógica entre Requisitos Funcionais e Requisitos Técnicos.\n\n"
            "FONTE PRIMÁRIA DE VERDADE — use o documento original abaixo para validar as sugestões do QA:\n\n"
            f"Documento original:\n{input_text}\n\n"
            "IMPORTANTE: Entregue APENAS o código/texto Markdown final. Nenhuma palavra de saudação."
        ),
        expected_output="Documento final de requisitos em Markdown, com 100% de cenários BDD acoplados.",
        agent=refactorer_agent,
        context=[task_extract_all, task_critic],
        output_file="3_user_stories_finais.md"
    )

    crew_qa = Crew(
        agents=[critic_agent, refactorer_agent],
        tasks=[task_critic, task_refactor],
        process=Process.sequential,
        verbose=True
    )
    
    logger.info("Fase 2: Iniciando o fluxo de QA e Arquitetura...")
    crew_qa.kickoff()
    logger.info("Processo finalizado com sucesso! Verifique os arquivos Markdown gerados.")

if __name__ == "__main__":
    run_crewai_pipeline()