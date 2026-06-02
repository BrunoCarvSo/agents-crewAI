**RELATÓRIO DE AUDITORIA DE QA - SISTEMA DE GESTÃO DE BRECHÓ**

**Status da Auditoria:** REPROVADO
**Nota Geral:** 2 (Insuficiente)

---

### 1. Contagem de Conformidade
*   **Total de Regras Mapeadas (RF):** 8
*   **Total de Cenários BDD:** 8
*   **Cobertura:** 1:1 (Atende à regra de cardinalidade básica, mas falha gravemente na qualidade técnica e nos cenários negativos obrigatórios).

### 2. Parecer de Auditoria
O documento apresenta uma cobertura estrutural completa (um cenário por regra), porém, **falha na qualidade técnica e na completude lógica**. Não foram previstos cenários negativos ou de exceção, o que é inaceitável para um sistema de gestão comercial e financeira. Sem testes de erro, o TDD é impossível.

### 3. Análise Individual por Requisito

| ID | Nota | Avaliação |
| :--- | :--- | :--- |
| REQ-001 | 3 | Atende ao básico, mas não prevê erro em cadastro de peça duplicada. |
| REQ-002 | 2 | Ausência de cenário de falha para comissionamento. |
| REQ-003 | 2 | Falta cenário negativo: Saldo insuficiente no crédito de troca. |
| REQ-004 | 3 | Funcional, mas falta cenário de peça com 44 dias (limite de borda). |
| REQ-005 | 3 | Aceitável. |
| REQ-006 | 2 | Falta cenário de busca sem resultados (feedback ao usuário). |
| REQ-007 | 3 | Aceitável. |
| REQ-008 | 2 | Falta cenário para item não encontrado no sistema. |

---

### 4. Plano de Ação (Ações Corretivas)

**[Adicionar feature]** - Necessária a inclusão de cenários negativos e de borda para garantir a robustez do sistema.

1.  **REQ-002:** Adicionar cenário: "Dado que o fornecedor está inativo, quando a venda ocorrer, então o sistema deve impedir o processamento e emitir alerta de inconsistência".
2.  **REQ-003:** Adicionar cenário: "Dado que o saldo do 'Crédito de Troca' é inferior ao valor da compra, quando o sistema processar, então deve aplicar o saldo total e solicitar o complemento via outro meio de pagamento".
3.  **REQ-004:** Adicionar teste de borda: "Dado que uma peça foi cadastrada há exatamente 45 dias, então o sistema deve validar se o desconto de 20% é aplicado corretamente (análise de limite)".
4.  **REQ-006:** Adicionar cenário: "Dado que a busca não retorna itens, então o sistema deve informar claramente que não há produtos com aquele filtro, evitando erro de sistema".
5.  **REQ-008:** Adicionar cenário: "Dado que o código de barras é inválido ou inexistente, então o sistema deve retornar a mensagem: 'Item não localizado no inventário'".

**Instruções para o próximo agente:** 
Refaça o artefato adicionando os fluxos alternativos (caminho infeliz). Nenhum requisito de negócio em sistemas financeiros (como o de consignação e créditos de troca) deve ser documentado apenas com o "caminho feliz". Utilize a técnica de partição de equivalência e análise de valor limite para os campos de data (45 dias) e valores (cálculo de 40/60).