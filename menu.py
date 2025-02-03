import os
import funcoes as f

inequacoes = []
is_opcoes = [False        , False         , False           , False]
#            add func obj  add inequação    ver inequações    ver solução
funcao_objetivo = ""

def menu_add_inequacao():
  titulo("Adicionar Inequação")
  print("Digite a inequação no formato: x1 + x2 <= / = / >= 10, ENTER para voltar")
  print(">: ", end="")
  i = input()
  if i == "":
    os.system("cls")
    return
  elif f.is_inequacao(i):
    inequacoes.append(i)
    is_opcoes[1] = True
    if is_opcoes[0]:
      is_opcoes[2] = True
      is_opcoes[3] = True
    os.system("cls")
    print("Inequação adicionada com sucesso.\n")
    titulo("")
    return menu_add_inequacao()
  else:
    print("Inequação incorreta, digite novamente.")
    return menu_add_inequacao()

def menu_add_funcao_objetivo():
  global funcao_objetivo
  titulo("Adicionar/editar Função Objetivo")
  if funcao_objetivo != "":
    print(f"Função objetivo atual: {funcao_objetivo}")
  else:
    print("Digite a função objetivo no formato: 3x1 + 2x2 + x3, ENTER para voltar")
  print()
  print(">: ", end="")
  f = input()
  if f == "":
    os.system("cls")
    return
  elif f.is_funcao_objetivo(f):
    funcao_objetivo = f
    is_opcoes[0] = True
    os.system("cls")
    is_opcoes[0] = True
    if is_opcoes[1]:
      is_opcoes[2] = True
      is_opcoes[3] = True
    print("Função objetivo adicionada com sucesso.\n")
    titulo("")
    return menu_add_funcao_objetivo()
  else:
    os.system("cls")
    print("Função objetivo incorreta, digite novamente.")
    return menu_add_funcao_objetivo()

def menu_ver_inequacoes():
  titulo("Inequações")
  for i, inequacao in enumerate(inequacoes):
    print(f"{i + 1}. {inequacao}")
  titulo("")
  return

def menu_ver_solucao():
  titulo("Solução")
  f.resolver(inequacoes, funcao_objetivo)
  titulo("")
  return

def menu_principal():
  titulo("Menu Principal")
  opcoes    = ["add/editar função objetivo", "add inequação", "ver inequações", "ver solução"]
  
  for i, opcao in enumerate(opcoes[:2]):
    print(f"{i + 1}. {opcao}")
  
  for j, opcao in enumerate(opcoes[2:], start=2):
    if is_opcoes[j]:
      print(f"{j + 1}. {opcao}")
  print("0. Sair")
  titulo("")
  print(">: ", end="")
  e = input()
  if e == "1":
    os.system("cls")
    menu_add_funcao_objetivo()
    return menu_principal()
  elif e == "2":
    if not is_opcoes[0]:
      print("Opção inválida")
      return menu_principal()
    os.system("cls")
    menu_add_inequacao()
    return menu_principal()
  elif e == "3":
    if not is_opcoes[1]:
      print("Opção inválida")
      return menu_principal()
    os.system("cls")
    menu_ver_inequacoes()
    return menu_principal()
  elif e == "4":
    if not is_opcoes[2]:
      print("Opção inválida")
      return menu_principal()
    os.system("cls")
    menu_ver_solucao()
    return menu_principal()
  elif e == "0":
    os.system("cls")
    return
  else:
    os.system("cls")
    print("Opção inválida")
    return menu_principal()

def titulo(s):
  quantitidade_ifens = (50 - len(s)) // 2
  print(f"{'-' * quantitidade_ifens} {s} {'-' * quantitidade_ifens}")

if __name__ == "__main__":
  os.system("cls")
  menu_principal()
