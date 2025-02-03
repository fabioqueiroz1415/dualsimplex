import re
import numpy as np
import tabulate as tb
import fractions as fc
from dsimplex import dual_simplex
from simplex import simplex

def get_sub(s):
  sub = ''.join([chr(0x2080 + int(c)) for c in str(s)])
  return sub

def print_tableau(tableau:list[list[int]], num_variaveis, linhas = None, colunas = None, elementos=None, cabecalhos=None):
  t = np.copy(tableau).tolist()
  cabecalho = [""] + ["x" + get_sub(v + 1) for v in range(num_variaveis)] + ["b"]
  cabecalho_esq    = ["eq. " + str(i + 1) for i in range(len(t) - 1)] + ["Z"]
  cabecalho_esq = [get_ansi(e, "1") for e in cabecalho_esq]
  cabecalho = [get_ansi(c, "1") for c in cabecalho]
  
  if linhas is not None:
    for linha in linhas:
      cabecalho_esq[linha] = get_ansi(cabecalho_esq[linha], "33")
      t[linha] = [get_ansi(str(e), "33") for e in t[linha]]
  
  if colunas is not None:  
    for coluna in colunas:
      if coluna >= 0:
        cabecalho[coluna + 1] = get_ansi(cabecalho[coluna + 1], "33")
      else:
        cabecalho[coluna] = get_ansi(cabecalho[coluna], "33")
      for i in range(len(t)):
        t[i][coluna] = get_ansi(str(t[i][coluna]), "33")
  
  if elementos is not None:
    for elemento in elementos:
      t[elemento[0]][elemento[1]] = get_ansi(str(t[elemento[0]][elemento[1]]), "1;33")
  
  if cabecalhos is not None:
    for i in range(len(cabecalhos)):
      cabecalho[cabecalhos[i]+1] = get_ansi(cabecalho[cabecalhos[i]+1], "1;33")
  
  for i in range(len(t)):
    t[i].insert(0, cabecalho_esq[i])
  
  for i in range(len(t)):
    for j in range(len(t[i])):
      t[i][j] = str(t[i][j])
  
  print(tb.tabulate(t, headers=cabecalho, tablefmt="github", colalign=("right" for _ in t[0])))
  print()

def get_ansi(a, comando):
  return f"\033[{comando}m{a}\033[0m"

def print_ansi(string, comando="1"):
  print(get_ansi(string, comando))

def zerar_todos_da_coluna(tableau, linha, coluna):
  print_ansi("4º passo - escalonamento.")
  print_ansi("4.1 - dividir a linha pivô pelo elemento pivô.", "1")
  print_tableau(tableau, linhas=[linha], elementos=[(linha, coluna)], num_variaveis=len(tableau[0]) - 1)
  print_ansi("...", "1")
  divisor = tableau[linha, coluna]
  for i in range(len(tableau[linha])):
    tableau[linha, i] = fc.Fraction(tableau[linha, i], divisor)
  print_tableau(tableau, linhas=[linha], elementos=[(linha, coluna)], num_variaveis=len(tableau[0]) - 1)
  
  print_ansi("4.2 - zerar todos os elementos da coluna pivô, exceto o elemento pivô.", "1")
  print_tableau(tableau, colunas=[coluna], elementos=[(linha, coluna)], num_variaveis=len(tableau[0]) - 1)
  
  for i in range(len(tableau)):
    if i != linha:
      tableau[i, :] =  - tableau[i, coluna] * tableau[linha, :] + tableau[i, :]
    
  print_ansi("...", "1")
  
  print_tableau(tableau, colunas=[coluna], elementos=[(linha, coluna)], num_variaveis=len(tableau[0]) - 1)

def get_var_ineqs(inequacoes):
  inequacoes = get_coef_e_var_ineqs(inequacoes)
  variaveis = set()
  for inequacao in inequacoes:
    for _, var in inequacao:
      variaveis.add(var)
  return sorted(list(variaveis))

def is_inequacao(s):
  exp_ineq = r"^(-?\d*)?\s*x\d+\s*([+-]\s*\d*\s*x\d+\s*)*(<=|>=|=)\s*-?\s*(\d+)$"
  return re.match(exp_ineq, s)

def is_funcao_objetivo(s):
  exp_funcao_objetivo = r"^(-?\d*)?\s*x\d+\s*([+-]\s*\d*\s*x\d+\s*)*$"
  return re.match(exp_funcao_objetivo, s)

def get_coef_e_var_ineqs(inequacoes, res=False): # ((coef, var),)
  exp_reg_var_encontradas = []
  exp_reg_var = re.compile(r"(-?\d*)?x(\d+)")
  for inequacao in inequacoes:
    i = inequacao.replace(" ", "")
    exp_reg_var_encontradas.append(exp_reg_var.findall(i))
  for i, variaveis_inequacao in enumerate(exp_reg_var_encontradas):
    for j, variavel in enumerate(variaveis_inequacao):
      if variavel[0] == "":
        exp_reg_var_encontradas[i][j] = (fc.Fraction(1, 1), int(variavel[1]))
      elif variavel[0] == "-":
        exp_reg_var_encontradas[i][j] = (fc.Fraction(-1, 1), int(variavel[1]))
      else:
        exp_reg_var_encontradas[i][j] = (fc.Fraction(int(variavel[0]), 1), int(variavel[1]))
        
    if res:
      exp_reg_res = re.compile(r"(-?)\s*(\d+)$")
      sinal, valor = exp_reg_res.findall(inequacoes[i])[0]
      exp_reg_var_encontradas[i] += [f"{sinal}{valor}"] # add ultima coluna
      exp_reg_var_encontradas[i][-1] = int(exp_reg_var_encontradas[i][-1])
  return exp_reg_var_encontradas

def get_coef_ineq(inequacoes):
  variaveis = get_var_ineqs(inequacoes)
  coef_e_var_ineq = get_coef_e_var_ineqs(inequacoes)
  coeficientes_list = []
  for inequacao in coef_e_var_ineq:
    coeficientes_dict = {var: fc.Fraction(0, 1) for var in variaveis}
    for coef, var in inequacao:
      coeficientes_dict[var] = coef
    
    coeficientes_list.append([coeficientes_dict[var] for var in variaveis])
  
  return coeficientes_list

def get_tableau(inequacoes, funcao_objetivo):
  coeficientes = get_coef_ineq(inequacoes)
  resultados = [ineq[-1] for ineq in get_coef_e_var_ineqs(inequacoes, res=True)]
  
  num_variaveis = len(get_var_ineqs(inequacoes))
  num_folgas = len(inequacoes)
  tableau = []
  for i in range(len(coeficientes)):
    linha = coeficientes[i] + [fc.Fraction(0, 1)] * i + [fc.Fraction(1, 1)] + [fc.Fraction(0, 1)] * (num_folgas - i - 1) + [fc.Fraction(resultados[i], 1)]
    tableau.append(linha)

  funcao_objetivo_formatada = get_coef_e_var_ineqs([funcao_objetivo])[0]
  funcao_objetivo_transformada = [-coef for coef, _ in funcao_objetivo_formatada] + [fc.Fraction(0, 1)] * num_folgas + [fc.Fraction(0, 1)]
  tableau.append(funcao_objetivo_transformada)

  return np.array(tableau), num_variaveis, num_folgas

def get_re_sub(match):
  return f"x{get_sub(match.group(1))}"

def get_ineq_formatada(i):
  i = i.replace(" ", "").replace("+", get_ansi("+", "1;32")).replace("-", get_ansi("-", "1;32")).replace("<=", get_ansi(" ≤ ", "1;32")).replace(">=", get_ansi(" ≥ ", "1;32")).replace("=", get_ansi(" = ", "1;32"))
  i = re.sub(r'x(\d+)', get_re_sub, i)
  return i

def len_ineq_formatada(i):
  return len(i.replace(" ", "").replace("+", "+").replace("-", "-").replace("<=", "≤").replace(">=", "≥").replace("=", "="))

def resolver(inequacoes, funcao_objetivo):
  for ineq in inequacoes:
    if re.search(r">=|(?<![><])=", ineq):
      print("esse problema é de minização ou maximização?\n")
      print(f"1. Minimização.")
      print(f"2. Maximização.")
      print()
      print(">: ", end="")
      e = input()
      while e not in ["1", "2"]:
        e = input(">: ")
      isMax = True if e == "2" else False
      return dual_simplex(inequacoes, funcao_objetivo, isMax)
  return simplex(inequacoes, funcao_objetivo)
