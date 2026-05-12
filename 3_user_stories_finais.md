# Documento de Requisitos: Sistema MeuPet

## 1. Módulo de Agendamento
**User Story:** Como funcionário do petshop, desejo visualizar um calendário de horários para agendar banhos e tosas, garantindo a organização dos serviços.

*   **Cenário 1: Bloqueio de horário na agenda**
    *   **Dado** que estou na tela de visualização do calendário
    *   **Quando** seleciono um horário disponível e preencho os dados do pet e do serviço
    *   **Então** o sistema deve bloquear o horário selecionado e exibir o agendamento visualmente no calendário.

## 2. Comunicação e Lembretes
**User Story:** Como dono do petshop, desejo que o sistema envie lembretes automáticos via WhatsApp, para reduzir faltas e manter os pets com a vacinação em dia.

*   **Cenário 1: Envio de lembrete de agendamento**
    *   **Dado** que existe um agendamento confirmado para o dia seguinte
    *   **Quando** o sistema processar a rotina de envio de mensagens diárias (agendada para as 08:00)
    *   **Então** o sistema deve disparar um lembrete via API de WhatsApp para o número cadastrado do cliente.
*   **Cenário 2: Alerta de vacinação**
    *   **Dado** que o prazo de vencimento da vacina do pet está a menos de 3 dias
    *   **Quando** a rotina de verificação diária for executada
    *   **Então** o sistema deve enviar um alerta automático de vacinação via WhatsApp para o tutor responsável.

## 3. Controle de Estoque
**User Story:** Como operador de caixa, desejo ser alertado visualmente quando um produto atingir o estoque mínimo, para evitar a ruptura de vendas.

*   **Cenário 1: Gatilho de alerta de estoque crítico**
    *   **Dado** que um produto possui estoque igual ou inferior a 5 unidades
    *   **Quando** o operador acessar a tela inicial do PDV (Ponto de Venda)
    *   **Então** o sistema deve exibir um alerta visual na cor vermelha, listando os itens com baixo estoque.

## 4. Programa de Fidelidade
**User Story:** Como cliente do petshop, desejo acumular pontos a cada compra, para futuramente trocar por serviços de banho.

*   **Cenário 1: Acúmulo de pontos**
    *   **Dado** que o cliente realizou uma compra válida
    *   **Quando** a transação financeira for concluída com sucesso
    *   **Então** o sistema deve calcular e adicionar pontos ao saldo do cliente na proporção de 1 ponto a cada R$ 10,00 gastos.
*   **Nota Técnica de Implementação:** O parâmetro de resgate (quantidade de pontos necessária para trocar por um serviço de banho) está pendente de definição estratégica pelo departamento financeiro. A lógica de conversão deve ser implementada via variável configurável no *back-end* para permitir atualização posterior sem necessidade de *redeploy* ou alteração de código.

## 5. Aplicativo Móvel (Câmera ao Vivo)
**User Story:** Como cliente, desejo acessar uma câmera ao vivo do meu pet durante o banho, para acompanhar o atendimento em tempo real.

*   **Cenário 1: Acesso ao streaming da câmera**
    *   **Dado** que o pet está sob atendimento e o status do serviço é "Em execução"
    *   **Quando** o cliente acessar o aplicativo e selecionar a aba "Acompanhamento em Tempo Real"
    *   **Então** o sistema deve realizar o *handshake* com o serviço de streaming e exibir a transmissão ao vivo da câmera vinculada à baia de banho.