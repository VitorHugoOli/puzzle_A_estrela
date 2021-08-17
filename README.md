# Olá Alcione!

### Antes de realizar os primeiro teste no codigo, gostaria de informar que tomei a liberdade de realizar algumas pequenas mudançãs no codigos.

- **Classe Posicao**

  Foi adicionado os metodo toTuple e toString, para simplificar a usuabilidade da classe
  ```python
    def toTuple(self):
        return self.linha, self.coluna

    def __str__(self):
        return print(self.toTuple())
  ```

- **Classe QuebraCabecaImp**

  Foi modificado a classe getPos, pois antreriormente está funcionava apenas como um metodo statico agora ela posibilita chamar como metodo statico e regular.Além disso, realizei a
  correção da documentação do metodo de acordo com https://www.python.org/dev/peps/pep-0257/
  ```python
        def getPos(self, valor, tab=None):
        """
        Retorna a posicao de um valor em relacao a um array
        :param valor: integer 0>=valor<=7
        :param tab: inter[][] 
        :return: A posicao do valor recebido em relação a tabela.
        """
        if tab is None:
            tab = self.tab
        for i in range(0, 3):
            for j in range(0, 3):
                if tab[i][j] == valor:
                    return Posicao(i, j)
        return None
  ```

  Foi modificado a classe toString para dar uma aparencia mais legal a tabela de retorno
  ```python
    def toString(self):
        buf = '╔═══╦═══╦═══╗\n'
        for i in range(0, 3):
            buf += '║ '
            for j in range(0, 3):
                if self.tab[i][j] == QuebraCabeca.VAZIO:
                    buf = buf + '  ║ '
                else:
                    buf = buf + str(self.tab[i][j]) + ' ║ '
            buf = buf + ('\n╠═══╬═══╬═══╣\n' if i != 2 else '\n')
        buf += '╚═══╩═══╩═══╝\n'
        return buf
    ```


  
### Por fim, para melhor experiência recomendo que o programa seja executado em um terminal linux.



