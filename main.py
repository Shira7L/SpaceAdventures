from class_play import *
from views import GameMenu


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    view = GameMenu()
    window.show_view(view)
    arcade.run()


if __name__ == '__main__':
    main()