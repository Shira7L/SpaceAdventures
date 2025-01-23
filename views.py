import arcade
from constants import *
import pytmx
import pygame
pygame.init()


class Button(arcade.Sprite):
    # Кнопки
    def __init__(self, text, x, y, width, height, color=arcade.csscolor.AQUA):
        super().__init__()
        self.width, self.height, self.color, self.text, self.center_x, self.center_y, self.is_hovered = (
            width, height, color, text, x, y, False)

    def draw(self):
        if self.is_hovered:
            arcade.draw_rectangle_filled(self.center_x, self.center_y, self.width, self.height, arcade.csscolor.GRAY)
        else:
            arcade.draw_rectangle_filled(self.center_x, self.center_y, self.width, self.height, self.color)
        arcade.draw_text(self.text, self.center_x, self.center_y, arcade.color.BLACK, font_size=20,
                         anchor_x="center", anchor_y="center")


class GameMenu(arcade.View):  # Меню игры
    def __init__(self):
        super().__init__()
        self.game1 = Button("Начать игру 1", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.1 - 200, 430, 50)
        self.game2 = Button("Начать игру 2", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.1 - 270, 430, 50)
        self.rules = Button("Правила игры", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.1 - 340, 430, 50)

    def on_show(self):
        arcade.set_background_color(arcade.csscolor.LIGHT_BLUE)
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, arcade.load_texture(BACKGROUND_IMAGE))
        arcade.draw_text("Космические приключения", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.1, arcade.color.WHITE,
                         font_size=50, anchor_x="center")
        # Рисуем кнопки
        self.game1.draw()
        self.game2.draw()
        self.rules.draw()

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        # Наведение мыши на кнопки
        self.game1.is_hovered = (self.game1.center_x - self.game1.width / 2 < x < self.game1.center_x +
                                 self.game1.width / 2 and self.game1.center_y - self.game1.height / 2 < y <
                                 self.game1.center_y + self.game1.height / 2)

        self.game2.is_hovered = (self.game2.center_x - self.game2.width / 2 < x < self.game2.center_x +
                                 self.game2.width / 2 and self.game2.center_y - self.game2.height / 2 < y <
                                 self.game2.center_y + self.game2.height / 2)

        self.rules.is_hovered = (self.rules.center_x - self.rules.width / 2 < x < self.rules.center_x +
                                 self.rules.width / 2 and self.rules.center_y - self.rules.height / 2 < y <
                                 self.rules.center_y + self.rules.height / 2)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        # Нажатие на кнопки
        if self.game1.is_hovered:
            # Начать игру 1
            self.window.close()
            view = Game()
            view.run()
        elif self.game2.is_hovered:
            # Начать игру 2
            print("Запуск игры 2")
        elif self.rules.is_hovered:
            # Правила
            self.show_rules()

    def show_rules(self):
        rules_view = RulesView()
        self.window.show_view(rules_view)


class RulesView(arcade.View):
    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Правила игры:", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50, arcade.color.BLACK, 24,
                         anchor_x="center", anchor_y="center")
        arcade.draw_text("1. Используйте стрелки для перемещения персонажа", SCREEN_WIDTH // 2,
                         SCREEN_HEIGHT // 2, arcade.color.BLACK, 20, anchor_x="center", anchor_y="center")
        arcade.draw_text("2. Пробел - стрельба", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30,
                         arcade.color.BLACK, 20, anchor_x="center", anchor_y="center")
        arcade.draw_text("3. Собирайте звёзды и уничтожайте мобов для получения очков", SCREEN_WIDTH // 2,
                         SCREEN_HEIGHT // 2 - 60, arcade.color.BLACK, 20, anchor_x="center", anchor_y="center")
        arcade.draw_text("Нажмите на экран для возврата в меню", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100,
                         arcade.color.BLACK, 20, anchor_x="center", anchor_y="center")

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        view = GameMenu()
        self.window.show_view(view)


class Game:
    # Загрузка карты
    def __init__(self):
        self.screen = pygame.display.set_mode((MAP_WIDTH * TILE_SIZE, MAP_HEIGHT * TILE_SIZE))
        pygame.display.set_caption("Игра 1")
        self.tmx_data = pytmx.load_pygame("C:\\Users\\User\\PycharmProjects\\pythonProject4\\ground.tmx")

    def draw_map(self):
        # Слой "background"
        background_layer = self.tmx_data.get_layer_by_name("background")
        if isinstance(background_layer, pytmx.TiledTileLayer):
            for x, y, gid in background_layer:
                if gid != 0:
                    tile = self.tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        self.screen.blit(tile, (x * TILE_SIZE, y * TILE_SIZE))

        # Слой "ground"
        ground_layer = self.tmx_data.get_layer_by_name("ground")
        if isinstance(ground_layer, pytmx.TiledObjectGroup):
            for obj in ground_layer:
                if hasattr(obj, 'gid') and obj.gid != 0:
                    tile = self.tmx_data.get_tile_image_by_gid(obj.gid)
                    if tile:
                        self.screen.blit(tile, (obj.x, obj.y))

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.draw_map()
            pygame.display.flip()
        pygame.quit()


class GameOver(arcade.View):  # Конечная заставка
    def __init__(self, score):
        super(GameOver, self).__init__()
        self.score = score

    def on_show(self):
        arcade.set_background_color(arcade.csscolor.LIGHT_BLUE)
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Конец игры", SCREEN_WIDTH / 2,
                         SCREEN_HEIGHT / 2, arcade.color.WHITE, font_size=50,
                         anchor_x="center")
        arcade.draw_text(f"Набранно очков: {self.score}", SCREEN_WIDTH / 2,
                         SCREEN_HEIGHT / 2 - 75, arcade.color.WHITE, font_size=20,
                         anchor_x="center")

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        view = GameMenu()
        self.window.show_view(view)
