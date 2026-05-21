import os
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

    with open(caminho_arquivo, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line.startswith("## Agent 1"):
                current_agent = "extractor"
                agents_data[current_agent] = {}
            elif line.startswith("## Agent 2"):
                current_agent = "critic"
                agents_data[current_agent] = {}
            elif line.startswith("## Agent 3"):
                current_agent = "refactorer"
                agents_data[current_agent] = {}
            elif current_agent and line.startswith("**Role:**"):
                agents_data[current_agent]["role"] = line.replace("**Role:**", "").strip()
            elif current_agent and line.startswith("**Goal:**"):
                agents_data[current_agent]["goal"] = line.replace("**Goal:**", "").strip()
            elif current_agent and line.startswith("**Backstory:**"):
                agents_data[current_agent]["backstory"] = line.replace("**Backstory:**", "").strip()

    # Adicionamos um papel genérico para o Planner, que pode ser o próprio Extractor assumindo outra postura, 
    # ou podemos instanciar com base na role do Extractor.
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
    # 2. Criação das Tasks: Abordagem Genérica de Chunking Funcional
    # ==========================================
    
    # Task 1: O Extractor agora é orientado a quebrar mentalmente o documento, 
    # independentemente de ele ter 10 módulos ou 50 itens de lista.
    task_extract_all = Task(
        description=(
            f"Leia o texto bruto abaixo e extraia TODAS as regras de negócio, requisitos funcionais "
            f"e não-funcionais (sistemas, arquitetura, restrições).\n\n"
            f"Texto original:\n{input_text}\n\n"
            f"ESTRATÉGIA OBRIGATÓRIA (Evite perder dados):\n"
            f"1. Mapeie mentalmente todas as seções e listas do documento.\n"
            f"2. Para cada bloco lógico identificado, extraia minuciosamente os requisitos.\n"
            f"3. Se houver listas numeradas ou com letras (ex: a, b, c), você DEVE converter CADA item "
            f"individualmente em um requisito técnico ou regra de negócio.\n"
            f"Gere o resultado em User Stories e cenários TDD/BDD utilizando puramente Markdown."
        ),
        expected_output="Documento Markdown detalhado contendo todos os requisitos e user stories, garantindo que listas longas não sejam resumidas.",
        agent=extractor_agent,
        output_file="1_user_stories_completas.md"
    )

    task_critic = Task(
        description=(
            f"Audite o documento gerado comparando-o estritamente com o Texto original abaixo:\n\n"
            f"Texto original:\n{input_text}\n\n"
            f"Para CADA User Story, Cenário ou Requisito Técnico, atribua uma nota de 0 a 5 conforme as regras da sua persona.\n"
            f"Se a nota for menor que 3, escreva uma instrução clara usando as categorias: "
            f"[Descartar alucinação], [Melhorar clareza], ou [Adicionar feature].\n"
            f"ATENÇÃO ESPECIAL: Verifique meticulosamente se ALGUM item de lista do texto original foi ignorado ou agrupado indevidamente no documento gerado. Se sim, use [Adicionar feature]."
        ),
        expected_output="Relatório de auditoria estruturado indicando notas e apontamentos de correção categorizados.",
        agent=critic_agent,
        context=[task_extract_all],
        output_file="2_relatorio_critica.md"
    )

    task_refactor = Task(
        description=(
            "Reescreva o documento de requisitos aplicando rigorosamente as diretrizes categorizadas do relatório da crítica.\n"
            "Mantenha uma separação lógica entre Requisitos Funcionais e Requisitos Não-Funcionais/Técnicos.\n\n"
            "FONTE PRIMÁRIA DE VERDADE — use este documento original para validar cada sugestão do QA "
            "antes de aplicá-la. Se uma sugestão do QA contradizer ou extrapolar o original, ignore-a:\n\n"
            f"Documento original:\n{input_text}\n\n"
            "IMPORTANTE: Entregue APENAS o código/texto Markdown final. Nenhuma palavra de saudação."
        ),
        expected_output="Documento final de requisitos em Markdown, puramente técnico e exaustivo.",
        agent=refactorer_agent,
        context=[task_extract_all, task_critic],
        output_file="3_user_stories_finais.md"
    )

    # ==========================================
    # 3. Configuração e Execução do Crew
    # ==========================================
    crew = Crew(
        agents=[extractor_agent, critic_agent, refactorer_agent],
        tasks=[task_extract_all, task_critic, task_refactor],
        process=Process.sequential,
        verbose=True
    )
    
    logger.info("Iniciando o pipeline do CrewAI com estratégia genérica...")
    crew.kickoff()
    logger.info("Processo finalizado com sucesso! Verifique os arquivos Markdown gerados.")

if __name__ == "__main__":
    run_crewai_pipeline()