import textwrap
from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime

saldo = 0  # Variável para armazenar o saldo inicial da conta (R$ 0,00).
limite = 500  # Limite máximo para saque por transação que é de (R$ 500,00).
extrato = ""  # Variável para armazenar o histórico de transações (vazia no início).
numero_saques = 0  # Contador de saques realizados (iniciado em 0).
LIMITE_SAQUES = 3  # Limite máximo de saques por dia (3 saques).
numero_conta = 1  # Número da Conta (sequencial, iniciado em 1).
agencia = "0001"  # Agencia bancária (fixa).
contas = []  # Lista para armazenar contas bancárias.
usuarios = []  # Lista para armazenar usuários.

class ContaIterador:
    def __init__(self, contas):
        self._contas = contas

    def __iter__(self):
        return self

    def __next__(self):
        if not self._contas:
            raise StopIteration

        conta = self._contas.pop(0)
        return conta

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
            return False

        elif valor > 0:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True

        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
            return True
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")

        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )

    def gerar_relatorio(self, tipo_transacao=None):
        if tipo_transacao is None:
            tipo_transacao = "Todas"

        print(f"\n\n====== HISTÓRICO - {tipo_transacao} ======\n")

        for transacao in self.transacoes:
            if tipo_transacao == "Todas" or transacao["tipo"] == tipo_transacao:
                data_hora = transacao["data"]
                valor = transacao["valor"]
                tipo = transacao["tipo"]
                print(f"{tipo}: R$ {valor:.2f} - {data_hora}")


class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


def log_transacao(func):
    def wrapper(*args, **kwargs):
        cpf = input("Informe o CPF do cliente: ")
        clientes = args[0]
        cliente = filtrar_cliente(cpf, clientes)

        if not cliente:
            print("\n@@@ Cliente não encontrado! @@@")
            return

        conta = recuperar_conta_cliente(cliente)

        if not conta:
            return

        valor = float(input("Informe o valor: "))

        tipo_transacao = func.__name__

        if tipo_transacao == "sacar":
            transacao = Saque(valor)

        elif tipo_transacao == "depositar":
            transacao = Deposito(valor)

        else:
            raise ValueError(f"Tipo de transação inválido: {tipo_transacao}")

        cliente.realizar_transacao(conta, transacao)

        data_hora = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        print(f"\n=== {tipo_transacao} realizado com sucesso! ===")
        print(f"{tipo_transacao}: R$ {valor:.2f} - {data_hora}")

        conta.historico.gerar_relatorio(tipo_transacao)

        return func(cliente, *args[1:], **kwargs)

    return wrapper

def menu():

    menu = """
        ================ MENU ================
        [d]\tDepositar
        [s]\tSacar
        [e]\tExtrato
        [u]\tNovo usuário
        [c]\tNova conta
        [l]\tListar contas
        [g]\tGerar Relatório
        [i]\tIterador de Contas
        [q]\tSair
        => """
    return input(textwrap.dedent(menu))


def filtrar_cliente(cpf, clientes):
    cliente_encontrado = next((cliente for cliente in clientes if cliente.cpf == cpf), None)  # Retorna o cliente ou None se não encontrado
    return cliente_encontrado

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n@@@ Cliente não possui conta! @@@")
        return

    print("\n==== Contas do Cliente ====\n")
    for i, conta in enumerate(cliente.contas):
        print(f"{i + 1} - {conta}")

    try:
        opcao_conta = int(input("Informe o número da conta desejada: ")) - 1
    except ValueError:
        print("\n@@@ Opção inválida! @@@")
        return None

    if 0 <= opcao_conta < len(cliente.contas):
        return cliente.contas[opcao_conta]
    else:
        print("\n@@@ Opção inválida! @@@")
        return None


@log_transacao
def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


@log_transacao
def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n================ EXTRATO ================")

    tipo_transacao = input(
        "Selecione o tipo de transação a ser exibido (Todas, Saques ou Depósitos): "
    ).upper()

    conta.historico.gerar_relatorio(tipo_transacao)

    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================")

def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente número): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\n@@@ Já existe cliente com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)
    print("\n=== Cliente criado com sucesso! ===")

def criar_conta(clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado, fluxo de criação de conta encerrado! @@@")
        return

    print(f"Cliente encontrado: {cliente.nome}")
    numero_conta = len(contas) + 1
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)

    if not conta:
        print("\n@@@ Falha ao criar a conta! @@@")

    contas.append(conta)
    cliente.contas.append(conta)

    print("\n=== Conta criada com sucesso! ===")


def listar_contas(contas):
    for conta in ContaIterador(contas):
        print("=" * 100)
        print(textwrap.dedent(str(conta)))

def gerar_relatorio(contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)  

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    gerador_transacoes = conta.historico.gerar_relatorio()

    tipo_transacao = input("Selecione o tipo de transação (Todas, Saques ou Depósitos): ").upper()
    if tipo_transacao != "TODAS":
        gerador_transacoes = (transacao for transacao in gerador_transacoes if transacao["tipo"] == tipo_transacao)

    for transacao in gerador_transacoes:
        data_hora = transacao["data"]
        valor = transacao["valor"]
        tipo = transacao["tipo"]
        print(f"{tipo}: R$ {valor:.2f} - {data_hora}")

    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================")


clientes = []  # Globalizando a variável 'clientes'

def iterador_contas(contas):
    global clientes
    cpf = input("Informe o CPF do cliente")
    cliente = filtrar_cliente(cpf, clientes)  # Acessando a variável global
    iterador_contas = ContaIterador(contas)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    # Imprimindo as informações de cada conta
    for conta in iterador_contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))
        print(f"Saldo: R$ {conta.saldo:.2f}")

def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()
        
        if opcao == "d":
            depositar(clientes)

        elif opcao == "s":
            sacar(clientes)

        elif opcao == "e":
            exibir_extrato(clientes)

        elif opcao == "u":
            criar_cliente(clientes)

        elif opcao == "c":
            criar_conta(clientes, contas)

        elif opcao == "l":
            listar_contas(contas)

        elif opcao == "g":
            gerar_relatorio(contas)

        elif opcao == "i":
            iterador_contas(contas)

        elif opcao == "q":
            break

        else:
            print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")

if __name__ == "__main__":
    main()