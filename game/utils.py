from pygame import font
import config
colors = {"white" : (255,255,255), "black" : (0,0,0)}

MAX_LEFT = 0
MAX_RIGHT = config.DISPLAY_WIDTH
MAX_TOP = 0
MAX_BOTTOM = config.DISPLAY_HEIGHT

def text_objects(text, font):
    textSurface = font.render(text, True, colors["black"])
    return textSurface, textSurface.get_rect()

def message_display(gameDisplay, text, x, y):
    largeText = font.Font('freesansbold.ttf',20)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((x),(y))
    gameDisplay.blit(TextSurf, TextRect)
