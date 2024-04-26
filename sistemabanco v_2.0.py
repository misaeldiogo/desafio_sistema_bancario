import datetime # Biblioteca de manipulação de datas.

saldo = 0  # Variável para armazenar o saldo inicial da conta (R$ 0,00).
limite = 500  # Limite máximo para saque por transação que é de (R$ 500,00).
extrato = ""  # Variável para armazenar o histórico de transações (vazia no início).
numero_saques = 0  # Contador de saques realizados (iniciado em 0).
LIMITE_SAQUES = 3  # Limite máximo de saques por dia (3 saques).
numero_conta = 1 # Número da Conta (sequencial, iniciado em 1).
agencia = "0001" # Agencia bancária (fixa).
contas = [] # Lista para armazenar contas bancárias.
usuarios = [] # Lista para armazenar usuários.

def listar_contas(): # Lista contas que já foram cadastradas.
    """
    Exibe a lista de contas bancárias cadastradas.

    """
    if not contas:
        print("\nNão há contas bancárias cadastradas.\n") # Não conta bancária cadastrada.
        return

    print("\n============ LISTA DE CONTAS =============") # Cebeçalho.
    for conta in contas:
        print(f"\nNúmero: {conta['numero']}") # Numero da conta.
        print(f"Titular: {conta['titular']}") # Nome do Titular da conta.
        print(f"Saldo: R$ {conta['saldo']:.2f}") # Saldo da conta.
        

def criar_usuario(nome: str, data_nascimento: str, cpf: str, endereco: str) -> dict: # Função para criar usuário.
    """ 
    Cria um novo usuário no sistema.

    Argumentos:
        nome (str): Nome completo do usuário.
        data_nascimento (str): Data de nascimento no formato dd/mm/aaaa.
        cpf (str): CPF do usuário (apenas números).
        endereco (str): Endereço completo do usuário. 
    """

    novo_usuario = { # Preenchimento de dados para criação de um novo usuário.
        "nome": nome, # Nome.
        "data_nascimento": data_nascimento, # Data de Nascimento.
        "cpf": cpf, # CPF.
        "endereco": endereco # Endereço.
    }

    return novo_usuario # Retorno da criação do usuário.

def criar_conta(usuario: dict) -> dict: # Criar nova conta bancária.
    
    """
    Cria uma nova conta bancária para um usuário.

    Argumentos:
        usuario (dict): Dicionário contendo as informações do usuário (nome, data_nascimento, cpf, endereco).

    Retorno:
        dict: Dicionário contendo as informações da nova conta.
        str: Mensagem de erro caso a criação da conta falhe.
    
    """    
            
    global numero_conta, contas # Variaveis globais dentro de criar_conta.

    if not usuario.get("cpf"): # Se o usuário não tem CPF cadastrado.
        return None, "Usuário não possui CPF cadastrado." # Retorno sobre CPF cadastrado do novo usuário.

    conta_existente = buscar_usuario_por_cpf(usuario["cpf"]) # Usuário com conta existe, comando para buscar.
    if conta_existente: # Buscar a conta existente.
        if "numero" in conta_existente: # Ver se o numero vai bater certo com a conta.
            return None, f"Usuário já possui uma conta bancária (Número: {conta_existente['numero']})." # Retorno, usuário já possui conta.
        
    nova_conta = {   # Nova conta sendo gravada.
        "numero": numero_conta, # Número da conta.
        "agencia": "0001", # Agencia.
        "saldo": 0.0, # Saldo.
        "titular": usuario["nome"], # Nome do titular da conta.
        "extrato": "", # Extrato.
        "cpf": usuario["cpf"], # CPF.
        "saques": 0  # Adicione um contador de saques aqui

    }

    contas.append(nova_conta) # Armazenação de informações sobre novas contas registradas.
    numero_conta += 1 # Incrementar o valor da variável global numero_conta em 1.

    return nova_conta, None # Retorno nova conta ou erro.

def buscar_usuario_por_cpf(cpf_usuario: str) -> dict or None: # Busca o usuário pelo CPF.
    """
    Busca um usuário pelo CPF.

    Argumentos:
        cpf (str): CPF do usuário.

    Retorno:
        dict: Dicionário contendo as informações do usuário encontrado, ou None caso não seja encontrado.
    """

    for usuario in usuarios:
        if usuario["cpf"] == cpf_usuario:
            return usuario
    return None

def buscar_conta_por_numero(numero_conta: str) -> dict or None: # Procura uma conta bancária pelo número da conta.
    for conta in contas:
        if conta["numero"] == int(numero_conta):
            return conta
    return None

