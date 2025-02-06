from final.constants import *
from final.class_play1 import *
import random
BACKGROUND_IMAGE = "background.jpeg"


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
            window = MyGame()
            window.setup()
            arcade.run()
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


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.tile_map = None
        self.scene = None
        self.player_sprite = None
        self.physics_engine = None
        self.camera = None
        self.gui_camera = None
        self.score = 0
        self.coins = arcade.SpriteList()
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        self.camera = arcade.Camera(self.width, self.height)
        self.gui_camera = arcade.Camera(self.width, self.height)
        map_name = "maps.json"
        layer_options = {
            "platforms": {
                "use_spatial_hash": True,
            },
        }
        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        self.player_sprite = PlayerSprite()
        self.player_sprite.center_x = 128
        self.player_sprite.center_y = 128
        self.scene.add_sprite("Player", self.player_sprite)
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, self.scene.get_sprite_list("platforms"), GRAVITY
        )
        self.generate_coins()

    def generate_coins(self):
        while len(self.coins) < MAX_COINS:
            x = random.randint(500, SCREEN_WIDTH - 20)
            y = random.randint(50, SCREEN_HEIGHT - 20)
            coin = Coin(x, y)
            if not arcade.check_for_collision_with_list(coin, self.scene.get_sprite_list(
                    "platforms")) and not arcade.check_for_collision(coin, self.player_sprite):
                self.coins.append(coin)
                self.scene.add_sprite("Coins", coin)

    def on_draw(self):
        arcade.start_render()
        self.camera.use()
        self.scene.draw()
        self.gui_camera.use()
        score_text = f"Score: {self.score}"
        arcade.draw_text(score_text, 10, 10, arcade.csscolor.WHITE, 18)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (self.camera.viewport_height / 2)

        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0

        player_centered = screen_center_x, screen_center_y
        self.camera.move_to(player_centered)

    def on_update(self, delta_time):
        self.physics_engine.update()
        self.player_sprite.update_texture()
        self.center_camera_to_player()
        collided_coins = arcade.check_for_collision_with_list(self.player_sprite, self.coins)
        for coin in collided_coins:
            coin.remove_from_sprite_lists()
            self.score += COIN_SCORE
        self.generate_coins()


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
