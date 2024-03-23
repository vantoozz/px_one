"""
Platformer Game
"""
import arcade
import Player

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
SCREEN_TITLE = "PX_ONE"

PLAYER_MOVEMENT_SPEED = 5
GRAVITY = 0.5
PLAYER_JUMP_SPEED = 10

SPRITE_SCALING = .4
BACKGROUND_RISE_AMOUNT = 20


class Game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.tile_map = None
        self.scene = None
        self.player_sprite = None
        self.physics_engine = None
        self.camera = None

        self.backgrounds = arcade.SpriteList()

        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        self.camera = arcade.Camera(self.width, self.height)

        map_name = "assets/tiles/level_1.tmx"

        layer_options = {
            "Platforms": {
                "use_spatial_hash": True,
            },
            "Foreground": {
                "use_spatial_hash": True,
            },
            "Background": {
                "use_spatial_hash": True,
            },
        }

        self.tile_map = arcade.load_tilemap(map_name, scaling=1, layer_options=layer_options)

        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        self.player_sprite = Player.PlayerCharacter("assets/tiles/player-sheet.png")
        self.player_sprite.center_x = 128
        self.player_sprite.center_y = 128
        self.scene.add_sprite("Player", self.player_sprite)
        self.scene.move_sprite_list_before("Player", "Foreground")


        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, gravity_constant=GRAVITY, walls=self.scene["Platforms"]
        )

        """ Set up the game variables. Call to re-start the game. """
        # Create your sprites and sprite lists here
        images = (
            "assets/bg/_05_hill1.png",
            "assets/bg/_04_bushes.png",
            "assets/bg/_03_distant_trees.png",

        )

        rise = BACKGROUND_RISE_AMOUNT * SPRITE_SCALING

        for count, image in enumerate(images):
            bottom = rise * (len(images) - count - 1)

            sprite = arcade.Sprite(image, scale=SPRITE_SCALING)
            sprite.bottom = bottom
            sprite.left = 0
            self.backgrounds.append(sprite)

            sprite = arcade.Sprite(image, scale=SPRITE_SCALING)
            sprite.bottom = bottom
            sprite.left = sprite.width
            self.backgrounds.append(sprite)

        self.scene.add_sprite_list("Parallax", use_spatial_hash=False, sprite_list=self.backgrounds)
        self.scene.move_sprite_list_before("Parallax", "Background")
        self.scene.move_sprite_list_before("Parallax", "Platforms")

    def on_draw(self):
        self.clear()
        self.camera.use()
        self.scene.draw(pixelated=True)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

        if key == arcade.key.SPACE:
            if self.physics_engine.can_jump():
                arcade.play_sound(self.jump_sound)
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (
                self.camera.viewport_height / 2
        )
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered)

    def on_update(self, delta_time):
        """Movement and game logic"""

        # Move the player with the physics engine
        self.physics_engine.update()
        self.player_sprite.update_animation(delta_time)

        # See if we hit any coins
        coin_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.scene["Coins"]
        )

        # Loop through each coin we hit (if any) and remove it
        for coin in coin_hit_list:
            arcade.play_sound(self.collect_coin_sound)
            coin.remove_from_sprite_lists()

        # Position the camera
        self.center_camera_to_player()

        camera_x = self.camera.position[0]

        for count, sprite in enumerate(self.backgrounds):
            layer = count // 2
            frame = count % 2
            offset = camera_x / (2 ** (layer + 1))
            jump = (camera_x - offset) // sprite.width
            final_offset = offset + (jump + frame) * sprite.width
            sprite.left = final_offset


def main():
    """Main function"""
    window = Game()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