def depositar(conta: dict, valor: float) -> float or None: # Fazer depósito em conta bancária.
    if valor <= 0:
        return None, "Valor inválido para depósito."

    conta["saldo"] += valor
    conta["extrato"] += f"\nDeposito: R${valor:.2f}" # Adiciona transação ao extrato.
    return conta["saldo"], None

def extrato(conta: dict) -> str: # Ver o extrato
    return conta["extrato"]

total_sacado = 0

saques_diarios = {} # Dicionario global para armazenar saques por dia.

def sacar(conta: dict, valor: float) -> float or None: # Sacar 
    global total_sacado
    if valor <= 0:
        return None, "Valor inválido para saque."
    
    if valor > 500:
        return None, "O valor máximo para saque é R$500."
    
    if total_sacado + valor > 500:
        return None, "Você atingiu seu limite de saque de R$500."

    hoje = datetime.date.today().strftime("%d/%m/%Y")  # Data atual no formato dd/mm/aaaa
    if not saques_diarios.get(conta["numero"]):
        saques_diarios[conta["numero"]] = {}  # Inicializa o dicionário para a conta
    
    if saques_diarios[conta["numero"]].get(hoje, 0) >= LIMITE_SAQUES:
        return None, "Você atingiu seu limite de 3 saques diários."
            
    if conta["saldo"] < valor:
        return None, "Saldo insuficiente para saque."

    conta["saldo"] -= valor
    total_sacado += valor
    conta["extrato"] += f"\nSaque: R$ {valor:.2f}"  # Adiciona a transação no extrato
    saques_diarios[conta["numero"]][hoje] = saques_diarios[conta["numero"]].get(hoje, 0) + 1
    return conta["saldo"], None

