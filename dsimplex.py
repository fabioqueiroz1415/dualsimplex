import funcoes as f
import re
import os
import fractions as fc
import numpy as np

def dual_get_pivo(tableau, isMax=False):
  linha_pivo = np.argmin(tableau[:-1, -1])
  if tableau[linha_pivo, -1] >= fc.Fraction(0, 1):
    return None, None
  
  f.print_ansi("2.1 - escolher linha com menor valor em b.")
  f.print_tableau(tableau, colunas=[-1], num_variaveis=len(tableau[0]) - 1)
  f.print_ansi("...")
  f.print_tableau(tableau, elementos=[(linha_pivo, -1)], num_variaveis=len(tableau[0]) - 1)
  f.print_ansi("...")
  f.print_tableau(tableau, linhas=[linha_pivo], num_variaveis=len(tableau[0]) - 1)

  f.print_ansi("3º passo - coluna pivô.", "1")
  f.print_ansi("3.1 - dividir os coeficientes da linha Z pelos respectivos coeficientes da linha pivô negativos.", "1")
  f.print_tableau(tableau, linhas=[linha_pivo, -1], num_variaveis=len(tableau[0]) - 1)
  f.print_ansi("...")
  f.print_tableau(tableau,
                elementos=[(linha_pivo, j) for j, elem in enumerate(tableau[linha_pivo][:-1]) if elem < 0] + 
                          [(-1, j) for j, elem in enumerate(tableau[linha_pivo][:-1]) if elem < 0],
                num_variaveis=len(tableau[0]) - 1)

  colunas_candidatas = []
  for j in range(len(tableau[linha_pivo]) - 1):
    if tableau[linha_pivo, j] < 0:
      colunas_candidatas.append((fc.Fraction(tableau[-1, j], tableau[linha_pivo, j]), j))

  if not colunas_candidatas:
    raise ValueError("Esse problema não tem solução viável.")

  if isMax:
    coluna_pivo = min(colunas_candidatas, key=lambda x: abs(x[0]))[1]
  else:
    coluna_pivo = min(colunas_candidatas, key=lambda x: x[0])[1]
  
  f.print_ansi(f"3.2 - ({"MAX" if isMax else "MIN"}) escolher coluna que obteve o menor valor {"absoluto" if isMax else ""} entre os quocientes encontrados.", "1")
  f.print_tableau(tableau,
                elementos=[(linha_pivo, coluna_pivo), (-1, coluna_pivo)],
                colunas=[coluna_pivo],
                num_variaveis=len(tableau[0]) - 1)
  f.print_ansi("3.3 - o pivô é o encontro entre linha pivô e coluna pivô.")
  f.print_tableau(tableau, linhas=[linha_pivo], colunas=[coluna_pivo], elementos=[(linha_pivo, coluna_pivo)], num_variaveis=len(tableau[0]) - 1)
  f.print_ansi("...")
  f.print_tableau(tableau, elementos=[(linha_pivo, coluna_pivo)], num_variaveis=len(tableau[0]) - 1)
  
  return linha_pivo, coluna_pivo

def converter_ineqs_para_menor_igual(inequacoes: list, funcao_objetivo, isMax, rec=False):
  if not rec:
    f.print_ansi("passo 0 - converter inequações para <=.\n")
  i = -1
  while (i + 1 < len(inequacoes)):
    i += 1
    inequacoes[i] = inequacoes[i].replace(" ", "")

    if ">=" in inequacoes[i]:
      if not rec:
        print(f"{f.get_ineq_formatada(inequacoes[i])}    --->    ", end="")
      if inequacoes[i][0] not in ["-", "+"]:
        inequacoes[i] = "+" + inequacoes[i]
      
      if not re.search(r">=[+-]", inequacoes[i]):
        inequacoes[i] = inequacoes[i].replace(">=", ">=+")
      inequacao = ""
      for j in inequacoes[i]:
        if j == "-":
          inequacao += "+"
        elif j == "+":
          inequacao += "-"
        else:
          inequacao += j
      inequacoes[i] = inequacao.replace(">=", "<=")
      if not rec:
        print(f.get_ineq_formatada(inequacoes[i]))
        print()
    elif "<=" in inequacoes[i]:
      continue
    elif "=" in inequacoes[i]:
      inequacoes2 = [inequacoes[i].replace("=", "<="), inequacoes[i].replace("=", ">=")]
      
      print(f"{' ' * f.len_ineq_formatada(inequacoes[i])}   |--->    {f.get_ineq_formatada(inequacoes2[0])}")
      print(f"{f.get_ineq_formatada(inequacoes[i])} --|")
      
      print(f"{' ' * f.len_ineq_formatada(inequacoes[i])}   |--->    {f.get_ineq_formatada(inequacoes2[1])}", end='')
      
      inequacoes2 = converter_ineqs_para_menor_igual(inequacoes2, funcao_objetivo, isMax, rec=True)
      
      print(f"    --->    {f.get_ineq_formatada(inequacoes2[1])}")
      print()
      
      inequacoes = inequacoes[:i] + inequacoes2 + inequacoes[i + 1:]
      i += len(inequacoes2) - 1

  if not rec:
    f.print_ansi("...", "1")
    print(f"{f.get_ansi(f"{"MAX" if isMax else "MIN"} Z = ", "1")}{f.get_ineq_formatada(funcao_objetivo)}\n")
    f.print_ansi("sujeito a:")
    for inequacao in inequacoes:
      print(f"           {f.get_ineq_formatada(inequacao)}")
    print()
  
  return inequacoes

