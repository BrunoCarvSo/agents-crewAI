# Documento de Requisitos do Sistema - Gestão de Brechó

## 1. Requisitos Funcionais

**[REQ-001] - Cadastro Individual de Itens (Peça Única)**
* **Regra:** O sistema deve permitir o cadastro de peças individuais, atribuindo tamanho, estado de conservação e gerando um código de barras exclusivo por item.
* **Cenário BDD (Caminho Feliz):**
    * Dado que o operador acessou o módulo de cadastro
    * Quando inserir os dados da peça, informar o tamanho e o estado de conservação
    * Então o sistema deve salvar o item como único e gerar um código de barras exclusivo para impressão
* **Cenário BDD (Caminho Infeliz):**
    * Dado que o sistema já possui um código de barras registrado
    * Quando o operador tentar cadastrar um novo item com o mesmo código
    * Então o sistema deve bloquear o cadastro e exibir a mensagem: "Erro: Item duplicado. O código de barras já existe no inventário."

**[REQ-002] - Gestão de Consignação e Comissionamento**
* **Regra:** O sistema deve vincular a peça ao fornecedor (dono original) e calcular automaticamente a comissão (40% fornecedor / 60% brechó) no momento da venda.
* **Cenário BDD (Caminho Feliz):**
    * Dado que uma peça consignada foi vendida no caixa
    * Quando a transação for concluída
    * Então o sistema deve registrar o valor de venda, calcular a comissão de 40% para o fornecedor e 60% para o brechó, vinculando o valor ao perfil do fornecedor
* **Cenário BDD (Caminho Infeliz):**
    * Dado que o fornecedor está inativo no sistema
    * Quando a venda da peça consignada ocorrer
    * Então o sistema deve impedir o processamento e emitir alerta de inconsistência sobre o vínculo do fornecedor

**[REQ-003] - Pagamento com Crédito de Troca**
* **Regra:** O sistema deve aceitar "Crédito de Troca" como forma de pagamento no caixa, permitindo pagamentos combinados (split de pagamento).
* **Cenário BDD (Caminho Feliz):**
    * Dado que um cliente possui um saldo de crédito de troca no sistema
    * Quando o operador processar a venda e selecionar formas de pagamento
    * Então o sistema deve permitir abater o valor do crédito e solicitar o saldo restante em outra forma (ex: Pix)
* **Cenário BDD (Caminho Infeliz):**
    * Dado que o saldo do "Crédito de Troca" é inferior ao valor da compra
    * Quando o sistema processar a forma de pagamento
    * Então o sistema deve aplicar o saldo total disponível e solicitar obrigatoriamente o complemento do saldo via outro meio de pagamento

**[REQ-004] - Liquidação Automática de Estoque Parado**
* **Regra:** Peças cadastradas há mais de 45 dias devem receber automaticamente 20% de desconto no momento do checkout.
* **Cenário BDD (Análise de Valor Limite):**
    * Dado que uma peça foi cadastrada há exatamente 45 dias
    * Quando o operador bipar o código de barras no caixa
    * Então o sistema não deve aplicar o desconto de 20%
    * E quando o tempo decorrido for de 46 dias, o sistema deve aplicar 20% de desconto automaticamente

**[REQ-005] - Emissão de Comprovante Digital (WhatsApp/E-mail)**
* **Regra:** O sistema deve oferecer o envio do recibo via canais digitais (WhatsApp ou E-mail) ao finalizar a venda.
* **Cenário BDD:**
    * Dado que a venda foi finalizada
    * Quando o sistema solicitar a forma de envio do comprovante
    * Então o operador poderá selecionar WhatsApp ou E-mail para enviar o recibo ao cliente

**[REQ-006] - Consulta Inteligente de Estoque**
* **Regra:** O sistema deve permitir a busca rápida de itens por filtros (tipo, tamanho, cor) e indicar a localização física (arara/setor).
* **Cenário BDD (Caminho Feliz):**
    * Dado que o operador está no módulo de consulta
    * Quando o operador buscar por características (ex: vestido, preto, G)
    * Então o sistema deve exibir a disponibilidade do item e a sua localização física na loja
* **Cenário BDD (Caminho Infeliz):**
    * Dado que a busca não retorna itens com os filtros aplicados
    * Quando o operador realizar a pesquisa
    * Então o sistema deve informar claramente que não há produtos com aquele filtro, evitando erro de sistema

**[REQ-007] - Relatórios de Performance de Vendas**
* **Regra:** O sistema deve gerar relatórios que identifiquem categorias de maior saída e fornecedores com melhor performance de giro de estoque.
* **Cenário BDD:**
    * Dado que o gestor acessou o dashboard de relatórios
    * Quando solicitar os dados de performance mensal
    * Então o sistema deve exibir os itens mais vendidos e o ranking de fornecedores com base na velocidade de venda

**[REQ-008] - Rastreabilidade (Auditoria de Peça)**
* **Regra:** O sistema deve manter o histórico completo da peça (data de entrada, funcionário responsável, histórico de preços e data de venda).
* **Cenário BDD (Caminho Feliz):**
    * Dado que o operador busca pelo código de barras de uma peça
    * Quando solicitar o histórico completo ("capivara")
    * Então o sistema deve exibir a data de entrada, quem cadastrou, alterações de preço e a data efetiva da venda
* **Cenário BDD (Caminho Infeliz):**
    * Dado que o código de barras informado é inválido ou inexistente
    * Quando o operador solicitar a busca do histórico
    * Então o sistema deve retornar a mensagem: "Item não localizado no inventário"