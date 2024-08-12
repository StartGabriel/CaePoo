from basico.input import Input
import pygame
import sys
import bdpython
import bdpython.user
import re
import funcionais.aviso
import sqlite3
import usuario

pygame.init()

class Incluir:
    def __init__(self,
                 menu,
                 size_button: list[int],
                 coordinates_button: list[int],
                 color_button: str,
                 color_title: str):
        self.menu = menu
        self.size = size_button
        self.coordinates = coordinates_button
        self.backups = menu.copy()
        self.color = color_button
        self.color_title = color_title
        self.retorna = []

    def user(self):
        self.nome = Input(window=self.menu,
                          size=self.size,
                          coordinates=self.coordinates,
                          title="nome",
                          color=self.color,
                          color_title=self.color_title)
        self.idade = Input(window=self.menu,
                           size=self.size,
                           coordinates=self.coordinates,
                           title="idade",
                           color=self.color,
                           color_title=self.color_title)
        
        self.email = Input(window=self.menu,
                           size=self.size,
                           coordinates=self.coordinates,
                           title="email",
                           color=self.color,
                           color_title=self.color_title)
        self.inputs = [self.nome, self.idade, self.email]
        self.loop()

    def loop(self):
        for inp in self.inputs:
            inp.pack()
            self.loops = True
            while self.loops:
                for events in pygame.event.get():
                    if events.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if events.type == pygame.MOUSEBUTTONDOWN:
                        self.pos = pygame.mouse.get_pos()
                        self.retorna.append(inp.run(self.pos))
                        inp.clear_window()
                        self.loops = False
                pygame.display.flip()

        # Tentar incluir os dados no banco
        try:
            self.incluir(nome=self.retorna[0], idade=self.retorna[1], email=self.retorna[2])
            print(self.retorna)
        except Exception as e:
            print(f"Erro inesperado durante a inclusão: {e}")
            # Opcionalmente, pode-se exibir um aviso ao usuário
            self.erro = funcionais.aviso.Avisos(size_button=[300, 50],
                                                coordinates_button=self.coordinates,
                                                title_button="Erro durante inclusão",
                                                color_button="black",
                                                color_title="yellow")
            self.erro.mensagem(f"Erro durante a inclusão: {str(e)}")

    def incluir(self, nome: str, idade: int, email: str, bd="bdpython/user.db"):
        try:
            nome = self.tratar_entrada(nome)
            cnn = bdpython.user.conectar(bd)
            bdpython.user.criar_tabela(cnn)
            bdpython.user.inserir_user(cnn, nome=nome, idade=idade, email=email)
            
        except Exception as e:
            print(f"Erro inesperado: {e}")
            self.erro = funcionais.aviso.Avisos(size_button=[300, 50],
                                                coordinates_button=self.coordinates,
                                                title_button="Erro",
                                                color_button="black",
                                                color_title="red")
            self.erro.mensagem(f"Erro inesperado: {str(e)}",
                               size_text_message=30,color="yellow")
        

    def tratar_entrada(self, entrada):
        try:
            tratado = re.sub(r'[^a-zA-Z\s]', '', entrada)
            print(tratado)
            return tratado
        except Exception as e:
            print(f"Erro ao tratar entrada: {e}")
            raise  # Relevanta a exceção após o log para que ela possa ser capturada na chamada
