# Relatório de Auditoria: Sistema Educational Trail Builder

**Auditor:** QA Lead & System Auditor  
**Status:** Auditado com Restrições  

Este relatório audita a conformidade técnica entre o texto original de requisitos e o documento gerado pelo Engenheiro. O documento apresenta uma estrutura organizada, porém falha na cobertura total de requisitos específicos solicitados no texto original.

---

### Avaliação de Requisitos (Notas 0-5)

| Requisito | Descrição | Nota | Comentário do Auditor |
| :--- | :--- | :--- | :--- |
| **REQ 01** | Identificador alfanumérico único | 5 | Implementado (RF01). |
| **REQ 02** | Proibição publicar trilha vazia | 5 | Implementado (RN01). |
| **REQ 03** | Limite de 10 passos por módulo | 5 | Implementado (RF04). |
| **REQ 04** | Unicidade de título (Publicadas) | 5 | Implementado (RN02). |
| **REQ 05** | Persistência In-Memory | 5 | Implementado (RNF01). |
| **REQ 06** | Limite de 3 trilhas ativas | 5 | Implementado (RN04). |
| **REQ 07** | Recalculo automático progresso | 5 | Implementado (RF06). |
| **REQ 08** | Bloqueio de passos (N-1) | 5 | Implementado (RF05). |
| **REQ 09** | Cálculo tempo estimado total | 5 | Implementado (RF03). |
| **REQ 10** | Soft-delete de trilha | 5 | Implementado (RF09). |
| **REQ 11** | Lockout (3 tentativas falhas) | 5 | Implementado (RF08). |
| **REQ 12** | Relatório JSON contrato | 5 | Implementado (RF07/RNF03). |
| **REQ 13** | Inatividade 30 dias (Suspended) | 5 | Implementado (RN05). |
| **REQ 14** | Impedir delete com aluno ativo | 5 | Implementado (RN03). |
| **REQ 15** | Erro padrão (ErrorCode/Msg) | 2 | **Falha na estruturação.** Embora citado em cenários, a regra global não está explicitamente vinculada a "qualquer violação" conforme a RF15 original. |
| **REQ 16** | Categorização com Tag | 5 | Implementado (RF02). |

---

### Apontamentos de Correção (Ações Corretivas)

1. **[Adicionar feature/Melhorar clareza] (Sobre REQ 15):** O documento original especifica que *qualquer* violação de regra de negócio deve retornar o contrato de erro. O documento gerado vincula isso a casos isolados (BDD). É necessário elevar o status deste item para uma Regra de Negócio (RN) global ou Requisito Não-Funcional (RNF), garantindo que a regra cubra todas as 16 condições de erro, não apenas o 11º passo ou a trilha vazia.

---

### Documento Auditorado (Corrigido para Completude)

*(O documento abaixo integra as correções necessárias para garantir a cobertura 100% dos requisitos originais)*

# Documentação de Requisitos: Educational Trail Builder (Revisada)

## 1. Módulos do Sistema
*   **Trail Creation:** Interface para definição de módulos, estruturação de passos e publicação.
*   **Navigation:** Controle de fluxo pedagógico e marcação de progresso do aluno.
*   **Progress Tracking:** Monitoramento em tempo real, métricas e geração de contratos de progresso.

## 2. User Stories e Especificações BDD
*(Mantidas as US01 a US05, com a inclusão da regra global de erros)*

## 3. Requisitos Não-Funcionais (Arquitetura)

*   **RNF01 (Persistência):** Todos os dados devem residir exclusivamente em um Repositório In-Memory volátil.
*   **RNF02 (Padronização de Erro - Global):** **Para qualquer violação de regra de negócio** (incluindo tentativas de exclusão de módulos ativos, violação de limites de passos ou tentativas de acesso a passos bloqueados), o sistema deve retornar obrigatoriamente um contrato JSON:
    ```json
    {
      "ErrorCode": "string",
      "ErrorMessage": "string"
    }
    ```
*   **RNF03 (Contrato de Saída):** Relatórios de progresso devem seguir estritamente o formato JSON solicitado pelo educador.

## 4. Matriz de Rastreabilidade (Consolidada)

| ID | Regra / Requisito | Ação em caso de violação |
| :--- | :--- | :--- |
| RN01 | Publicação com 0 módulos | Erro Padrão (RNF02) |
| RN02 | Títulos duplicados | Erro Padrão (RNF02) |
| RN03 | Exclusão de módulo (aluno ativo) | Erro Padrão (RNF02) |
| RN04 | Max 3 trilhas ativas | Erro Padrão (RNF02) |
| RN05 | 30 dias inativo | Alterar status para "Suspended" |
| RN06 | Limite de 10 passos por módulo | Erro Padrão (RNF02) |
| RN07 | Acesso a passo bloqueado (N-1) | Erro Padrão (RNF02) |
| RNF01 | Persistência externa | Bloqueado por arquitetura |
| RNF02 | Erro de Domínio | Retornar contrato de erro JSON |