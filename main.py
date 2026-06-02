import os
import sys
import json
import logging
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process

load_dotenv()

logger = logging.getLogger("ai_pipeline")
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def ler_config_llm(caminho_arquivo: str = "llm_config.json") -> tuple[str, str]:
    """Lê o JSON genérico e retorna o modelo e a variável de ambiente da API Key."""
    if not os.path.exists(caminho_arquivo):
        logger.error(f"Arquivo de configuração LLM não encontrado: {caminho_arquivo}")
        raise SystemExit(1)
    
    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        config = json.load(f)

    modelo = config.get("model")
    env_var = config.get("api_key_env_var")
    
    if not modelo or not env_var:
         logger.error("O arquivo JSON deve conter as chaves 'model' e 'api_key_env_var'.")
         raise SystemExit(1)
         
    return modelo, env_var

def ler_personas_do_md(caminho_arquivo: str) -> dict:
    if not os.path.exists(caminho_arquivo):
        logger.error(f"Arquivo de personas não encontrado: {caminho_arquivo}")
        raise SystemExit(1)

    # Mapeia o cabeçalho do Markdown para a chave interna usada no pipeline.
    # O Agente 6 é o Avaliador (Evaluator). Cabeçalhos de agentes não mapeados
    # (ex.: 4 e 5) encerram o bloco anterior sem poluir o backstory do agente
    # imediatamente acima.
    header_map = {
        "## Agent 1": "extractor",
        "## Agent 2": "critic",
        "## Agent 3": "refactorer",
        "## Agent 6": "evaluator",
    }

    agents_data = {}
    current_agent = None
    current_field = None

    with open(caminho_arquivo, "r", encoding="utf-8") as file:
        for line in file:
            clean_line = line.strip()
            
            if not clean_line:
                continue

            # Qualquer cabeçalho de agente fecha o bloco anterior.
            if clean_line.startswith("## Agent"):
                current_agent = next(
                    (
                        chave
                        for prefixo, chave in header_map.items()
                        if clean_line.startswith(prefixo)
                    ),
                    None,
                )
                if current_agent:
                    agents_data[current_agent] = {
                        "role": "",
                        "goal": "",
                        "backstory": "",
                    }
                current_field = None
                continue

            if not current_agent:
                continue

            if clean_line.startswith("**Role:**"):
                agents_data[current_agent]["role"] = clean_line.replace(
                    "**Role:**", ""
                ).strip()
                current_field = None
            elif clean_line.startswith("**Goal:**"):
                agents_data[current_agent]["goal"] = clean_line.replace(
                    "**Goal:**", ""
                ).strip()
                current_field = None
            elif clean_line.startswith("**Backstory:**"):
                agents_data[current_agent]["backstory"] = clean_line.replace(
                    "**Backstory:**", ""
                ).strip()
                current_field = "backstory"
            elif current_field == "backstory":
                agents_data[current_agent]["backstory"] += "\n" + clean_line

    return agents_data

