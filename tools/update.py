import os
import sys
from time import sleep

# Removi o ZipFile e requests da parte de execução porque não vamos mais baixar nada
import requests 

class Update():
    def __init__(self):
        # Mantemos a versão para não quebrar referências, se houver
        self.version = '1.5.8'
        self.update_checker()

    def update_checker(self):
        # Simulamos que a checagem foi feita e está tudo ok
        print('Modo de Estudo Ativo: Ignorando atualizações...')
        sleep(1)
        print('Esta versao (1.5.8) sera tratada como atualizada.')
        sleep(1)
        
        # O script original diz que você deve abrir o builder.pyw
        print('\n[SUCESSO] Voce ja pode abrir o arquivo "builder.pyw" para estudar o construtor!')
        sleep(1)
        print('Encerrando o verificador em 3 segundos...')
        sleep(3)
        sys.exit()

if __name__ == '__main__':
    Update()