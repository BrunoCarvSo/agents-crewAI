# Documentação de Requisitos: Educational Trail Builder

Este documento consolida as especificações técnicas, regras de negócio e requisitos funcionais extraídos da transcrição do sistema Educational Trail Builder.

---

## 1. Módulos do Sistema
*   **Trail Creation:** Interface para definição de módulos, estruturação de passos e publicação.
*   **Navigation:** Controle de fluxo pedagógico e marcação de progresso do aluno.
*   **Progress Tracking:** Monitoramento em tempo real, métricas e geração de contratos de progresso.

---

## 2. User Stories e Especificações BDD

### US01: Criação e Gestão de Trilhas
**Como** educador, **quero** criar trilhas de aprendizagem, **para** estruturar o ensino de conceitos de computação.

*   **RF01:** O sistema deve permitir a criação de trilhas com um identificador alfanumérico único.
*   **RF02:** Trilhas devem ser categorizadas com pelo menos uma tag educacional no momento da criação.
*   **RF03:** O sistema deve calcular o tempo total estimado da trilha somando os tempos individuais de cada passo.
*   **RN01:** Não é permitido publicar trilhas com 0 módulos.
*   **RN02:** Não é permitido ter duas trilhas publicadas com o mesmo título (unicidade de domínio).

**Cenários (BDD):**
*   **Cenário:** Publicação de trilha vazia
    *   **Dado** que a trilha possui 0 módulos
    *   **Quando** o educador tentar publicar a trilha
    *   **Então** o sistema deve retornar erro com "ErrorCode" e "ErrorMessage"

### US02: Estruturação Pedagógica
**Como** sistema, **quero** impor limites estruturais, **para** garantir a qualidade do aprendizado.

*   **RF04:** Cada módulo deve ter no máximo 10 passos sequenciais.
*   **RN03:** Proibir a exclusão de um módulo se houver pelo menos um aluno inscrito na trilha.

**Cenários (BDD):**
*   **Cenário:** Adição de 11º passo em um módulo
    *   **Dado** que o módulo já possui 10 passos
    *   **Quando** o educador tentar adicionar um novo passo
    *   **Então** o sistema deve retornar o contrato de erro padrão.

### US03: Navegação e Progressão do Aluno
**Como** aluno, **quero** navegar pelos passos de forma ordenada, **para** garantir a aquisição correta do conhecimento.

*   **RF05:** O acesso ao passo N é condicionado à conclusão do passo N-1.
*   **RF06:** Ao concluir um passo, o sistema deve recalcular automaticamente a porcentagem de progresso da trilha.
*   **RN04:** Limite de 3 trilhas ativas simultâneas por aluno.

**Cenários (BDD):**
*   **Cenário:** Pular passo bloqueado
    *   **Dado** que o passo anterior não foi concluído
    *   **Quando** o aluno tentar acessar o passo atual
    *   **Então** o sistema deve negar o acesso.

### US04: Monitoramento e Relatórios
**Como** educador, **quero** visualizar o progresso dos alunos, **para** intervir quando necessário.

*   **RF07:** O sistema deve gerar relatórios de progresso em formato JSON sob demanda.
*   **RN05:** Inatividade de 30 dias em uma trilha altera o status de "Active" para "Suspended".

**Cenários (BDD):**
*   **Cenário:** Suspensão por inatividade
    *   **Dado** que o aluno não concluiu nenhum passo há 30 dias
    *   **Quando** o sistema processar a verificação diária
    *   **Então** o status do aluno na trilha deve ser alterado para "Suspended".

### US05: Segurança e Administração
**Como** administrador, **quero** gerenciar o acesso e o ciclo de vida das trilhas.

*   **RF08:** Bloqueio de conta após 3 tentativas de login falhas.
*   **RF09:** Soft-delete de trilhas publicadas (invisível para novas matrículas, visível para alunos ativos).

---

## 3. Requisitos Não-Funcionais (Arquitetura)

*   **RNF01 (Persistência):** Todos os dados devem residir exclusivamente em um Repositório In-Memory volátil durante a sessão. Proibida a conexão com bancos de dados externos (ex: PostgreSQL).
*   **RNF02 (Padronização de Erro):** Qualquer violação de regra de negócio deve disparar uma resposta contendo estritamente:
    ```json
    {
      "ErrorCode": "string",
      "ErrorMessage": "string"
    }
    ```
*   **RNF03 (Contrato de Saída):** Relatórios de progresso devem seguir estritamente a especificação de contrato JSON definida pelo sistema de monitoramento.

---

## 4. Matriz de Rastreabilidade (Resumo de Regras Críticas)

| ID | Regra / Requisito | Ação em caso de violação |
| :--- | :--- | :--- |
| RN01 | Publicação com 0 módulos | Retornar contrato de erro |
| RN02 | Títulos duplicados | Retornar contrato de erro |
| RN03 | Exclusão de módulo (aluno ativo) | Retornar contrato de erro |
| RN04 | Max 3 trilhas ativas | Bloquear matrícula |
| RN05 | 30 dias inativo | Alterar status para "Suspended" |
| RNF01 | Persistência externa | Bloqueado por arquitetura |
| RNF02 | Erro 11º passo | Retornar contrato de erro |