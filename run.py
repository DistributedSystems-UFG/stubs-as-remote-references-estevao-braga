import pickle
import sys
from time import sleep

from constRPC import *
from client import *
from server import *
from dbclient import *


def client1():
    print("[Client1] Iniciando...")

    c1 = Client(PORTC1)
    db = DBClient(HOSTS, PORTS)

    print("[Client1] Criando lista remota...")
    db.create()

    print("[Client1] Inserindo dado...")
    db.appendData('Client 1')

    print("[Client1] Enviando referência para Client2...")
    sleep(2)  # tempo para garantir que client2 esteja rodando

    c1.sendTo(HOSTC2, PORTC2, db)

    print("[Client1] Finalizado.")


def client2():
    print("[Client2] Aguardando dados...")

    c2 = Client(PORTC2)

    data = c2.recvAny()
    db = pickle.loads(data)

    print("[Client2] Referência recebida!")

    db.appendData('Client 2')

    result = db.getValue()
    print("[Client2] Lista final:", result)

    # encerra servidor
    c2.sendTo(HOSTS, PORTS, [STOP])

    print("[Client2] Finalizado.")


def server_process():
    print("[Server] Iniciando...")
    s = Server(PORTS)
    s.run()
    print("[Server] Encerrado.")


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Uso:")
        print("  python run.py server")
        print("  python run.py client1")
        print("  python run.py client2")
        exit(1)

    role = sys.argv[1]

    if role == "server":
        server_process()

    elif role == "client1":
        client1()

    elif role == "client2":
        client2()

    else:
        print("Role inválido:", role)