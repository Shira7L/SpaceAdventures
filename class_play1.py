import arcade

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Platformer"
CHARACTER_SCALING = 0.5
TILE_SCALING = 1
GRAVITY = 1
PLAYER_JUMP_SPEED = 15
PLAYER_MOVEMENT_SPEED = 6
LEFT_FACING = 0
RIGHT_FACING = 1
COIN_SCALING = 0.5
MAX_COINS = 3
COIN_SCORE = 10


class Coin(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__("coin.png", COIN_SCALING)
        self.center_x = x
        self.center_y = y


class PlayerSprite(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.scale = CHARACTER_SCALING
        self.idle_right_texture = arcade.load_texture("girl/stand_right.png")
        self.idle_left_texture = arcade.load_texture("girl/stand_left.png")
        self.run_right_textures = [
            arcade.load_texture("girl/run_right1.png"),
            arcade.load_texture("girl/run_right2.png"),
            arcade.load_texture("girl/run_right3.png"),
        ]
        self.run_left_textures = [
            arcade.load_texture("girl/run_left1.png"),
            arcade.load_texture("girl/run_left2.png"),
            arcade.load_texture("girl/run_left3.png"),
        ]

        self.cur_texture = 0
        self.character_face_direction = RIGHT_FACING

        self.animation_time = 0
        self.animation_speed = 0.1
        self.texture = self.idle_right_texture

    def update_texture(self):
        if self.change_x < 0:  # Персонаж движется влево
            self.character_face_direction = LEFT_FACING
            self.texture = self.run_left_textures[self.cur_texture]
        elif self.change_x > 0:  # Персонаж движется вправо
            self.character_face_direction = RIGHT_FACING
            self.texture = self.run_right_textures[self.cur_texture]
        else:  # Персонаж стоит
            if self.character_face_direction == LEFT_FACING:
                self.texture = self.idle_left_texture
            else:
                self.texture = self.idle_right_texture

        self.animation_time += 1 / 60
        if self.animation_time >= self.animation_speed:
            if self.change_x != 0:
                self.cur_texture = (self.cur_texture + 1) % len(
                    self.run_right_textures if self.character_face_direction == RIGHT_FACING else self.run_left_textures)
            self.animation_time = 0