def main():
    """
    Função principal do sistema bancário.

    """
    global usuarios, contas

    while True: # Criar uma repetição continua.
        print("\n================ MENU ===============")  # Cabeçalho do MENU, coloquei para melhorar a visualização.
        print("\nEscolha uma das oções abaixo:")  # Mensagem para escolher uma opção.
        menu = "\n[u] Cadastrar Usuário\n[c] Criar Conta\n[l] Listar Contas\n[d] Depositar\n[s] Sacar\n[e] Extrato\n[q] Sair\n\n=> "  # Menu de opções, importante - barra + n é para pular para próxima linha
        opcao = input(menu).lower()  # Captura a opção do usuário e converte para minúsculas
        
        

        if opcao == "q": # Sair da conta.
            print("\n================ AGUARDE ===============")  # Cabeçalho da opção SAIR.
            print("\nAguarde um instante estamos saindo do sistema bancário...\n") # Saindo do loop principal, não vai mais repetir.
            print("======== OBRIGADO POR AGUARDA ==========\n") # Roda pé do menu sair.
            break # Encerrar o ciclo.

        elif opcao == "u":  # Cadastrar Usuário
            print("\n=============== CADASTRE-SE ===============")  # Cabeçalho da opção CADASTRE-SE.
            nome = input("\nNome completo: ") # Nome completo do novo usuário.
            data_nascimento = input("Data de nascimento (dd/mm/aaaa): ") # Data de nascimento do novo usuário.
            cpf = input("CPF (apenas números): ") # CPF do novo usuário.
            endereco = input("Endereço completo: ") # Endereço do novo usuário.                    

            novo_usuario = criar_usuario(nome, data_nascimento, cpf, endereco) # Cria um novo usuário.
            if novo_usuario is not None:
                usuarios.append(novo_usuario)
                print(f"\nUsuário {nome} cadastrado com sucesso!\n") # Resposta que o usuário foi cadastrado com sucesso
            else:
                print("\nFalha ao cadastrar usuário. Tente novamente!\n") # Resposta que houve falha ao cadastrar o novo usuário.

        elif opcao == "c":  # Criar Conta corrente.
            print("\n========== CRIE SUA CONTA ==========")  # Cabeçalho da opção CRIAR CONTA.
            cpf_usuario = input("\nCPF do usuário: ") # CPF do usuário para criar a conta corrente.
            usuario = buscar_usuario_por_cpf(cpf_usuario) # Faz a busca do CPF do usuário, para verificar se o mesmo já tem conta corrente cadastrada
            if not usuario:  # Usuário não tem cpf cadastrado ou colocou os números errado.
                print(f"\nUsuário com CPF {cpf_usuario} não encontrado.\n") # CPF do usuário não foi encontrado.
            else:
                nova_conta, erro = criar_conta(usuario) # Erro ao criar nova conta corrente.

                if nova_conta:  # Tudo certo para nova conta corrente será criada.
                    print(f"\nConta criada com sucesso para o usuário {usuario['nome']}.") # Resposta que a conta foi criada com sucesso.
                    print(f"\nNúmero da conta: {nova_conta['numero']}\n") # Gerar o número da conta.
                else:
                    print(f"\nFalha ao criar conta: {erro}\n") # Falha ao criar o número da conta.

        elif opcao == "d":  # Depositar
            print("\n========= FAÇA O SEU DEPÓSITO =========")  # Cabeçalho da opção sair.
            numero_conta = input("\nNúmero da conta: ") # Número da conta que receberá o depósito.
            
            # Verifica se o número da conta é numérico
            if not numero_conta.isdigit():
                print("Número da conta inválido. Por favor, insira um número.")
                continue

            valor = float(input("Valor a ser depositado: R$ ")) # Valor do depósito.

            conta = buscar_conta_por_numero(numero_conta) # Comando para buscar o nuúmero da conta digitado.
            if not conta:
                print(f"\nConta {numero_conta} não encontrada.\n") # Número da conta não encontrado.
            else:
                novo_saldo, erro = depositar(conta, valor) # Novo saldo ou erro.
                if novo_saldo:
                    print(f"\nDepósito realizado com sucesso!\n") # Resposta que o depósito foi realizado com sucesso.
                    print(f"Novo saldo: R$ {novo_saldo:.2f}") # Atualização do novo saldo, após o deposito.
                else:
                    print(f"\nFalha ao realizar depósito: {erro}\n") # Erro ao fazer o depósito. (caractere errado)


        elif opcao == "s":  # Sacar
            print("\n========= FAÇA O SEU SAQUE ==========")  # Cabeçalho da opção sair.
            numero_conta = input("\nNúmero da conta: ") # Número da conta que vai executar o saque.
            
            # Verifica se o número da conta é numérico
            if not numero_conta.isdigit():
                print("Número da conta inválido. Por favor, insira um número.")
                continue

            valor = input("Valor a ser sacado: R$ ") # Valor a ser sacado.
            
            # Verifica se o valor é numérico
            if not valor.replace('.', '', 1).isdigit():
                print("Valor inválido. Por favor, insira um número.")
                continue

            try:
                valor = float(valor)
                # Continue com o saque...
            except ValueError:
                print("Erro: Você não digitou um número válido.")


            conta = buscar_conta_por_numero(numero_conta) # Comando para buscar o nuúmero da conta digitado.
            if not conta:
                print(f"\nConta {numero_conta} não encontrada.\n") # Número da conta não encontrado.
            else:
                novo_saldo, erro = sacar(conta, valor) # Novo saldo ou erro.
                if novo_saldo:
                    print(f"\nSaque realizado com sucesso!\n") # Saque foi realizado com sucesso.
                    print(f"\nNovo saldo: R$ {novo_saldo:.2f}\n") # Atualização do novo saldo, após o saque.
                else:
                    print(f"\nFalha ao realizar saque: {erro}\n") # Erro ao realizar o saque.

        elif opcao == "e":  # Extrato
            print("\n============ EXTRATO DETALHADO =============") # Cabeçalho do extrato.
            numero_conta = input("\nNúmero da conta: ") # Número da conta para verificação do extrato.
            if numero_conta.isdigit():
                conta = buscar_conta_por_numero(numero_conta)
            else:
                print("Número da conta inválido. Por favor, insira um número.")
                        

            conta = buscar_conta_por_numero(numero_conta) # Comando para buscar o nuúmero da conta digitado.
            if not conta:
                print(f"\nConta {numero_conta} não encontrada.\n") # Número da conta não encontrado.
            else:
                print("\n============ EXTRATO DETALHADO =============") # Cabeçalho do extrato.
                if not conta.get("extrato"): 
                    print("\nNão há movimentações na conta.") # Resposta quando não há movimentação no extrato.
                else:
                    print(conta["extrato"]) # Movimentações no extrato
                print(f"\nSaldo: R$ {conta['saldo']:.2f}\n") # Saldo dentro do extrato.

        elif opcao == "l":  # Listar Contas
            listar_contas() # Mostrar a quantidade de contas que o usuário tem cadastrada.

        else:
            print("\nOpção inválida. Por favor, selecione uma opção válida.\n") # Tentou sacar sem ter saldo.


if __name__ == "__main__":
    main()