import arcade

RIGHT_FACING = 0
LEFT_FACING = 1
FRAME_RATE = 10


class PlayerCharacter(arcade.Sprite):
    def __init__(self, file_name):
        sprite_sheet = arcade.load_texture(file_name)
        tile_size = sprite_sheet.height

        super().__init__(file_name, scale=1, image_width=tile_size, image_height=tile_size)

        self.time = 0
        self.frames = []
        self.face_direction = RIGHT_FACING

        x = 0
        while x < sprite_sheet.width:
            self.frames.append([
                arcade.load_texture(
                    file_name,
                    x=x,
                    y=0,
                    width=tile_size,
                    height=tile_size
                ),
                arcade.load_texture(
                    file_name,
                    x=x,
                    y=0,
                    width=tile_size,
                    height=tile_size,
                    flipped_horizontally=True
                )
            ])
            x += tile_size

        self.current_frame = 0

    def update_animation(self, delta_time: float = 1 / 60):
        if self.change_x < 0:
            self.face_direction = LEFT_FACING
        elif self.change_x > 0:
            self.face_direction = RIGHT_FACING

        self.time += delta_time
        if self.time > 1 / FRAME_RATE:
            self.time = 0
            self.current_frame += 1
            if self.current_frame > (len(self.frames) - 1):
                self.current_frame = 0

        self.texture = self.frames[self.current_frame][self.face_direction]
