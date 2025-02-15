import arcade
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
MAP_WIDTH1 = 1984
MAP_HEIGHT1 = 832
MAP_WIDTH2 = 1184
MAP_HEIGHT2 = 736
MUSIC_FILE = "music.mp3"
BACKGROUND_IMAGE = "C:\\Users\\User\\PycharmProjects\\SpaceAdventuresPlay\\img\\background.jpeg"
SCREEN_TITLE = "Platformer"
CHARACTER_SCALING = 0.5
TILE_SCALING = 1
GRAVITY = 1
PLAYER_JUMP_SPEED = 15
PLAYER_MOVEMENT_SPEED = 6
LEFT_FACING = 0
RIGHT_FACING = 1
COIN_SCALING = 0.5
COIN_SCORE = 10
BULLET_SPEED = 10
MAX_MISSES = 10
BULLET_SCALING = CHARACTER_SCALING / 3
BULLET_SCALINGMOB = CHARACTER_SCALING
TOTAL_MOBS = 10
MOBS_PER_DIRECTION = TOTAL_MOBS // 2


class Coin(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__("C:\\Users\\User\\PycharmProjects\\SpaceAdventuresPlay\\img\\coin.png", COIN_SCALING)
        self.center_x = x
        self.center_y = y


class Bullet(arcade.Sprite):
    def __init__(self, x, y, direction):
        super().__init__("C:\\Users\\User\\PycharmProjects\\SpaceAdventuresPlay\\img\\bullet\\bullet.png", BULLET_SCALING)
        self.center_x = x
        self.center_y = y
        self.direction = direction

    def update(self):
        if self.direction == RIGHT_FACING:
            self.center_x += BULLET_SPEED
        else:
            self.center_x -= BULLET_SPEED


class BulletMob(arcade.Sprite):
    def __init__(self, x, y, direction):
        super().__init__("C:\\Users\\User\\PycharmProjects\\SpaceAdventuresPlay\\img\\bullet\\bullet_mob.png", BULLET_SCALINGMOB)  # Используем изображение пули для mob
        self.center_x = x
        self.center_y = y
        self.direction = direction

    def update(self):
        if self.direction == RIGHT_FACING:
            self.center_x += BULLET_SPEED
        else:
            self.center_x -= BULLET_SPEED


class PlayerSprite(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.scale = CHARACTER_SCALING
        self.idle_right_texture = arcade.load_texture("C:\\Users\\User\\PycharmProjects\\SpaceAdventuresPlay\\img\\girl\\stand_right.png")
        self.idle_left_texture = arcade.load_texture("C:\\Users\\User\\PycharmProjects\\SpaceAdventuresPlay\\img\\girl\\stand_left.png")
        self.run_right_textures = [
            arcade.load_texture("C:\\Users\\User\\PycharmProjects\\SpaceAdventuresPlay\\img\\girl\\run_right1.png"),
            arcade.load_texture("C:\\Users\\User\\PycharmProjects\\SpaceAdventuresPlay\\img\\girl\\run_right2.png"),
            arcade.load_texture("C:\\Users\\User\\PycharmProjects\\SpaceAdventuresPlay\\img\\girl\\run_right3.png"),
        ]
        self.run_left_textures = [
            arcade.load_texture("C:\\Users\\User\\PycharmProjects\\SpaceAdventuresPlay\\img\\girl\\run_left1.png"),
            arcade.load_texture("C:\\Users\\User\\PycharmProjects\\SpaceAdventuresPlay\\img\\girl\\run_left2.png"),
            arcade.load_texture("C:\\Users\\User\\PycharmProjects\\SpaceAdventuresPlay\\img\\girl\\run_left3.png"),
        ]
        self.cur_texture = 0
        self.character_face_direction = RIGHT_FACING
        self.shooting = False
        self.animation_time = 0
        self.animation_speed = 0.1
        self.texture = self.idle_right_texture

    def update_texture(self):
        if self.change_x < 0:
            self.character_face_direction = LEFT_FACING
            self.texture = self.run_left_textures[self.cur_texture]
            self.flip_horizontally = True
        elif self.change_x > 0:
            self.character_face_direction = RIGHT_FACING
            self.texture = self.run_right_textures[self.cur_texture]
            self.flip_horizontally = False
        else:
            if self.character_face_direction == LEFT_FACING:
                self.texture = self.idle_left_texture
            else:
                self.texture = self.idle_right_texture
        self.animation_time += 1 / 60
        if self.animation_time >= self.animation_speed:
            if self.change_x != 0:
                self.cur_texture = (self.cur_texture + 1) % len(self.run_right_textures if self.character_face_direction == RIGHT_FACING else self.run_left_textures)
            self.animation_time = 0


class Mob(arcade.Sprite):
    def __init__(self, x, y, direction):
        if direction == RIGHT_FACING:
            texture = "C:\\Users\\User\\PycharmProjects\\SpaceAdventuresPlay\\img\\mob\\mob.png"
        else:
            texture = "C:\\Users\\User\\PycharmProjects\\SpaceAdventuresPlay\\img\\mob\\mob1.png"
        super().__init__(texture, CHARACTER_SCALING)
        self.center_x = x
        self.center_y = y
        self.bullet_timer = 0
        self.direction = direction
        self.bullets = arcade.SpriteList()

    def update(self):
        self.bullet_timer += 1 / 60
        if self.bullet_timer >= 2:
            self.shoot_bullet()
            self.bullet_timer = 0

    def shoot_bullet(self):
        bullet = BulletMob(self.center_x, self.center_y, self.direction)
        self.bullets.append(bullet)
        if self.direction == RIGHT_FACING:
            bullet.center_x += 0
        else:
            bullet.center_x -= 0
