### Requisitos Funcionais

**[REQ-001] - Cadastro Individual de Peças Únicas**
* **Regra:** Cada item deve ser registrado individualmente com atributos específicos (tamanho, estado de conservação) e possuir um código de barras exclusivo gerado pelo sistema.
* **Cenário BDD (Positivo):**
    * Dado que o operador acessa a tela de cadastro de estoque
    * Quando insere os dados de uma peça única com seu respectivo tamanho e estado de conservação
    * Então o sistema deve salvar o registro e gerar um código de barras exclusivo para impressão da etiqueta.
* **Cenário BDD (Negativo):**
    * Dado que o operador está na tela de cadastro de estoque
    * Quando tenta salvar uma peça sem preencher o tamanho ou estado de conservação
    * Então o sistema deve exibir uma mensagem de erro e impedir a geração do código de barras.

**[REQ-002] - Gestão de Consignação e Comissionamento**
* **Regra:** O sistema deve vincular a peça ao fornecedor original e calcular automaticamente a comissão (40% fornecedor / 60% loja) no momento da venda.
* **Cenário BDD (Positivo):**
    * Dado que uma peça consignada foi vendida no caixa
    * Quando o sistema processa o pagamento
    * Então o sistema deve registrar a venda e calcular automaticamente a comissão de 40% destinada ao fornecedor original.
* **Cenário BDD (Negativo):**
    * Dado que o operador tenta processar a venda de uma peça
    * Quando o sistema identifica que a peça não possui um fornecedor vinculado
    * Então o sistema deve bloquear o cálculo de comissão e alertar o operador sobre a inconsistência no cadastro.

**[REQ-003] - Pagamento com Crédito de Troca**
* **Regra:** O sistema deve permitir o uso de créditos pré-existentes do cliente como forma de pagamento, permitindo transações mistas (Crédito + Pix/Dinheiro).
* **Cenário BDD (Positivo):**
    * Dado que o cliente possui um saldo de crédito de troca no sistema
    * Quando o operador seleciona "Crédito de Troca" e outro método de pagamento para completar o valor da venda
    * Então o sistema deve abater o crédito e processar o restante através do outro método selecionado.
* **Cenário BDD (Negativo):**
    * Dado que o cliente tenta utilizar um crédito de R$ 100,00 possuindo apenas R$ 40,00 de saldo
    * Quando o operador tenta aplicar o valor total do crédito
    * Então o sistema deve negar a transação e solicitar o ajuste do valor para o saldo disponível.

**[REQ-004] - Desconto Automático por Tempo de Estoque**
* **Regra:** Peças cadastradas há mais de 45 dias devem sofrer uma redução automática de 20% no preço de venda no momento do checkout.
* **Cenário BDD (Positivo):**
    * Dado que uma peça está no sistema há 46 dias sem venda
    * Quando o item é lido no caixa
    * Então o sistema deve aplicar automaticamente um desconto de 20% sobre o preço original.
* **Cenário BDD (Negativo):**
    * Dado que uma peça está no sistema há 44 dias
    * Quando o item é lido no caixa
    * Então o sistema deve manter o preço original, sem aplicar o desconto de 20%.

**[REQ-005] - Emissão Digital de Recibo**
* **Regra:** O sistema deve oferecer a opção de envio do comprovante de venda via WhatsApp ou E-mail em substituição à impressão térmica.
* **Cenário BDD (Positivo):**
    * Dado que uma venda foi finalizada
    * Quando o operador optar pelo envio digital
    * Então o sistema deve enviar o comprovante para o canal escolhido (WhatsApp/E-mail) e capturar o contato do cliente para o banco de dados.
* **Cenário BDD (Negativo):**
    * Dado que o operador solicita o envio do recibo via WhatsApp
    * Quando o sistema detecta uma falha de conexão ou erro no envio
    * Então o sistema deve notificar o operador sobre a falha e permitir uma nova tentativa ou a impressão do comprovante.

**[REQ-006] - Consulta de Estoque por Filtros**
* **Regra:** O sistema deve permitir busca por categoria, tamanho e localização física (arara/setor) em tempo real.
* **Cenário BDD (Positivo):**
    * Dado que a vendedora consulta o sistema por "Vestido preto tamanho G"
    * Quando a busca é executada
    * Então o sistema deve exibir a disponibilidade e a respectiva localização física da peça na loja.
* **Cenário BDD (Negativo):**
    * Dado que a vendedora consulta um item inexistente ou sem estoque
    * Quando a busca é executada
    * Então o sistema deve informar que não existem produtos encontrados para os filtros aplicados.

**[REQ-007] - Relatório de Inteligência de Negócio**
* **Regra:** O sistema deve gerar relatórios sobre o desempenho de vendas por categoria e fornecedor para subsidiar decisões de curadoria.
* **Cenário BDD (Positivo):**
    * Dado que o administrador solicita o relatório de desempenho
    * Quando o sistema processa os dados do mês
    * Então o relatório deve listar os itens mais vendidos e os fornecedores cujas peças possuem maior giro.
* **Cenário BDD (Negativo):**
    * Dado que o administrador solicita um relatório de um período específico
    * Quando não houver registros de vendas nesse período
    * Então o sistema deve exibir uma mensagem informando que não há dados suficientes para gerar o relatório.

**[REQ-008] - Rastreabilidade do Histórico da Peça (Log de Auditoria)**
* **Regra:** O sistema deve manter um log imutável de cada peça, desde a entrada (avaliação/funcionário), alterações de preço e data final da venda.
* **Cenário BDD (Positivo):**
    * Dado que o administrador acessa o histórico de um item específico
    * Quando o sistema exibe os detalhes
    * Então devem estar visíveis: data de entrada, funcionário que avaliou, histórico de preços e data de venda efetivada.
* **Cenário BDD (Negativo):**
    * Dado que o administrador tenta acessar o histórico de um código de peça inexistente
    * Quando a consulta é realizada
    * Então o sistema deve emitir um aviso de "Peça não localizada no sistema".

### Requisitos Técnicos

* **Arquitetura de Dados:** O sistema deve utilizar banco de dados relacional para garantir a integridade da vinculação entre Peça, Fornecedor e Venda.
* **Protocolo de Integração:** O envio de recibos deve integrar com APIs de mensageria (WhatsApp Business API ou similares).
* **Auditoria:** O log de histórico deve ser imutável e armazenado com identificação do usuário responsável pela ação.