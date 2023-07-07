import datetime
import os
from json import dump, dumps, load, loads

menu = """
MENU
==============
[d] - DEPOSITO
[s] - SAQUE
[e] - EXTRATO
[q] - ENCERRAR
==============
"""

def deposito(valor, saldo, depositos):
    dp = depositos.copy()
    if valor > 0:
        saldo += valor
        deposito = {"valor": valor,
                    "data": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "ope": "+",}
        dp.append(deposito)
        print("DEPOSITO EFETUADO COM SUCESSO!")
    else:
        print("OCORREU UM ERRO E O DEPÓSITO NÃO FOI EFETUADO.")
    return saldo, dp

def contar_saques(saque):
    contador = 0
    for saque in saques:
        now = datetime.datetime.now()
        dia = datetime.date(now.year, now.month, now.day)
        dia_saque_dt = datetime.datetime.strptime(saque["data"], "%d/%m/%Y %H:%M:%S")
        dia_saque = datetime.date(dia_saque_dt.year, dia_saque_dt.month, dia_saque_dt.day)
        if dia_saque == dia:
            contador += 1
    return contador

def saque(valor, saldo, saques):
    sq = saques.copy()
    if contar_saques(sq) >= 3:
        print("LIMITE DE SAQUES DIÁRIOS ATINGIDO")
    elif valor > LIMITE_SAQUE:
        print("VALOR LIMITE POR SAQUE EXCEDIDO")
    elif valor > saldo:
        print("SALDO INDISPONÍVEL PARA SAQUE")
    else:
        saldo -= valor
        saque_ = {"valor": valor,
                 "data": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                 "ope": "-",}
        sq.append(saque_)
        print("SAQUE EFETUADO COM SUCESSO.")
    return saldo, sq

def extrato(saldos, depositos, saques):
    saldos.sort(key=lambda x : x["data"])
    depositos.sort(key=lambda x : x["data"])
    saques.sort(key=lambda x : x["data"])
    delta = datetime.timedelta(days=30)
    saldos_e = []
    extrato = []
    for saq in saques:
        extrato.append(saq)
    for deposito in depositos:
        extrato.append(deposito)
    extrato.sort(key=lambda x : x["data"])
    for saldo in saldos:
        sald_data = datetime.datetime.strptime(saldo["data"], "%d/%m/%Y %H:%M:%S")
        if datetime.datetime.now() - delta <= sald_data <= datetime.datetime.now():
            saldos_e.append(saldo)
    saldos_e.sort(key=lambda x : x["data"])
    for i in range(len(saldos_e) - 1):
        data = datetime.datetime.strptime(saldos_e[i]["data"], "%d/%m/%Y %H:%M:%S")
        hoje = datetime.datetime.now()
        valor = saldos_e[i]["valor"]
        prox_data = datetime.datetime.strptime(saldos_e[i + 1]["data"], "%d/%m/%Y %H:%M:%S")
        prox_valor = saldos_e[i + 1]["valor"]
        data_ant = datetime.datetime(year=1991, month=11, day=4)
        if i > 0:
            data_ant = datetime.datetime.strptime(saldos_e[i - 1]["data"], "%d/%m/%Y %H:%M:%S")
        if i == 0 or ((data.day, data.month, data.year) != (data_ant.day, data_ant.month, data_ant.year)):
            print(f"{data.day:2}/{data.month}/{data.year}", end=" ")
            valor_str = f"{valor:.2f}"
            print(f"SALDO: R${valor_str.rjust(10)}")
        for operacao in extrato:
            data_op = datetime.datetime.strptime(operacao["data"], "%d/%m/%Y %H:%M:%S")
            valor_op = operacao["valor"]
            sinal = operacao["ope"]
            if data < data_op <= prox_data:
                print(f"{data_op.day:2}/{data_op.month}/{data_op.year}", end=" ")
                valor_op_str = f"{valor_op:.2f}"
                print(f"{sinal:>6} R${valor_op_str.rjust(10)}")
        if i == len(saldos_e) - 2:
            print(f"{prox_data.day:2}/{prox_data.month}/{prox_data.year}", end=" ")
            prox_valor_str = f"{prox_valor:.2f}"
            print(f"SALDO: R${prox_valor_str.rjust(10)}")

saldos = []
depositos = []
saques = []
if os.path.exists("saldos.json"):
    with open("saldos.json", "r") as file:
        saldos = load(file)
if os.path.exists("saques.json"):
    with open("saques.json", "r") as file:
        saques = load(file)
if os.path.exists("depositos.json"):
    with open("depositos.json", "r") as file:
        depositos = load(file)
saldo = 0
if not saldos:
    saldos = [{"valor": 1000, "data": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")},]
LIMITE_SAQUE = 500
saldo = saldos[-1]["valor"]
while True:
    try:
        print(menu)
        op = input("ESCOLHA UMA OPÇÃO: ")
        if op.lower() == 'd':
            valor = float(input("ENTRE O VALOR A DEPOSITAR: "))
            saldo, depositos = deposito(valor, saldo, depositos)
            saldo_d = {"valor": saldo,
                       "data": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
            saldos.append(saldo_d)
        elif op.lower() == 's':
            valor = float(input("ENTRE O VALOR A SACAR: "))
            saldo, saques = saque(valor, saldo, saques)
            saldo_d = {"valor": saldo,
                       "data": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
            saldos.append(saldo_d)
        elif op.lower() == 'e':
            print("\nEXTRATO DOS ÚLTIMOS 30 DIAS")
            print("-" * 30)
            extrato(saldos, depositos, saques)
            print("-" * 30)
        elif op.lower() == 'q':
            print("OBRIGADO POR UTILIZAR O NOSSO SISTEMA! ATÉ A PRÓXIMA.")
            break
        else:
            print("POR FAVOR, ENTRE UMA OPÇÃO VÁLIDA: 'd', 's' ou 'e'.")
    except ValueError as e:
        print("POR FAVOR, INSIRA UM VALOR VÁLIDO")
    except Exception as e:
        print(f"ERRO: {e}")
    finally:
        with open("saldos.json", "w") as file:
            dump(saldos, file)
        with open("saques.json", "w") as file:
            dump(saques, file)
        with open("depositos.json", "w") as file:
            dump(depositos, file)
