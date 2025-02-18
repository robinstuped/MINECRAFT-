from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random

app = Ursina()
window.exit_button.visible = False

# Load textures
textures = {
    1: load_texture("Assets/Textures/Grass_Block.png"),
    2: load_texture("Assets/Textures/Stone_Block.png"),
    3: load_texture("Assets/Textures/Brick_Block.png"),
    4: load_texture("Assets/Textures/Dirt_Block.png"),
    5: load_texture("Assets/Textures/Wood_Block.png"),
}

block_pick = 1  # Start with grass

punch_sound = Audio("Assets/SFX/Punch_Sound.wav", loop=False, autoplay=False)

class Block(Button):
    def __init__(self, position=(0, 0, 0), texture=textures[1], breakable=True):
        super().__init__(
            parent=scene,
            position=position,
            model="Assets/Models/Block",
            origin_y=0.5,
            texture=texture,
            color=color.color(0, 0, random.uniform(0.9, 1)),
            highlight_color=color.light_gray,
            scale=0.5
        )
        self.breakable = breakable

    def input(self, key):
        if self.hovered:
            if key == "left mouse down":
                punch_sound.play()
                new_block = Block(position=self.position + mouse.normal, texture=textures[block_pick])
            elif key == "right mouse down" and self.breakable:
                punch_sound.play()
                destroy(self)
class Tree(Entity):
    def __init__(self, position=(0,0,0)):
        super().__init__(
            parent=scene,
            position=position,
            model="Assets/Models/Lowpoly_tree_sample.obj",
            scale=(0.5,0.5,0.5)
        )

def generate_trees(num_trees=3, terrain_size=20):
    for _ in range(num_trees):
        x = random.randint(0, terrain_size-1)
        y = 0
        z = random.randint(0, terrain_size-1)
        Tree(position=(x,y,z))

generate_trees()


def terrainator():
    height = [[0 for x in range(20)] for z in range(20)]

    for z in range(20):
        for x in range(20):
            height[z][x] = random.randint(3,6)
    for z in range(1, 19):
        for x in range(1, 19):
            total = height[z][x]
            count = 1
            neighbors = [(0,1),(0,-1),(1,0),(-1,0)]
            for dx, dz in neighbors:
                total += height[z+dz][x+dx]
                count += 1
            height[z][x] = total // count
    for z in range(20):
        for x in range(20):
            h = height[z][x]
            for y in range(h+1):
                if y==h:
                    Block(position=(x,y,z), texture=textures[1])
                elif y >=h - 2:
                    Block(position=(x,y,z), texture=textures[4])
                else:
                    Block(position=(x,y,z), texture=textures[2])
            
terrainator()



for z in range(20):
    for x in range(20):
        block = Block(position=(x,0,z))


player = FirstPersonController(position=(10, 10, 10))
player.cursor.visible = False

sky = Sky()

def update():
    global block_pick
    for i in range(1, 6):
        if held_keys[str(i)]:
            block_pick = i
            break
    if held_keys["escape"]:
        application.quit()
    
    if player.y <= -5:
        player.position=(10,10,10)

app.run()


# https://drive.google.com/file/d/1XMxh_U6Esbiw8l9artv2U8hQ8wmG6Vb4/view?usp=sharing