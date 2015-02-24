from math import sqrt
class tabuleiro(object):
    def __init__(self, tab, posicoes_vazias = None):
        self.tab = tab
        
        if posicoes_vazias is None:
            self.posicoes_vazias = self._posicoes_vazias()
            for l, c in self.posicoes_vazias:
                if not self.num_na_pos(l, c):
                    self.tab[l][c] = self.nums_possiveis_posicao(l, c)
        else:
            self.posicoes_vazias = posicoes_vazias
                        
    @classmethod
    def tabuleiro_vazio(self, num_col, def_valor):
        return tabuleiro([[def_valor] * num_col] * num_col)
        
    @classmethod  
    def ler_tab(self,ficheiro):
        tab = open(ficheiro)
        aux = []
        for linha in tab:
            linha_aux = linha.split()
            linha_inteiros = [int(x) for x in linha_aux]
            aux.append(linha_inteiros)        
        return tabuleiro(aux[1:])
        
    def tabuleiro_valido(self):
        if int(sqrt(self.tab_dim())) % 2 == 0:
            for i in self.tab:
                if isinstance(i, list) and len(i) == self.tab_dim():
                    for x in i:
                        if isinstance(x, int) and x >= 0 and x <= self.tab_dim():
                            pass
                        else:
                            return False
                else:
                    return False
            return True
        return False
    
    
    def _posicoes_vazias(self):
        posicoes_vazias = []
        for i in range(0,self.tab_dim() ):
            for d in range(0,self.tab_dim() ):
                aux = self.num_na_pos(i, d)
                if isinstance(aux,list) or aux == 0:
                    posicoes_vazias.append((i,d))
        return posicoes_vazias    

    def __str__(self):
        tab_copia = [[i if not isinstance(i, list) else list(i) for i in x] \
                                                            for x in self.tab]
        len_tab = len(tab_copia)
        num_grupos = int(sqrt(len_tab))     
        indices = range(num_grupos - 1,len_tab -1, num_grupos)
        aux = range(1,num_grupos) 

        #por os zeros                                                    
        for i in range(0,len_tab):
            for j in range(0,len_tab):
                if len_tab > 9:
                    if isinstance(tab_copia[i][j],list):
                        tab_copia[i][j] = ' 0'
                    else:
                        if tab_copia[i][j] < 10:
                            tab_copia[i][j] = ' ' +str(tab_copia[i][j])
                        else:
                            tab_copia[i][j] = str(tab_copia[i][j])                                
                else:
                    if isinstance(tab_copia[i][j],list):
                        tab_copia[i][j] = str(0)
                    else:
                        tab_copia[i][j] = str(tab_copia[i][j])
                               
        #por as barras
        for i in range(0, len_tab):
            for j,x in zip(indices,aux):
                tab_copia[i].insert(j+x,'|')
        
        #por as barras horizontais
        b = []
        if len_tab > 9:
            num_abaixo_de_10 = 9
            for i in range((len(tab_copia[0]) + num_abaixo_de_10)-1):
                b.append('-')
        else:
            for i in range((len(tab_copia[0]))):
                b.append('-')
        for i,j in zip(indices,aux):
            tab_copia.insert(i+j,b)        
        
        #imprimir tabuleiro    
        tabu = ''
        for linha in tab_copia:
            for num in linha:
                tabu += num + ' '
            tabu += '\n'
        return tabu
    
    
    def num_na_pos(self, num_linha, num_col):
        return self.tab[num_linha][num_col]
    
    def tab_dim(self):
        return len(self.tab)
    
    def posicoes_col(self,num_col):
        posicoes = []
        for indice in range(0,self.tab_dim()):
            posicoes.append((indice,num_col))
        return posicoes

    def nums_possiveis_col(self, num_col):
        todos_nums_possiveis = range(1,self.tab_dim() +1)
        for pos in self.posicoes_col(num_col):
            num = self.num_na_pos(pos[0],pos[1])
            if not isinstance(num, list) and num in todos_nums_possiveis:
                todos_nums_possiveis.remove(num)
        return todos_nums_possiveis    
    
    def posicoes_linha(self, num_linha):
      posicoes = []
      for indice in range(0,self.tab_dim()):
          posicoes.append((num_linha, indice))
      return posicoes            
    
    def nums_possiveis_linha(self, num_linha):
        todos_nums_possiveis = range(1,self.tab_dim() +1)
        for pos in self.posicoes_linha(num_linha):
            num = self.num_na_pos(pos[0],pos[1])
            if not isinstance(num, list) and num in todos_nums_possiveis:
                todos_nums_possiveis.remove(num)
        return todos_nums_possiveis     
       
    def posicoes_grupo(self, num_linha, num_col):
        grupo_linha = num_linha / int(sqrt(self.tab_dim())) 
        grupo_col = num_col / int(sqrt(self.tab_dim())) 
        posicoes = []
        for i in range(0, int(sqrt(self.tab_dim())) ):
            for d in range(0,int(sqrt(self.tab_dim())) ):
                x = (grupo_linha * int(sqrt(self.tab_dim())) ) + i
                y = (grupo_col * int(sqrt(self.tab_dim())) ) + d
                posicoes.append((x, y))
        return posicoes
             
    def nums_possiveis_grupo(self,num_linha, num_col):        
        todos_nums_possiveis = range(1,self.tab_dim() +1)
        for pos in self.posicoes_grupo(num_linha, num_col):
            num = self.num_na_pos(pos[0],pos[1])
            if not isinstance(num, list) and num in todos_nums_possiveis:
                todos_nums_possiveis.remove(num)
        return todos_nums_possiveis     
    
    def nums_possiveis_posicao(self,num_linha, num_col):
        nums_possiveis_linha = self.nums_possiveis_linha(num_linha)
        nums_possiveis_col = self.nums_possiveis_col(num_col)
        nums_possiveis_grupo = self.nums_possiveis_grupo(num_linha, num_col)
        
        nums_possiveis_linha_e_col = set(nums_possiveis_linha).intersection(nums_possiveis_col)
        return list(nums_possiveis_linha_e_col.intersection(nums_possiveis_grupo))
       
    def poe_num(self, valor, num_linha, num_col, copy_tab=True):
        if copy_tab:
            novo_tab = [[i if not isinstance(i, list) else list(i) for i in x] for x in self.tab]
            posicoes_vazias = [p for p in self.posicoes_vazias if p != (num_linha, num_col)]
            novo_tab[num_linha][num_col] = valor
            t = tabuleiro(novo_tab, posicoes_vazias)
        else:
            self.tab[num_linha][num_col] = valor
            self.posicoes_vazias.remove((num_linha, num_col))
            t = self

        return t.propagar_restricoes(valor, num_linha, num_col)
        
        
    def propagar_restricoes(self, valor, num_linha, num_col):
        for pos in self.posicoes_col(num_col) + \
                self.posicoes_grupo(num_linha, num_col) + \
                self.posicoes_linha(num_linha):
            valor_na_pos = self.num_na_pos(*pos)
            posicoes_um_numero = []
            if isinstance(valor_na_pos, list):
                if valor in valor_na_pos:
                    valor_na_pos.remove(valor) 
                    if len(valor_na_pos) == 0:
                        return None
                    if len(valor_na_pos) == 1:
                        posicoes_um_numero.append(pos)
        for pos in posicoes_um_numero:
            if not self.poe_num(self.num_na_pos(*pos)[0], *pos, copy_tab=False):
                return None
        return self    

    def resolver(self):        
        if not self.posicoes_vazias:
            return self
                    
        posicao_menos_hipoteses = min(self.posicoes_vazias,
            key=lambda posicao_vazia: len(self.num_na_pos(*posicao_vazia)))
        
        hipoteses = self.num_na_pos(*posicao_menos_hipoteses)
        
        if not hipoteses:
            return None
            
        for hipotese in hipoteses:
            novo_tab = self.poe_num(hipotese, *posicao_menos_hipoteses)
            
            if not novo_tab:
                continue
            
            tabuleiro_resolvido = novo_tab.resolver()
            
            if tabuleiro_resolvido:
                return tabuleiro_resolvido
                    

d = tabuleiro.ler_tab('boards/9-1.sudoku')
print d.resolver()
