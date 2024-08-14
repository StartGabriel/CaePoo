from basico.input import Input
import pygame
import sys
import bdpython
import bdpython.user
import re
import funcionais.aviso
import sqlite3
import usuario
from basico.button import Button
import basico.button as button
import basico.tools as tools
from basico.window import Window
import funcionais.aviso as aviso


pygame.init()

class Alterar:
    def __init__(self):
        self.menu = Window(size=[1000, 600], color="black", background="images/pantano.jpg").pack() #esse é o menu <-
        self.backups = self.menu.copy()
        self.menu_size = [1000,600]
        self.color_inputs = "black"
        self.color_inputs_title= "white"
        self.coordinate_inputs = [0,0]
        self.loops = True
        self.db_path = "bdpython/user.db"
        self.nome = None
        self.idade = None
        self.email = None
        self.verify = False
        

    def user(self):
        self.title_window = tools.insert_text(text="ALTERAR DADOS",
                                              color="white",
                                              size= 50,
                                              background_color="black")
        self.mid_title = tools.get_obj_center([1000,600],self.title_window.get_size())
        self.menu.blit(self.title_window,(self.mid_title[0],10))
        self.backups2 = self.menu.copy()
        self.mid_id = tools.get_obj_center(self.menu_size,[300,50])
        self.id = Input(window=self.menu,
                          size=[300,50],
                          coordinates=self.mid_id,
                          title="ID",
                          color="white",
                          color_title="black")
        
        self.id.pack()
        self.alterando = self.id
        self.user_id = self.coletar()
        try:
            self.conn = bdpython.user.conectar(self.db_path)
            user_data = bdpython.user.consultar_user(self.conn, self.user_id)
            if not user_data:
                self.nao_encontrado = aviso.Avisos([300, 50], [275, 0], "AVISO!", "black", "white")
                self.nao_encontrado.mensagem(f"'{self.user_id}' User não encontrado")
                return

            self.user_name = user_data[1]
            self.menu.blit(self.backups2,(0,0))
            
            self.botoes()
            self.confirmar()
            if self.verify == True:
                self.atualizar(cnn=self.conn,nome=self.nome, idade=self.idade,email= self.email)
        except:
            pass
        
        
    def botoes(self):
        self.mid = tools.get_obj_center(coordinate_size=[1000,600],size_objt=[300,50])
        self.but_nome = Button(window=self.menu,
                               title="NOME",
                               size=[300,50],
                               color= "red",
                               coordinates=[0,0],
                               command=self.alterar_nome)
        self.but_idade = Button(window=self.menu,
                               title="IDADE",
                               size=[300,50],
                               color= "red",
                               coordinates=[0,0],
                               command=self.alterar_idade)
        self.but_email = Button(window=self.menu,
                               title="E-MAIL",
                               size=[300,50],
                               color= "red",
                               coordinates=[0,0],
                               command=self.alterar_email)
        self.but_sair = Button(window=self.menu,
                               title="SAIR",
                               size=[300,50],
                               color="green",
                               coordinates=[0,0],
                               command=self.sair)
        
        self.buts = [self.but_nome, self.but_idade, self.but_email, self.but_sair]
        button.alight_buttons(start_coordinates=self.mid,
                              orientation="y",
                              space=10,
                              buttons=self.buts)
        for but in self.buts:
            but.pack()
        pygame.display.flip()
        self.loop()
        
    def alterar_nome(self):
        self.nome = Input(window=self.menu,
                          size=[600,50],
                          coordinates= self.coordinate_inputs,
                          title="nome",
                          color=self.color_inputs,
                          color_title=self.color_inputs_title)
        self.ajuste_coordenada(self.but_email.coordinates,self.but_email.size,10,self.nome)
        self.nome.pack()
        self.alterando = self.nome
        self.nome = self.coletar()
        
        
    def alterar_idade(self):
        self.idade = Input(window=self.menu,
                           size=[300,50],
                           coordinates=self.coordinate_inputs,
                           title="idade",
                           color=self.color_inputs,
                           color_title=self.color_inputs_title)
        self.ajuste_coordenada(self.but_email.coordinates,self.but_email.size,10,self.idade)
        self.idade.pack()
        self.alterando = self.idade
        self.idade = self.coletar()
        
        
    def alterar_email(self):    
        self.email = Input(window=self.menu,
                           size=[800,50],
                           coordinates=self.coordinate_inputs,
                           title="email",
                           color=self.color_inputs,
                           color_title=self.color_inputs_title)
        self.ajuste_coordenada(self.but_email.coordinates,self.but_email.size,10,self.email)
        self.email.pack()
        self.alterando = self.email
        self.email = self.coletar()
    
    def sair(self):
        self.loops = False


    def loop(self):
        self.loops = True
        while self.loops:
            for events in pygame.event.get():
                if events.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if events.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for run in self.buts:
                        run.run(pos)
            pygame.display.flip()
                
    def atualizar(self,
                  cnn,
                  nome:str = None,
                  idade:int = None,
                  email:str = None
                  ):
        
        
        try:
            if nome:
                nome= self.tratar_entrada(nome)
            bdpython.user.atualizar_user(conn=cnn,
                                            user_id=self.user_id,
                                            nome=nome,
                                            idade=idade,
                                            email=email)
                
                
            
        except Exception as e:
            print(f"Erro inesperado durante a inclusão: {e}")
            # Opcionalmente, pode-se exibir um aviso ao usuário
            self.erro = funcionais.aviso.Avisos(size_button=[300, 50],
                                                coordinates_button=self.coordinates,
                                                title_button="Erro durante alteração",
                                                color_button="black",
                                                color_title="yellow")
            self.erro.mensagem(f"Erro durante a alteração: {str(e)}")
        finally:
            app = usuario.UsuarioTela()
            app.run()

    def coletar(self):
        self.loops = True
        while self.loops:
            for events in pygame.event.get():
                if events.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if events.type == pygame.MOUSEBUTTONDOWN:
                    posinp = pygame.mouse.get_pos()
                    self.retornar = self.alterando.run(pos=posinp)
                    self.loops = False
            pygame.display.flip()
        return self.retornar
            
    def confirmar(self):
        self.mid_confirmation = tools.get_obj_center(self.menu_size,[300,50])
        self.confirmation = aviso.Avisos(size_button=[300,50],
                                         coordinates_button=[self.mid_confirmation[0],10],
                                         title_button="CONFIRMAR",
                                         color_button="black",
                                         color_title="yellow")
        self.verify = self.confirmation.create_confirmation_buttons()

    def tratar_entrada(self, entrada):
        try:
            tratado = re.sub(r'[^a-zA-Z\s]', '', entrada)
            return tratado
        except Exception as e:
            print(f"Erro ao tratar entrada: {e}")
            raise  # Relevanta a exceção após o log para que ela possa ser capturada na chamada
    @staticmethod
    def ajuste_coordenada(coordenada_principal:list[int],
                          tamanho_principal:list[int],
                          espaço:int,
                          inpute:Input):
        coordenada_ajuste_y = coordenada_principal[1]+tamanho_principal[1]+espaço
        new_coordenada_x = tools.get_obj_center([1000,600],inpute.size)
        new_coordenada = [new_coordenada_x[0], coordenada_ajuste_y]
        inpute.coordinates = new_coordenada
