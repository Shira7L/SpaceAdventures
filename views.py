from class_play import *
import random
import time
import pygame.mixer
import csv
import os


class Button(arcade.Sprite):
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


class GameMenu(arcade.View):
    def __init__(self):
        super().__init__()
        self.game1 = Button("Начать игру 1", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.1 - 200, 430, 50)
        self.game2 = Button("Начать игру 2", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.1 - 270, 430, 50)
        self.rules = Button("Правила игры", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.1 - 340, 430, 50)

    def on_show(self):
        arcade.set_background_color(arcade.csscolor.LIGHT_BLUE)
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)
        pygame.mixer.init()
        pygame.mixer.music.load(MUSIC_FILE)
        pygame.mixer.music.play(-1)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, arcade.load_texture(BACKGROUND_IMAGE))
        arcade.draw_text("Космические приключения", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.1, arcade.color.WHITE,
                         font_size=50, anchor_x="center")
        self.game1.draw()
        self.game2.draw()
        self.rules.draw()

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
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
        if self.game1.is_hovered:
            game_view = MyGame(map_name="C:\\Users\\User\\PycharmProjects\\SpaceAdventuresPlay\\maps\\maps1.json", map_width=MAP_WIDTH1, map_height=MAP_HEIGHT1, num=1)
            game_view.setup()
            self.window.show_view(game_view)
        elif self.game2.is_hovered:
            game_view = MyGame(map_name="C:\\Users\\User\\PycharmProjects\\SpaceAdventuresPlay\\maps\\maps2.json", map_width=MAP_WIDTH2, map_height=MAP_HEIGHT2, num=2)
            game_view.setup()
            self.window.show_view(game_view)
        elif self.rules.is_hovered:
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
        arcade.draw_text("3. Собирайте деньги и уничтожайте мобов для получения очков", SCREEN_WIDTH // 2,
                         SCREEN_HEIGHT // 2 - 60, arcade.color.BLACK, 20, anchor_x="center", anchor_y="center")
        arcade.draw_text("Нажмите на экран для возврата в меню", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100,
                         arcade.color.BLACK, 20, anchor_x="center", anchor_y="center")

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        view = GameMenu()
        self.window.show_view(view)


class MyGame(arcade.View):
    def __init__(self, map_name, map_width, map_height, num):
        super().__init__()
        self.map_name = map_name
        self.map_width = map_width
        self.map_height = map_height
        self.num = num
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.physics_engine = None
        self.camera = None
        self.tile_map = None
        self.scene = None
        self.player_spriteone = None
        self.gui_camera = None
        self.score = 0
        self.misses = 0
        self.coin = None
        self.coin_timer = 0
        self.bullets = arcade.SpriteList()
        self.mobs = arcade.SpriteList()
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)
        self.results_file = "results.csv"
        if not os.path.exists(self.results_file):
            with open(self.results_file, mode='w', newline='') as file:
                writer = csv.writer(file, delimiter=";")
                writer.writerow(["Game", "Score"])

    def setup(self):
        self.camera = arcade.Camera(self.width, self.height)
        self.gui_camera = arcade.Camera(self.width, self.height)
        map_name = self.map_name
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
        self.spawn_coin()
        self.spawn_mobs()

    def spawn_coin(self):
        if self.coin:
            self.coin.remove_from_sprite_lists()
        while True:
            x = random.randint(0, self.map_width)
            y = random.randint(0, self.map_height)
            coin = Coin(x, y)
            if not arcade.check_for_collision_with_list(coin, self.scene.get_sprite_list(
                    "platforms")) and not arcade.check_for_collision(coin, self.player_sprite):
                self.coin = coin
                self.scene.add_sprite("Coins", self.coin)
                break
        self.coin_timer = time.time() + 10

    def spawn_mobs(self):
        for _ in range(MOBS_PER_DIRECTION):
            self.spawn_single_mob(RIGHT_FACING)
        for _ in range(MOBS_PER_DIRECTION):
            self.spawn_single_mob(LEFT_FACING)

    def spawn_single_mob(self, direction):
        while True:
            x = random.randint(1, self.map_width)
            y = random.randint(1, self.map_height)
            mob = Mob(x, y, direction)
            if not arcade.check_for_collision_with_list(mob, self.scene.get_sprite_list("platforms")) and \
                    not arcade.check_for_collision(mob, self.player_sprite):
                self.mobs.append(mob)
                self.scene.add_sprite("Mobs", mob)
                break

    def on_draw(self):
        arcade.start_render()
        self.camera.use()
        self.scene.draw()
        self.bullets.draw()
        self.mobs.draw()
        for mob in self.mobs:
            mob.bullets.draw()

        self.gui_camera.use()
        score_text = f"Score: {self.score}  Misses: {self.misses}/{MAX_MISSES}"
        arcade.draw_text(score_text, 10, 10, arcade.csscolor.WHITE, 18)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.SPACE:
            self.shoot_bullet()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def shoot_bullet(self):
        bullet = Bullet(self.player_sprite.center_x, self.player_sprite.center_y,
                        self.player_sprite.character_face_direction)
        self.bullets.append(bullet)
        self.scene.add_sprite("Bullets", bullet)
        if self.player_sprite.character_face_direction == RIGHT_FACING:
            bullet.center_x += 0
        else:
            bullet.center_x -= 0

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
        self.bullets.update()
        for bullet in self.bullets:
            if arcade.check_for_collision_with_list(bullet, self.scene.get_sprite_list("platforms")):
                bullet.remove_from_sprite_lists()
        if self.coin and time.time() > self.coin_timer:
            self.misses += 1
            self.spawn_coin()
            if self.misses >= MAX_MISSES:
                self.game_over()
        if self.player_sprite and self.coin:
            if arcade.check_for_collision(self.player_sprite, self.coin):
                self.score += COIN_SCORE
                self.spawn_coin()
        self.mobs.update()
        for mob in self.mobs:
            mob.update()
            mob.bullets.update()
            for bullet in mob.bullets:
                bullet.update()
                if arcade.check_for_collision(bullet, self.player_sprite):
                    self.game_over()
                if arcade.check_for_collision_with_list(bullet, self.scene.get_sprite_list("platforms")):
                    bullet.remove_from_sprite_lists()
            for bullet in self.bullets:
                if arcade.check_for_collision(bullet, mob):
                    self.score += 15
                    bullet.remove_from_sprite_lists()
                    mob.remove_from_sprite_lists()
                    break
        if time.time() % 10 < 0.1:
            self.update_mobs_position()

    def update_mobs_position(self):
        current_mob_count = len(self.mobs)
        while current_mob_count < TOTAL_MOBS:
            facing_direction = RIGHT_FACING if len(
                [m for m in self.mobs if m.direction == RIGHT_FACING]) < MOBS_PER_DIRECTION else LEFT_FACING
            x = random.randint(0, self.map_width)
            y = random.randint(0, 832)
            new_mob = Mob(x, y, facing_direction)
            if not arcade.check_for_collision_with_list(new_mob, self.scene.get_sprite_list("platforms")) and \
                    not arcade.check_for_collision(new_mob, self.player_sprite):
                self.mobs.append(new_mob)
                self.scene.add_sprite("Mobs", new_mob)
                current_mob_count += 1
            for mob in self.mobs:
                mob.center_x = random.randint(0, self.map_width)
                mob.center_y = random.randint(0, self.map_height)

    def game_over(self):
        self.save_results()
        game_over_view = GameOver(self.score)
        arcade.get_window().show_view(game_over_view)

    def save_results(self):
        with open(self.results_file, mode='r', newline='') as file:
            reader = csv.reader(file, delimiter=";")
            header = next(reader)
            results = list(reader)
        new_result = [f"Game {self.num}", self.score]
        inserted = False
        for i in range(len(results)):
            if self.score > int(results[i][1]):
                results.insert(i, new_result)
                inserted = True
                break
        if not inserted:
            results.append(new_result)
        with open(self.results_file, mode='w', newline='') as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(header)
            writer.writerows(results)


class GameOver(arcade.View):
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







