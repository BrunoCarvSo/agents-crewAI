**[REQ-001] - Cadastro Individual de Peças Únicas**
* **Regra:** Cada item deve ser registrado individualmente com atributos específicos (tamanho, estado de conservação) e possuir um código de barras exclusivo gerado pelo sistema.
* **Cenário BDD:**
    * Dado que o operador acessa a tela de cadastro de estoque
    * Quando insere os dados de uma peça única com seu respectivo tamanho e estado de conservação
    * Então o sistema deve salvar o registro e gerar um código de barras exclusivo para impressão da etiqueta.

**[REQ-002] - Gestão de Consignação e Comissionamento**
* **Regra:** O sistema deve vincular a peça ao fornecedor original e calcular automaticamente a comissão (40% fornecedor / 60% loja) no momento da venda.
* **Cenário BDD:**
    * Dado que uma peça consignada foi vendida no caixa
    * Quando o sistema processa o pagamento
    * Então o sistema deve registrar a venda e calcular automaticamente a comissão de 40% destinada ao fornecedor original.

**[REQ-003] - Pagamento com Crédito de Troca**
* **Regra:** O sistema deve permitir o uso de créditos pré-existentes do cliente como forma de pagamento, permitindo transações mistas (Crédito + Pix/Dinheiro).
* **Cenário BDD:**
    * Dado que o cliente possui um saldo de crédito de troca no sistema
    * Quando o operador seleciona "Crédito de Troca" e outro método de pagamento para completar o valor da venda
    * Então o sistema deve abater o crédito e processar o restante através do outro método selecionado.

**[REQ-004] - Desconto Automático por Tempo de Estoque**
* **Regra:** Peças cadastradas há mais de 45 dias devem sofrer uma redução automática de 20% no preço de venda no momento do checkout.
* **Cenário BDD:**
    * Dado que uma peça está no sistema há 46 dias sem venda
    * Quando o item é lido no caixa
    * Então o sistema deve aplicar automaticamente um desconto de 20% sobre o preço original.

**[REQ-005] - Emissão Digital de Recibo**
* **Regra:** O sistema deve oferecer a opção de envio do comprovante de venda via WhatsApp ou E-mail em substituição à impressão térmica.
* **Cenário BDD:**
    * Dado que uma venda foi finalizada
    * Quando o operador optar pelo envio digital
    * Então o sistema deve enviar o comprovante para o canal escolhido (WhatsApp/E-mail) e capturar o contato do cliente para o banco de dados.

**[REQ-006] - Consulta de Estoque por Filtros**
* **Regra:** O sistema deve permitir busca por categoria, tamanho e localização física (arara/setor) em tempo real.
* **Cenário BDD:**
    * Dado que a vendedora consulta o sistema por "Vestido preto tamanho G"
    * Quando a busca é executada
    * Então o sistema deve exibir a disponibilidade e a respectiva localização física da peça na loja.

**[REQ-007] - Relatório de Inteligência de Negócio**
* **Regra:** O sistema deve gerar relatórios sobre o desempenho de vendas por categoria e fornecedor para subsidiar decisões de curadoria.
* **Cenário BDD:**
    * Dado que o administrador solicita o relatório de desempenho
    * Quando o sistema processa os dados do mês
    * Então o relatório deve listar os itens mais vendidos e os fornecedores cujas peças possuem maior giro.

**[REQ-008] - Rastreabilidade do Histórico da Peça (Log de Auditoria)**
* **Regra:** O sistema deve manter um log imutável de cada peça, desde a entrada (avaliação/funcionário), alterações de preço e data final da venda.
* **Cenário BDD:**
    * Dado que o administrador acessa o histórico de um item específico
    * Quando o sistema exibe os detalhes
    * Então devem estar visíveis: data de entrada, funcionário que avaliou, histórico de preços e data de venda efetivada.