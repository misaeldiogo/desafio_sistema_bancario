from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime

class Transacao(ABC): # Classe Abstrata
    @property
    @abstractproperty
    def valor(self):  # Propriedade abstrata valor, implementada pelas classes filhas.
        pass

    @abstractclassmethod
    def registrar(self, conta): # Propriedade da classe método abstrato, define como a trasação é registrada na conta.
        pass

class Saque(Transacao):  # Classe Herdeira - Representa uma trasação de saque em conta.
    def __init__(self, valor):
        self._valor = valor # Armazena o valor do saque.

    @property
    def valor(self):  # Implementa a propriedade valor
        return self._valor  # Retorna para o armazenamento do valor do saque.

    def registrar(self, conta): # Implementa o método registrar para realizar o saque na conta.
        sucesso_transacao = conta.sacar(self.valor) # Confirmação que a transação foi realizada com sucesso.

        if sucesso_transacao: # Verifica se o saque excede o limite da conta.
            conta.historico.adicionar_transacao(self) # Atualiza o saldo da conta e adiciona a transação ao histórico.

class Deposito(Transacao):  # Classe Herdeira
    def __init__(self, valor): # Representa uma transação de depósito em conta.
        self._valor = valor # Armazena o valor do depósito.

    @property
    def valor(self):  #  Implementa a propriedade valor, para retornar o valor do deposito armazenado. (Linha 30)
        return self._valor

    def registrar(self, conta):   #  Implementa o método registrar para realizar o deposito na conta. 
        sucesso_transacao = conta.depositar(self.valor) 

        if sucesso_transacao:  # Atualiza o saldo da conta e adiciona a transação ao histórico.
            conta.historico.adicionar_transacao(self)

class Conta(ABC): # Classe Abstrata
    @classmethod
    def nova_conta(cls, cliente, numero): # Define a estrutura básica para contas bancárias
        return cls(numero, cliente)

    @abstractproperty
    def saldo(self):   # Saldo - Propriedade abstrata
        pass

    @abstractproperty
    def numero(self): # Número da conta - Propriedade abstrata
        pass

    @abstractproperty
    def agencia(self): # Número da agencia - Propriedade abstrata
        pass

    @abstractproperty
    def cliente(self): # Nome do cliente - Propriedade abstrata
        pass

    @abstractproperty
    def historico(self): # Histórico - Propriedade abstrata
        pass

    def sacar(self, valor): # Sacar - Metodo abstrato
        pass

    def depositar(self, valor): # Depositar - Metodo abstrato
        pass

class ContaCorrente(Conta): # Classe Herdeira
    def __init__(self, numero, cliente, limite=500, limite_saques=3):  # Representa uma conta corrente com funcionalidades específicas.
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor): # Implementa o método sacar para realizar saques na conta.
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques 

        if excedeu_limite: # Verifica se o valor do saque excede o limite.
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")

        elif excedeu_saques: # Verifica se o valor do saque excede o número máximo de saques diários.
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")

        else:
            return super().sacar(valor)

        return False

    def __str__(self):  # Implementa o método __str__ para retornar uma representação textual da conta.
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """

class Cliente: # Armazena os dados do cliente, como endereço e contas bancárias.
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao): # Métodos para realizar transações em contas e adicionar novas contas.
        transacao.registrar(conta)

    def adicionar_conta(self, conta): 
        self.contas.append(conta)

class Historico: # Armazena o histórico de transações de uma conta.
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):  
        return self._transacoes

    def adicionar_transacao(self, transacao):  # Métodos para adicionar e consultar transações
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )
