import os
import funcoes as f

if __name__ == "__main__":
  #os.system("clear")
  funcao_objetivo = "1100x1 + 750x2"
  inequacoes = ["2x1 + 2x2 >= 16", "3x1 + x2 >= 12"]
  
  funcao_objetivo = "3x1 + 5x2"
  inequacoes = ["3x1 + 2x2 <= 18", "x1 <= 4", "x2 <= 6"]
  
  funcao_objetivo = "40x1 + 16x2"
  inequacoes = ["2x1 + x2 <= 6", "10x1 + 12x2 <= 60"]

  funcao_objetivo = "2x1 + x2"
  inequacoes = ["4x1 + 3x2 >= 6", "x1 + 2x2 <= 3"]

  '''
  funcao_objetivo =    "30x11 + 20x12 + 24x13 + 18x14"
  funcao_objetivo += "+ 12x21 + 36x22 + 30x23 + 24x24"
  funcao_objetivo += "+  8x31 + 15x32 + 25x33 + 20x34"
  
  inequacoes = ["10x11 + 10x21 + 10x31 = 50", 
                "10x12 + 10x22 + 10x32 = 80",
                "10x13 + 10x23 + 10x33 = 40",
                "10x14 + 10x24 + 10x34 = 100"]
  '''

  
  funcao_objetivo =  "7x11 + 8x12 + 4x13 + "
  funcao_objetivo += "5x21 + 6x22 + 3x23 + "
  funcao_objetivo += "6x31 + 5x32 + 4x33"
  
  inequacoes = ["x11 + x12 + x13 = 41", 
                "x21 + x22 + x23 = 80",
                "x31 + x32 + x33 = 105",

                "x11 + x21 + x31 = 41", 
                "x12 + x22 + x32 = 80",
                "x13 + x23 + x33 = 105"]
  

  
  # 2)
  funcao_objetivo =  "10x11 + 5x12 + 12x13 + 4x14 + "
  funcao_objetivo += "2x21 + 0x22 + x23 + 9x24 + "
  funcao_objetivo += "13x31 + 11x32 + 14x33 + 6x34"
  
  inequacoes = ["x11 + x12 + x13 + x14 = 40", 
                "x21 + x22 + x23 + x24 = 80",
                "x31 + x32 + x33 + x34 = 110",

                "x11 + x21 + x31 = 20", 
                "x12 + x22 + x32 = 30",
                "x13 + x23 + x33 = 100",
                "x14 + x24 + x34 = 80"]
  


  # exemplo de aula
  funcao_objetivo =  "1x11 + 2x12 + 3x13 + 4x14 + "
  funcao_objetivo += "4x21 + 3x22 + 2x23 + 4x24 + "
  funcao_objetivo += "0x31 + 2x32 + 2x33 + x34"
  
  inequacoes = ["x11 + x12 + x13 + x14 = 6", 
                "x21 + x22 + x23 + x24 = 8",
                "x31 + x32 + x33 + x34 = 10",

                "x11 + x21 + x31 = 4", 
                "x12 + x22 + x32 = 7",
                "x13 + x23 + x33 = 6",
                "x14 + x24 + x34 = 7"]
  


  funcao_objetivo =  "8x11 + 12x12 + 10x13 + "
  funcao_objetivo += "4x21 + 10x22 + 6x23 + "
  funcao_objetivo += "6x31 + 15x32 + 12x33"
  
  inequacoes = ["x11 + x12 + x13 = 50", 
                "x21 + x22 + x23 = 100",
                "x31 + x32 + x33 = 40",

                "x11 + x21 + x31 = 60", 
                "x12 + x22 + x32 = 70",
                "x13 + x23 + x33 = 30"]



  funcao_objetivo =  "8x11 + 12x12 + 10x13 + 0x14 + "
  funcao_objetivo += "4x21 + 10x22 + 6x23 + 0x24 + "
  funcao_objetivo += "6x31 + 15x32 + 12x33 + 0x34"
  
  inequacoes = ["x11 + x12 + x13 + x14 = 50", 
                "x21 + x22 + x23 + x24 = 100",
                "x31 + x32 + x33 + x34 = 40",

                "x11 + x21 + x31 = 60", 
                "x12 + x22 + x32 = 70",
                "x13 + x23 + x33 = 30",
                "x14 + x24 + x34 = 30"]

  f.resolver(inequacoes, funcao_objetivo)
