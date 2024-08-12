import pygame
from typing import Union,List,Tuple

pygame.init()
@staticmethod
def get_color(name_of_color:Union[str,Tuple[int,int,int]]):
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
@staticmethod
def get_image(path_image:str):
    image = pygame.image.load(path_image)
    return image

@staticmethod
def draw_rect(window,
              size:Union[List[int],Tuple[int,int,int]],
              color:Union[str,List[int],Tuple[int,int,int]],
              coordinates:Union[List[int],Tuple[int,int,int]],
              background:str,
              tags):
    if color is not None:
        rect = pygame.draw.rect(window,color,(coordinates[0],coordinates[1],size[0],size[1]))
    if background is not None:
        rect = pygame.Rect((coordinates[0],coordinates[1],size[0],size[1]))
        background = get_image(background)
        background = pygame.transform.scale(background,size)
        window.blit(background,coordinates)
    return rect
@staticmethod
def verify_click(rect:pygame.Rect,
                 position:Union[List[int],Tuple[int,int,int]]):
    clicked = rect.collidepoint(position)
    return clicked

@staticmethod
def insert_text(text:str,
                color:Union[List[int],Tuple[int,int,int],str],
                size:Union[Tuple[int,int],List[int]],
                color2:str,
                background:str = None,
                percent_background = 10):
    color = get_color(color)
    fonte = pygame.font.Font(None,size)
    text_render = fonte.render(text,True,color,color2)
    returnar = text_render
    if background is not None:
        background = get_image(background)
        size_image = text_render.get_size()
        size_image = [size_image[0]+percent_background/100*size_image[0],size_image[1]+percent_background/100*size_image[1]]
        background = pygame.transform.scale(background,size_image)
        returnar = [text_render, background]
        return returnar
    

    return returnar

@staticmethod
def get_obj_center(coordinate_size,
                   size_objt):
    size_obj = [size_objt[0],size_objt[1]]
    center = [int(coordinate_size[0]/2 - size_obj[0]/2),int(coordinate_size[1]/2-size_obj[1]/2)]
    print("center",center)
    return center

@staticmethod
def get_mid(object_base_coordinates:Union[List[int],Tuple[int,int]],
            object_base_size:Union[List[int],Tuple[int,int]],
            object_target_size:Union[List[int],Tuple[int,int]] = None,
            orientation:str="Todo"):
    """_summary_

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