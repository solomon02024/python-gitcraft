from ursina import *

app = Ursina() 

# здесь будет описана игровая логика

app.run()
...

app = Ursina() 

# создаем объекты модели cube, с текстурой white_cube и заданными координатами
for x in range(16): 
   for z in range(16):
       Entity(model="cube", texture="white_cube", position=Vec3(x,0,z))

app.run()# импортируем объект
from ursina.prefabs.first_person_controller import FirstPersonController 

...

# добавляем персонажа
player = FirstPersonController() 

# активируем невесомость, чтобы персонаж не упал в пустоту
player.gravity = 0.0 

app.run()

......

# загружаем текстуру
grass_texture = load_texture('assets/grass.png')

for x_dynamic in range(16):
   for z_dynamic in range(16):
       # настраиваем объект Entity, загружаем модель block.obj
       Entity(model='assets/block', scale=0.5, texture=grass_texture, position=Vec3(x_dynamic,0,z_dynamic))

...
...
# загружаем текстуру руки
arm_texture = load_texture('assets/arm_texture.png')

# объявляем объект hand, привязываем к камере camera.ui, загружаем модель и размещаем ее в правом нижнем углу 
hand = Entity(parent = camera.ui, model = 'assets/arm',
             texture = arm_texture, scale = 0.2,
             rotation = Vec3(150, -10,0), position = Vec2(0.5,-0.6))
...
...

sky_texture = load_texture('assets/sky_texture.png')

sky = Entity(
           model = 'sphere', texture = sky_texture,
           scale = 1000, double_sided = True
       )

...
...

def update():
  print(player.x, player.y, player.z)

...
...

def input(key):

  if key == 'o': # кнопка выхода из игры
    quit()

  if key == 'shift': # кнопка быстрого бега
    global shift_click
    if shift_click % 2 == 0:
      player.speed = normal_speed + 3 # увеличиваем скорость при нажатии
      shift_click += 1
    else:
      player.speed = normal_speed
      shift_click += 1

...
...

# создаем новый класс на базе Button и задаем стартовые параметры
class Voxel(Button):
   def __init__(self, position=(0, 0, 0), texture=grass_texture):
       super().__init__(
           parent=scene, model='assets/block', 
           scale=0.5, texture=texture, position=position,
           origin_y=0.5, color = color.color(0,0,random.uniform(0.9,1))
       )
   
   #  добавляем input — встроенную функцию взаимодействия с блоком Voxel:
   #     		если нажали на ПКМ — появится блок
   #     		если нажали на ЛКМ — удалится 
   def input(self, key):
       if self.hovered:
           if key == 'right mouse down':
               Voxel(position=self.position + mouse.normal, texture=texture)

           if key == 'left mouse down':
               destroy(self)

# генерация платформы из блоков Voxel
for x_dynamic in range(16):
   for z_dynamic in range(16):
       Voxel(position=(x_dynamic,0,z_dynamic))

..... 
# создаем объект Mesh
e = Entity(model=Mesh(), texture=this.textureAtlas) 

# подгружаем конкретную ячейку из атласа текстур (с помощью масштабирования)
# атлас текстур — это обычное изображение, в котором собраны текстуры разных блоков 
e.texture_scale *= 64/e.texture.width 

def genBlock(this, x, y, z):
    model = this.subsets[0].model
    uu = 8
    uv = 7
    model.uvs.extend([Vec2(uu, uv) + u for u in this.block.uvs])

def genTerrain(this):
   x = 0
   z = 0
   y = 0

   o_width = int(this.subWidth*0.5)

   for x_dynamic in range(-o_width, o_width):
      for z_dynamic in range(-o_width, o_width):

# обращаемся к genBlock(), генерируем блоки типа Mesh
          this.genBlock(x+x_dynamic, y, z+z_dynamic)

    this.subsets[0].model.generate()

...
... 
# создаем объект Mesh
e = Entity(model=Mesh(), texture=this.textureAtlas) 

# подгружаем конкретную ячейку из атласа текстур (с помощью масштабирования)
# атлас текстур — это обычное изображение, в котором собраны текстуры разных блоков 
e.texture_scale *= 64/e.texture.width 

def genBlock(this, x, y, z):
    model = this.subsets[0].model
    uu = 8
    uv = 7
    model.uvs.extend([Vec2(uu, uv) + u for u in this.block.uvs])

def genTerrain(this):
   x = 0
   z = 0
   y = 0

   o_width = int(this.subWidth*0.5)

   for x_dynamic in range(-o_width, o_width):
      for z_dynamic in range(-o_width, o_width):

# обращаемся к genBlock(), генерируем блоки типа Mesh
          this.genBlock(x+x_dynamic, y, z+z_dynamic)

    this.subsets[0].model.generate()

...
...

for x_dynamic in range(-o_width, o_width):
 for z_dynamic in range(-o_width, o_width):
     # генерация Mesh-блока в заданной точке, координату y берем из алгоритма Перлина
     this.genBlock(x+x_dynamic, this.landscale[x+x_dynamic][z+z_dynamic], z+z_dynamic)

...
from ursina.shaders import basic_lighting_shader

...

e = Entity(..., shader = basic_lighting_shader)

...
...

scene.fog_density=(0,95)
 
# scene, как и window, тоже один из основных элементов библиотеки. Иногда его можно встретить в параметре наследования parent. Хотя, по моему опыту, его использование скорее опционально, чем обязательно. 

scene.fog_color=color.white

...
 импортируем основные объекты. Предварительно нужно развернуть репозиторий UrsinaLighting внутри своего проекта.  
from UrsinaLighting import LitObject, LitInit

...

# важно! нужно инициализировать главный объект.
lit = LitInit()

...

# заполняем нижние уровни ландшафта водой (y = -1.1), создаем текстуру воды размером с ширину ландшафта. Проседать FPS не будет, тк water — это один объект, который просто «растянут» вдоль игровой сцены
water = LitObject(position = (floor(terrain.subWidth/2), -1.1, floor(terrain.subWidth/2)), scale = terrain.subWidth, water = True, cubemapIntensity = 0.75, collider='box', texture_scale=(terrain.subWidth, terrain.subWidth), ambientStrength = 0.5)

...
...

punch_sound = Audio('assets/punch_sound',loop = False, autoplay = False)

...

class Voxel(Button):
    ...
    def input(key):
        if key == 'left mouse down':
        punch_sound.play()

...
# в отдельном файле menu.py

from ursina import *

app = Ursina(title='Minecraft-Menu')

# создаем объект на базе Entity, настраиваем камеру и бэкграунд
class MenuMenu(Entity):
   def __init__(self, **kwargs):
       super().__init__(parent=camera.ui, ignore_paused=True)

       self.main_menu = Entity(parent=self, enabled=True)
       self.background = Sky(model = "cube", double_sided = True, texture = Texture("textures/skybox.jpg"), rotation = (0, 90, 0))

# стартовая надпись Gitcraft
       Text("Gitcraft", parent = self.main_menu, y=0.4, x=0, origin=(0,0))

       def switch(menu1, menu2):
           menu1.enable()
           menu2.disable()

# вместо print_on_screen можно вписать lambda-функцию для запуска игры
       ButtonList(button_dict={
           "Start": Func(print_on_screen,"You clicked on Start button!", position=(0,.2), origin=(0,0)),
           "Exit": Func(lambda: application.quit())
       },y=0,parent=self.main_menu)

main_menu = MenuMenu()

app.run()