def run_crewai_pipeline() -> None:
    # Carrega as configurações dinâmicas da LLM
    modelo_llm, env_var_necessaria = ler_config_llm()
    
    # Valida se a chave correspondente existe no ambiente (.env)
    api_key = os.getenv(env_var_necessaria)
    if not api_key:
        logger.error(
            f"A variável '{env_var_necessaria}' não foi encontrada no .env. Configure suas credenciais."
        )
        raise SystemExit(1)

    logger.info(f"Iniciando pipeline utilizando a LLM: {modelo_llm}")

    caminho_agents_md = "agents.md"
    personas = ler_personas_do_md(caminho_agents_md)

    # Garante que a persona do Avaliador (Agente 6) foi carregada.
    if "evaluator" not in personas:
        logger.error("Persona do Avaliador (## Agent 6) não encontrada em agents.md.")
        raise SystemExit(1)

    transcript_path = r"transcript.txt"
    
    if not os.path.exists(transcript_path):
        logger.error(f"Arquivo de entrada não encontrado no caminho: {transcript_path}")
        raise SystemExit(1)

    with open(transcript_path, "r", encoding="utf-8") as f:
        input_text = f.read()

    # ==========================================
    # 1. Criação dos Agentes
    # ==========================================
    extractor_agent = Agent(
        role=personas["extractor"]["role"],
        goal=personas["extractor"]["goal"],
        backstory=personas["extractor"]["backstory"],
        llm=modelo_llm,
        verbose=True,
        allow_delegation=False,
    )

    critic_agent = Agent(
        role=personas["critic"]["role"],
        goal=personas["critic"]["goal"],
        backstory=personas["critic"]["backstory"],
        llm=modelo_llm,
        verbose=True,
        allow_delegation=False,
    )

    refactorer_agent = Agent(
        role=personas["refactorer"]["role"],
        goal=personas["refactorer"]["goal"],
        backstory=personas["refactorer"]["backstory"],
        llm=modelo_llm,
        verbose=True,
        allow_delegation=False,
    )

    evaluator_agent = Agent(
        role=personas["evaluator"]["role"],
        goal=personas["evaluator"]["goal"],
        backstory=personas["evaluator"]["backstory"],
        llm=modelo_llm,
        verbose=True,
        allow_delegation=False,
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
        output_file="output/1_user_stories_completas.md",
    )

    crew_extractor = Crew(
        agents=[extractor_agent], tasks=[task_extract_all], verbose=True
    )

    logger.info("Fase 1: Iniciando Agente Extrator e verificação de Guardrails...")
    resultado_extracao = crew_extractor.kickoff()

    # CHECK DE GUARDRAIL
    saida_bruta = str(resultado_extracao).strip()
    if (
        "Eu não sou capaz de criar um documento de requisitos a partir desta entrada"
        in saida_bruta
    ):
        logger.warning(
            "\n[GUARDRAIL ATIVADO]: A entrada não possui escopo de software ou tecnologia."
        )
        logger.warning(
            "Execução finalizada precocemente. Agentes Crítico, Refatorador e Avaliador NÃO foram acionados.\n"
        )
        return

    logger.info(
        "Guardrail aprovado: A entrada é válida. Prosseguindo para QA, Refatoração e Avaliação..."
    )

    # ==========================================
    # 3. FASE 2: Tarefas de Crítica, Refatoração e Avaliação
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
        output_file="output/2_relatorio_critica.md",
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
        output_file="output/3_user_stories_finais.md",
    )

    # FASE 2.1: Avaliação (Agente 6) — recebe o documento original + as saídas
    # dos Agentes 1 (extração), 2 (crítica) e 3 (refatoração) via `context`.
    task_evaluate = Task(
        description=(
            "Você é o Agente Avaliador (Agente 6). Audite o documento técnico final produzido pelo "
            "Refactorer (Agente 3) e produza o relatório JSON definido na sua persona, aplicando "
            "rigorosamente as fórmulas, pesos e regras de gating.\n\n"
            "Você recebe QUATRO entradas:\n"
            "ENTRADA 1 — DOCUMENTO ORIGINAL DE REQUISITOS (FONTE PRIMÁRIA DE VERDADE / único árbitro):\n"
            f"{input_text}\n\n"
            "ENTRADA 2 — USER STORIES DO AGENTE 1 (Extractor): disponível no contexto (saída da tarefa de extração).\n"
            "ENTRADA 3 — RELATÓRIO DO QA DO AGENTE 2 (Critic): disponível no contexto (saída da tarefa de crítica).\n"
            "ENTRADA 4 — DOCUMENTO FINAL DO AGENTE 3 (Refactorer): disponível no contexto (saída da tarefa de refatoração).\n\n"
            "Sua resposta deve ser EXCLUSIVAMENTE o relatório JSON válido, em português do Brasil, "
            "sem nenhum texto, preâmbulo ou comentário fora do JSON."
        ),
        expected_output="Relatório de avaliação em JSON válido, conforme o schema definido na persona do Avaliador (Agente 6).",
        agent=evaluator_agent,
        context=[task_extract_all, task_critic, task_refactor],
        output_file="output/6_ava_user_stories_finais.json",
    )

    crew_qa = Crew(
        agents=[critic_agent, refactorer_agent, evaluator_agent],
        tasks=[task_critic, task_refactor, task_evaluate],
        process=Process.sequential,
        verbose=True,
    )

    logger.info("Fase 2: Iniciando o fluxo de QA, Arquitetura e Avaliação...")
    crew_qa.kickoff()
    logger.info(
        "Processo finalizado com sucesso! Verifique os arquivos gerados em output/."
    )


if __name__ == "__main__":
    run_crewai_pipeline()