def dual_simplex(inequacoes, funcao_objetivo, isMax=False):
  print(f"{f.get_ansi(f"{"MAX" if isMax else "MIN"} Z = ", "1")}{f.get_ineq_formatada(funcao_objetivo)}\n")
  f.print_ansi("sujeito a:")
  for inequacao in inequacoes:
    print(f"           {f.get_ineq_formatada(inequacao)}")
  print()
  inequacoes = converter_ineqs_para_menor_igual(inequacoes, funcao_objetivo, isMax)
  tableau, num_variaveis, num_folgas = f.get_tableau(inequacoes, funcao_objetivo)
  f.print_ansi("1º passo - tableau inicial: inserir uma variável de folga para cada equação.")
  f.print_tableau(tableau,
                  num_variaveis + num_folgas,
                  colunas=[i for i in range(num_variaveis, num_variaveis + num_folgas, 1)])
  is_primeiro = True
  
  while True:
    print(f"{f.get_ansi("(LOOP1) ", "1;32") if is_primeiro else f.get_ansi("(VOLTA LOOP1) ", "1;32")}{f.get_ansi("2º passo - linha pivô.", "1")}")
    is_primeiro = False
    linha_pivo, coluna_pivo = dual_get_pivo(tableau, isMax)
    if linha_pivo is None:
      break
    f.zerar_todos_da_coluna(tableau, linha_pivo, coluna_pivo)

  f.print_ansi("(FIM LOOP1) não há mais valores negativos em b.", "1;32")
  print()
  f.print_ansi("5º passo - as variáveis que possuem em sua coluna um \"1\" e \"0\" no restante,")
  f.print_ansi("possuem o respectivo valor na coluna b onde o \"1\" está.")
  f.print_ansi("o restante possui valor 0.")
  print(f"o valor ótimo é o valor de {f.get_ansi("Z", "1")}, na última linha e última coluna.")

  solucao = [str(fc.Fraction(0, 1))] * num_variaveis
  vb = []
  for c in range(num_variaveis):
    coluna = tableau[:, c]
    if np.sum(coluna) == 1 and np.sum(coluna == 0) == len(coluna) - 1:
      linha = np.argmax(coluna)
      vb.append((linha, c))
      solucao[c] = tableau[linha, -1]
  print()
  f.print_tableau(tableau, colunas=[i[1] for i in vb], num_variaveis = num_variaveis + num_folgas)
  f.print_ansi("...")
  f.print_tableau(tableau, linhas=[var[0] for var in vb], colunas=[i[1] for i in vb], elementos=[(var[0], -1) for var in vb], num_variaveis = num_variaveis + num_folgas)
  f.print_ansi("...")
  f.print_tableau(tableau, elementos=[(var[0], -1) for var in vb]+[(-1, -1)], cabecalhos=[var[1] for var in vb], num_variaveis = num_variaveis + num_folgas)

  var = f.get_var_ineqs(inequacoes)
  print("Solução ótima:")
  for v, s in zip(var, solucao):
    print(f"x{f.get_sub(v)} = {s}")
  print(f"Valor ótimo {f.get_ansi(f"({"MAX" if isMax else "MIN"})", "1")}:", tableau[-1, -1])

  return solucao, tableau[-1, -1]


if __name__ == "__main__":
  os.system("cls")
  funcao_objetivo = "2x1 + x2"
  inequacoes = ["4x1 + 3x2 >= 6","x1 + 2x2 <= 3"]
  
  funcao_objetivo = "x1 + 2x2"
  inequacoes = ["3x1 + x2 <= 12", "5x1 - 5x2 >= 10"]
  
  funcao_objetivo = "3x1 + 2x2"
  inequacoes = ["2x1 + x2 <= 8", "x1 + 3x2 = 9"]
  
  funcao_objetivo = "10x1 + 12x2 + 6x3"
  inequacoes = ["2x1 + x2 + x3 >= 20", "3x1 + 3x2 + 2x3 >= 30"]
  
  funcao_objetivo = "x1 + x2 + x3"
  inequacoes = ["2x1 + x2 - x3 <= 10", "x1 + x2 + 2x3 >= 20", "2x1 + x2 + 3x3 = 60"]
  
  dual_simplex(inequacoes, funcao_objetivo, isMax=True)
