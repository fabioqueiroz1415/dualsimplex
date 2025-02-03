import funcoes as f
import os
import numpy as np
import fractions as fc

def get_pivo(tableau):
  coluna_pivo = np.argmin(tableau[-1, :-1])
  if tableau[-1, coluna_pivo] >= 0:
    return None, None

  f.print_ansi("2.1 - escolher coluna com menor valor em Z.")
  f.print_tableau(tableau, linhas=[-1], num_variaveis=len(tableau[0]) - 1)
  f.print_ansi("...")
  f.print_tableau(tableau, elementos=[(-1, coluna_pivo)], num_variaveis=len(tableau[0]) - 1)
  f.print_ansi("...")
  f.print_tableau(tableau, colunas=[coluna_pivo], num_variaveis=len(tableau[0]) - 1)
  
  f.print_ansi("3º passo - linha pivô.", "1")
  f.print_ansi("3.1 - dividir o respectivo elemento da coluna b por cada elemento da coluna pivô maior que 0, exceto na linha Z.", "1")
  f.print_tableau(tableau, colunas=[-1, coluna_pivo], num_variaveis=len(tableau[0]) - 1)
  
  linhas_candidatas = []
  for i in range(len(tableau) - 1):
    if tableau[i, coluna_pivo] > 0:
      linhas_candidatas.append((tableau[i, -1] / tableau[i, coluna_pivo], i))

  if not linhas_candidatas:
    raise ValueError("esse problema não tem solução")

  linha_pivo = min(linhas_candidatas, key=lambda x: x[0])[1]
  
  f.print_ansi("3.2 - escolher linha que obteve o menor resultado.", "1")
  f.print_tableau(tableau, elementos=[(linha_pivo, coluna_pivo), (linha_pivo, -1)], colunas=[coluna_pivo], num_variaveis=len(tableau[0]) - 1)
  f.print_ansi("...")
  f.print_tableau(tableau, linhas=[linha_pivo], colunas=[coluna_pivo], elementos=[(linha_pivo, coluna_pivo)], num_variaveis=len(tableau[0]) - 1)
  
  f.print_ansi("3.3 - o pivô é o encontro entre linha pivô e coluna pivô..")
  f.print_tableau(tableau, elementos=[(linha_pivo, coluna_pivo)], num_variaveis=len(tableau[0]) - 1)
  return linha_pivo, coluna_pivo

def simplex(inequacoes, funcao_objetivo):
  tableau, num_variaveis, num_folgas = f.get_tableau(inequacoes, funcao_objetivo)
  
  print(f"{f.get_ansi("MAX Z = ", "1")}{f.get_ineq_formatada(funcao_objetivo)}\n")
  f.print_ansi("sujeito a:")
  for inequacao in inequacoes:
    print(f"           {f.get_ineq_formatada(inequacao)}")
  print()
  
  f.print_ansi("1º passo - tableau inicial: inserir uma variável de folga para cada equação.")
  f.print_tableau(tableau,
                  num_variaveis + num_folgas,
                  colunas=[i for i in range(num_variaveis, num_variaveis + num_folgas, 1)])
  
  is_primeiro = True
  while True:
    f.print_ansi(f"{f.get_ansi("(LOOP1) ", "1;32") if is_primeiro else f.get_ansi("(VOLTA LOOP1) ", "1;32")}2º passo - coluna pivô.", "1")
    is_primeiro = False
    linha_pivo, coluna_pivo = get_pivo(tableau)
    if linha_pivo is None:
      break
    f.zerar_todos_da_coluna(tableau, linha_pivo, coluna_pivo)
  print( f"{f.get_ansi("(FIM LOOP1)", "1;32")}: não há mais valores negativos em {f.get_ansi("Z", "1")}.")
  print()
  f.print_ansi("5º passo - as variáveis que possuem em sua coluna um \"1\" e \"0\" no restante,")
  f.print_ansi("possuem o respectivo valor na coluna b onde o \"1\" está.")
  f.print_ansi("o restante possui valor 0.")
  f.print_ansi(f"o valor ótimo é o valor de {f.get_ansi("Z", "1")} na última linha e última coluna.")
  
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
  print("Valor ótimo:", tableau[-1, -1])
  return None

if __name__ == "__main__":
  os.system("cls")
  
  inequacoes = ["10x1 + 12x2 <= 60", "2x1 + x2 <= 6"]
  funcao_objetivo = "40x1 + 16x2"
  
  simplex(inequacoes, funcao_objetivo)
