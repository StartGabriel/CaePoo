import pygame
from typing import Union,List,Tuple

pygame.init()

def get_color(name_of_color:Union[str,Tuple[int,int,int]]):
    """Converte o nome passado em uma tupla RGB

    Args:
        name_of_color (Union[str,Tuple[int,int,int]]): Var com o nome ou valores RGB (red, green, blue)
    Returns:
        tuple: valor (R, G, B) range(255,255,255)
    """
    COLORS = {
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "yellow": (255, 255, 0),
    "cyan": (0, 255, 255),
    "magenta": (255, 0, 255),
    "orange": (255, 165, 0),
    "purple": (128, 0, 128),
    "gray": (128, 128, 128),
    "brown": (165, 42, 42),
    "pink": (255, 192, 203),
    "lime": (0, 255, 0),
    "navy": (0, 0, 128),
    "teal": (0, 128, 128),
    "maroon": (128, 0, 0),
    "olive": (128, 128, 0),
    "gold": (255, 215, 0),
    "silver": (192, 192, 192)
}

    if type(name_of_color) == str:
        name_of_color = name_of_color.lower()
        return COLORS[name_of_color]
    else:
        return name_of_color

def get_image(path_image:str):
    """Função para fazer upload de imagem

    Args:
        path_image (str): Caminho da imagem

    Returns:
        Surface: Imagem convertida pela biblioteca pygame
    """
    image = pygame.image.load(path_image)
    return image

def draw_rect(window:pygame.Surface,
              size:Union[List[int],Tuple[int,int,int]],
              color:Union[str,List[int],Tuple[int,int,int]],
              coordinates:Union[List[int],Tuple[int,int,int]],
              background:str,
              tags:str):
    """Desenha um retângulo na tela

    Args:
        window (Surface): Janela onde sera desenhado o retângulo
        size (Union[List[int],Tuple[int,int,int]]): Tamanho do retângulo [largura,altura]
        color (Union[str,List[int],Tuple[int,int,int]]): _description_
        coordinates (Union[List[int],Tuple[int,int,int]]): _description_
        background (str): _description_
        tags (str): _description_

    Returns:
        _type_: _description_
    """
    if color is not None:
        rect = pygame.draw.rect(window,color,(coordinates[0],coordinates[1],size[0],size[1]))
    if background is not None:
        rect = pygame.Rect((coordinates[0],coordinates[1],size[0],size[1]))
        background = get_image(background)
        background = pygame.transform.scale(background,size)
        window.blit(background,coordinates)
    return rect

def verify_click(rect:pygame.Rect,
                 position:Union[List[int],Tuple[int,int,int]]):
    """Verifica a região clicada

    Args:
        rect (pygame.Rect): Retangulo do pygame
        position (Union[List[int],Tuple[int,int,int]]): Lista com coordenadas, de onde foi clicado [x,y]
    Returns:
        bool: Retorna se houve colisão mause/retângulo um valor bool
    """
    clicked = rect.collidepoint(position)
    return clicked


def insert_text(text:str,
                color:Union[List[int],Tuple[int,int,int],str],
                size:int,
                background_color:str = None,
                background:str = None,
                percent_background = 10):
    """Função para inserir trasformar texto

    Args:
        text (str): Texto a ser inserido.
        color (Union[List[int],Tuple[int,int,int],str]): Cor do texto.
        size (int): tamanho do texto.
        background_color (str, opitional): Cor do fundo. Defaults to None
        background (str, optional): Caminho para imagem de fundo. Defaults to None.
        percent_background (int, optional): porcentagem de aumento da imagem. Defaults to 10.

    Returns:
        Surface: Retorna um objeto Surface
    """
    color = get_color(color)
    fonte = pygame.font.Font(None,size)
    text_render = fonte.render(text,True,color,background_color)
    returnar = text_render
    if background is not None:
        background = get_image(background)
        size_image = text_render.get_size()
        size_image = [size_image[0]+percent_background/100*size_image[0],size_image[1]+percent_background/100*size_image[1]]
        background = pygame.transform.scale(background,size_image)
        returnar = [text_render, background]
        return returnar
    

    return returnar


def get_obj_center(coordinate_size:Union[List[int],Tuple[int,int]],
                   size_objt:Union[List[int],Tuple[int,int]]):
    """Coletar um ponto central de acordo com as posições

    Args:
        coordinate_size (Union[List[int],Tuple[int,int]]): Tamanho da area na qual quer coletar o centro [x,y]
        size_objt (Union[List[int],Tuple[int,int]]): Tamanho do objeto a ser calculado [x,y]

    Returns:
        list: Retorna uma lista com os valores do centro de acordo com o tamanho do objeto
    """
    size_obj = [size_objt[0],size_objt[1]]
    center = [int(coordinate_size[0]/2 - size_obj[0]/2),int(coordinate_size[1]/2-size_obj[1]/2)]
    print("center",center)
    return center


def get_mid(object_base_coordinates:Union[List[int],Tuple[int,int]],
            object_base_size:Union[List[int],Tuple[int,int]],
            object_target_size:Union[List[int],Tuple[int,int]] = None,
            orientation:str="Todo"):
    """Função para obter as coordenadas do centro de acordo com as coordenadas informadas

    Args:
        object_base_coordinates (Union[List[int],Tuple[int,int]]): Coordenadas do objeto alvo do calculo do centro
        object_base_size (Union[List[int],Tuple[int,int]]): Tamanho do obejto alvo
        object_target_size (Union[List[int],Tuple[int,int]]): _Tamanho do objeto que estara no centro
        orientation (str): Posição que deseja encontrar. Use "Largura", "Altura", "Todo"

    Returns:
        list: Retorna as coordenadas do centro
    """
    coordinate = []
    if orientation.lower() == "largura":
        coordinate = [object_base_coordinates[0] + object_base_size[0]/2 - object_target_size[0]/2,object_base_coordinates[1]]
        
    if orientation.lower() == "altura":
        coordinate = [object_base_coordinates[0], object_base_coordinates[1] + object_base_size[1]/2 - object_target_size[1]/2]
        
    else:
        coordinate = [object_base_coordinates[0] + object_base_size[0]/2 - object_target_size[0]/2, object_base_coordinates[1] + object_base_size[1]/2 - object_target_size[1]/2]
    
    return coordinate
