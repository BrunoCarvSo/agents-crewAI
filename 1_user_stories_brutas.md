# Documento de Requisitos: Sistema MeuPet

## 1. Módulo de Agendamento
**User Story:** Como funcionário do petshop, desejo visualizar um calendário de horários para agendar banhos e tosas, garantindo a organização dos serviços.

*   **Cenário 1: Bloqueio de horário na agenda**
    *   Dado que estou na tela de visualização do calendário
    *   Quando seleciono um horário disponível e preencho os dados do pet
    *   Então o sistema deve bloquear o horário e exibir o agendamento visualmente.

## 2. Comunicação e Lembretes
**User Story:** Como dono do petshop, desejo que o sistema envie lembretes automáticos via WhatsApp, para reduzir faltas e manter os pets com a vacinação em dia.

*   **Cenário 1: Envio de lembrete de agendamento**
    *   Dado que existe um agendamento para o dia seguinte
    *   Quando o sistema processar a rotina de envio diário
    *   Então um lembrete deve ser enviado para o WhatsApp do cliente.
*   **Cenário 2: Alerta de vacinação**
    *   Dado que o prazo da vacina do pet está próximo
    *   Quando a data limite for atingida
    *   Então o sistema deve enviar um alerta automático de vacinação via WhatsApp.

## 3. Controle de Estoque
**User Story:** Como operador de caixa, desejo ser alertado visualmente quando um produto atingir o estoque mínimo, para evitar a ruptura de vendas.

*   **Cenário 1: Gatilho de alerta vermelho**
    *   Dado que um produto possui menos de 5 unidades em estoque
    *   Quando o operador acessar a tela inicial do caixa
    *   Então o sistema deve exibir um alerta vermelho destacando o item com baixo estoque.

## 4. Programa de Fidelidade
**User Story:** Como cliente do petshop, desejo acumular pontos a cada compra, para futuramente trocar por serviços de banho.

*   **Cenário 1: Acúmulo de pontos**
    *   Dado que o cliente realizou uma compra no valor de R$ 10,00
    *   Quando a transação for concluída
    *   Então o sistema deve adicionar 1 ponto ao saldo do cliente.

## 5. Aplicativo Móvel (Câmera ao Vivo)
**User Story:** Como cliente, desejo acessar uma câmera ao vivo do meu pet durante o banho, para acompanhar o atendimento em tempo real.

*   **Cenário 1: Acesso ao streaming da câmera**
    *   Dado que o pet está em processo de banho e a câmera está ativa
    *   Quando o cliente abrir o aplicativo e selecionar a aba de acompanhamento
    *   Então o sistema deve exibir o streaming ao vivo do pet na área de banho.