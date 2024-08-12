import pygame
import basico.tools as tools
from typing import Union, List, Tuple

class Button:
    #começo de tudo, algumas funções estão uma zona, mas adicionei docstrings para não ficar tão confuso
    """
    Classe para criar e manipular botões na interface gráfica.

    Args:
        window (pygame.Surface): A janela onde o botão será desenhado.
        title (str): O título do botão.
        size (Union[list[int], Tuple[int, int, int]]): O tamanho do botão, representado por uma lista ou tupla.
        color (Union[str, Tuple[int, int, int]]): A cor do botão, que pode ser uma string ou uma tupla RGB.
        coordinates (List[int], optional): As coordenadas (x, y) do botão na janela. Defaults to [0,0].
        command (callable, optional): Função a ser executada quando o botão é clicado. Defaults to None.
        background (str, optional): O caminho para a imagem de fundo do botão, se houver. Defaults to None.
        tags (str, optional): O formato do botão (e.g., "elipse"). Defaults to "elipse".
        color_title (str, optional): A cor do texto do título. Defaults to "white".
        size_title (int, optional): O tamanho do texto do título. Defaults to 50.
        color2_title (str, optional): Cor adicional para efeitos no título. Defaults to None.
    """

    def __init__(self,
                 window: pygame.Surface,
                 title: str,
                 size: Union[list[int], Tuple[int, int, int]],
                 color: Union[str, Tuple[int, int, int]],
                 coordinates: List[int] = [0, 0],
                 command: callable = None,
                 background: str = None,
                 tags: str = "elipse",
                 color_title: str = "white",
                 size_title: int = 50,
                 color2_title: str = None):
        self.window = window
        self.title = title
        self.size = size
        self.color = tools.get_color(color)
        self.coordinates = coordinates
        self.command = command
        self.background = background
        self.tags = tags
        self.color2_title = color2_title
        self.color_title = color_title
        self.backup_window = window.copy()
        self.draw = False
        self.fora = False
        self.size_title = size_title
        self.title_surface = tools.insert_text(text=title.upper(),
                                               color=self.color_title,
                                               size=self.size_title,
                                               color2=self.color2_title)
        self.size_of_title = self.title_surface.get_size()

    def pack(self):
        """
        Desenha o botão na janela e ajusta a posição do título.

        Returns:
            Button: Retorna o próprio objeto Button.
        """
        self.__coordinate_title =  tools.get_mid(self.coordinates,self.size,self.size_of_title)
        self.rect = tools.draw_rect(window=self.window,
                                    size=self.size,
                                    color=self.color,
                                    coordinates=self.coordinates,
                                    background=self.background,
                                    tags=self.tags)
        self.window.blit(self.title_surface, (self.__coordinate_title))
        self.backup_window = self.window.copy()
        return self

    def run(self, pos: pygame.mouse):
        """
        Verifica se o botão foi clicado e executa o comando associado.

        Args:
            pos (pygame.mouse): A posição atual do cursor do mouse.
        """
        self.pos = pos
        self.press = tools.verify_click(self.rect, pos)
        if self.press:
            if self.command is not None:
                self.command()

    def tags_run(self,
                 pos:Union[List[int],Tuple[int,int]],
                 size_rect_point:Union[List[int],Tuple[int,int]]=[10,10],
                 color_rect_point:str = "green",
                 background_point:str = None):
        """
        Manipula o comportamento do botão baseado em suas tags, como "elipse".

        Args:
            pos (tuple): A posição atual do cursor do mouse.
            size_rect_point (Union[List[int], Tuple[int,int]], opitional): Tamanho do marcador. Defaults to [10,10]
            color_rect_point (str, opitional): Cor do marcador. Defaults to "green".
            background_point: (str, opitional): Caminho para imagem do marcador. Defaults to None.
        """
        self.pos_tg = pos
        self.coordinates_point = [self.coordinates[0]-size_rect_point[0], self.coordinates[1]+self.size[1]/2 - size_rect_point[1]/2]

        if self.tags == "elipse":
            if not self.draw and not self.fora:
                self.backup_window = self.window.copy()
            if (self.coordinates[0] <= self.pos_tg[0] <= self.coordinates[0] + self.size[0] and
                self.coordinates[1] <= self.pos_tg[1] <= self.coordinates[1] + self.size[1]):
                tools.draw_rect(window=self.window,
                                size=size_rect_point,
                                color= color_rect_point,
                                coordinates=self.coordinates_point,
                                background=background_point,
                                tags=None)
                self.draw = True
            else:
                self.fora = True
            if self.draw and self.fora:
                self.draw = False
                self.fora = False
                self.window.blit(self.backup_window, (0, 0))

def alight_buttons(start_coordinates: list,
                   orientation: str,
                   space: int,
                   buttons: List[Button]):
    """
    Alinha uma lista de botões horizontal ou verticalmente.

    Args:
        start_coordinates (list): As coordenadas iniciais para alinhar os botões.
        orientation (str): A orientação para alinhar os botões ('x' para horizontal, 'y' para vertical).
        space (int): O espaço entre os botões.
        buttons (List[Button]): A lista de botões a serem alinhados.
    """
    start_coordinate = [start_coordinates[0], start_coordinates[1]]
    if orientation == "x":
        for new_but in buttons:
            new_but.coordinates[0] = start_coordinate[0]
            start_coordinate[0] = start_coordinate[0] + space + new_but.size[0]
            new_but.coordinates[1] = start_coordinate[1]
    if orientation == "y":
        for new_but in buttons:
            new_but.coordinates[1] = start_coordinate[1]
            start_coordinate[1] = start_coordinate[1] + space + new_but.size[1]
            new_but.coordinates[0] = start_coordinate[0]

def get_center_button(size_window: Union[List[int], Tuple[int, int]],
                      button: Button,
                      tags: str = "j"):
    """
    Obtém as coordenadas centrais para posicionar um botão no centro da janela.

    Args:
        size_window (Union[List[int], Tuple[int, int]]): O tamanho da janela onde o botão será centralizado.
        button (Button): O botão a ser centralizado.
        tags (str, optional): Define se a centralização será horizontal ('x'), vertical ('y') ou total ('j'). Defaults to "j".

    Returns:
        Tuple[int, int]: As coordenadas centrais (x, y) para o botão.
    """
    if tags == "x":
        center = (int(size_window[0] / 2 - button.size[0] / 2), button.coordinates[1])
        return center
    if tags == "y":
        center = (button.coordinates[0], int(size_window[1] / 2 - button.size[1] / 2))
        return center
    if tags == "j":
        center = (int(size_window[0] / 2 - button.size[0] / 2), int(size_window[1] / 2 - button.size[1] / 2))
        return center
