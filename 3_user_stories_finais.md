# Documentação de Requisitos: Educational Trail Builder

Este documento consolida as especificações técnicas, regras de negócio e requisitos funcionais do sistema, estruturado para conformidade total com os critérios de aceite e auditoria de QA.

---

## 1. Módulos do Sistema
*   **Trail Creation:** Gestão de módulos, passos e publicação.
*   **Navigation:** Controle de fluxo, progressão e validação de bloqueios.
*   **Progress Tracking:** Monitoramento em tempo real e geração de relatórios.

---

## 2. Requisitos Funcionais (RF) e Regras de Negócio (RN)

### 2.1 Gestão de Trilhas e Pedagógica
*   **RF01:** Criação de trilhas com identificador alfanumérico único.
*   **RF02:** Obrigatoriedade de pelo menos uma tag educacional na criação.
*   **RF03:** Cálculo de tempo total (soma de tempos individuais dos passos).
*   **RF04:** Limite máximo de 10 passos por módulo.
*   **RN01:** Proibida publicação de trilhas com 0 módulos.
*   **RN02:** Unicidade de título obrigatória para trilhas publicadas.
*   **RN03:** Proibida exclusão de módulos se houver alunos inscritos.

### 2.2 Navegação e Progresso
*   **RF05:** Acesso ao passo N condicionado à conclusão do passo N-1.
*   **RF06:** Recálculo automático da porcentagem de progresso por passo concluído.
*   **RN04:** Limite de 3 trilhas ativas simultâneas por aluno.

### 2.3 Monitoramento e Administração
*   **RF07:** Geração de relatórios de progresso em formato JSON.
*   **RF08:** Bloqueio de conta após 3 tentativas de login falhas.
*   **RF09:** Soft-delete de trilhas publicadas.
*   **RN05:** Alteração de status para "Suspended" após 30 dias de inatividade.

---

## 3. Requisitos Não-Funcionais (RNF)

*   **RNF01 (Persistência):** Repositório In-Memory volátil (Proibido uso de bancos externos).
*   **RNF02 (Padronização Global de Erros):** **Qualquer** violação de Regra de Negócio deve retornar obrigatoriamente:
    ```json
    {
      "ErrorCode": "string",
      "ErrorMessage": "string"
    }
    ```
*   **RNF03 (Contrato de Saída):** Relatórios de progresso devem manter conformidade estrita com o contrato JSON definido.

---

## 4. Cenários BDD (Cobertura Total)

### US01: Criação e Gestão
*   **Cenário:** Publicação de trilha sem módulos
    *   **Dado** que a trilha está vazia
    *   **Quando** o educador solicitar a publicação
    *   **Então** o sistema deve retornar erro com código e mensagem padrão
*   **Cenário:** Criação de trilha com título já existente
    *   **Dado** que já existe uma trilha pública com o título "Java Básico"
    *   **Quando** o educador tentar publicar uma nova trilha com o título "Java Básico"
    *   **Então** o sistema deve retornar erro com código e mensagem padrão

### US02: Estruturação Pedagógica
*   **Cenário:** Exceder limite de passos em um módulo
    *   **Dado** que um módulo possui 10 passos
    *   **Quando** o educador tentar adicionar o 11º passo
    *   **Então** o sistema deve retornar erro com código e mensagem padrão
*   **Cenário:** Excluir módulo com aluno inscrito
    *   **Dado** que existe pelo menos um aluno inscrito na trilha
    *   **Quando** o educador tentar excluir um módulo da trilha
    *   **Então** o sistema deve retornar erro com código e mensagem padrão

### US03: Navegação e Progressão
*   **Cenário:** Acesso a passo bloqueado
    *   **Dado** que o aluno não concluiu o passo N-1
    *   **Quando** o aluno tentar acessar o passo N
    *   **Então** o sistema deve retornar erro com código e mensagem padrão
*   **Cenário:** Matrícula acima do limite permitido
    *   **Dado** que o aluno já possui 3 trilhas com status "Active"
    *   **Quando** o aluno tentar se inscrever em uma nova trilha
    *   **Então** o sistema deve retornar erro com código e mensagem padrão

### US04: Monitoramento e Relatórios
*   **Cenário:** Processamento de inatividade
    *   **Dado** que o status do aluno é "Active" e não há progresso há 30 dias
    *   **Quando** o job de verificação diária for executado
    *   **Então** o status do aluno na trilha deve ser atualizado para "Suspended"

### US05: Segurança
*   **Cenário:** Bloqueio por tentativas inválidas
    *   **Dado** que o usuário errou a senha 2 vezes
    *   **Quando** o usuário tentar logar novamente e falhar
    *   **Então** o sistema deve bloquear o acesso à conta e retornar erro padrão