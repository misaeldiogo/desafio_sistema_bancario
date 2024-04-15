saldo = 0  # Variável para armazenar o saldo inicial da conta (R$ 0,00)
limite = 500  # Limite máximo para saque por transação que é de (R$ 500,00)
extrato = ""  # Variável para armazenar o histórico de transações (vazia no início)
numero_saques = 0  # Contador de saques realizados (iniciado em 0)
LIMITE_SAQUES = 3  # Limite máximo de saques por dia (3 saques)

while True:  # Loop principal do sistema, se repete até que o usuário escolha sair, aperando a letra q
    menu = "[d] Depositar\n[s] Sacar\n[e] Extrato\n[q] Sair\n\n=> "  # Menu de opções, importante - barra + n é para pular para próxima linha
    opcao = input(menu).lower()  # Captura a opção do usuário e converte para minúsculas

    if opcao == "d":  # Operação de depósito
        print("\n================ FAÇA O SEU DEPOSITO ===============")  # Cabeçalho do deposito, coloquei para melhorar a visualização
        valor = float(input("\nInforme o valor do seu depósito: "))  # Valor do depósito
        if valor > 0:  # Valida se o valor é positivo
            saldo += valor  # Atualiza o saldo
            extrato += f"\nDepósito: R$ {valor:.2f}"  # Adiciona o depósito ao extrato
            print("Parabéns o seu depósito foi realizado com sucesso!")  # Mensagem de sucesso
            print("\n====================================================")  # Rodapé do deposito concluido
            print("\nEscolha uma das opções abaixo:\n")
        else:
            print("\nOperação falhou! Valor inválido.")  # Mensagem de erro
            print("\n============== TENTE OUTRO VALOR ==================")  # Rodapé do deposito invalido
            print("\nEscolha uma das opções abaixo:\n")
			
    elif opcao == "s":  # Operação de saque
        print("\n================ FAÇA O SEU SAQUE ===============")  # Cabeçalho do saque
        valor = float(input("\nInforme o valor do saque: "))  # Valor do saque
        excedeu_saldo = valor > saldo  # Verifica se o valor excede o saldo
        excedeu_limite = valor > limite  # Verifica se o valor excede o limite
        excedeu_saques = numero_saques >= LIMITE_SAQUES  # Verifica se o limite de saques foi atingido

        if excedeu_saldo:
            print("\nOperação falhou! Saldo insuficiente.")  # Mensagem de erro (saldo insuficiente)
            print("\n============= FAÇA UM DEPÓSITO ==================")  # Rodapé do saldo insuficiente
            print("\nEscolha uma das opções abaixo:\n")
        elif excedeu_limite:
            print("\nOperação falhou! Limite de saque excedido.")  # Mensagem de erro (limite excedido)
            print("\n=========== TENTE UM VALOR MENOR ================")  # Rodapé do limite de saque excedido
            print("\nEscolha uma das opções abaixo:\n")
        elif excedeu_saques:
            print("\nOperação falhou! Limite de saques por dia excedido.")  # Mensagem de erro (limite de saques)
            print("\n============== ACESSE MAIS OPÇÕES ===============") # Rodapé do limite de saque
            print("\nEscolha uma das opções abaixo:\n") 
        elif valor > 0:
            saldo -= valor  # Atualiza o saldo
            extrato += f"\nSaque: R$ {valor:.2f}"  # Adiciona o saque ao extrato
            numero_saques += 1  # Incrementa o contador de saques
            print("\nSaque realizado com sucesso!")  # Mensagem de sucesso
            print("\n============== ACESSE MAIS OPÇÕES ===============") # Rodapé do saque realizado com sucesso
            print("\nEscolha uma das opções abaixo:\n")
        else:
            print("\nOperação falhou! Valor inválido.")  # Mensagem de erro (valor inválido)
            print("\n============= TENTE OUTRO VALOR =================")  # Rodapé do valor invalido
            print("\nEscolha uma das opções abaixo:\n")

    elif opcao == "e":  # Operação de extrato
        print("\n============ EXTRATO DETALHADO ===========")  # Cabeçalho do extrato
        print("\nNão foram realizadas movimentações." if not extrato else extrato)  # Exibe o histórico de transações ou mensagem "Não foram realizadas movimentações"
        print(f"\nSaldo: R$ {saldo:.2f}\n")  # Exibe o saldo atual
        print("=========== ACESSE MAIS OPÇÕES ===========")  # Rodapé do extrato
        print("\nEscolha uma das opções abaixo:\n")

    elif opcao == "q":  # Sair do sistema
        break  # Sai do loop principal

    else:  # Opção inválida
        print("Operação inválida, por favor selecione novamente a operação desejada.")