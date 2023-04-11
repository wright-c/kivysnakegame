from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.clock import Clock
from random import randint
from kivy.core.window import Window


# start a string builder for the kv string
Builder.load_string("""

#:import random random

<SnakePart>:
    size: 40, 40
    canvas.before:
        Color:
            rgba: random.random(), random.random(), random.random(), 1
        Rectangle:
            pos: self.pos
            size: self.size

<GameScreen>:
    canvas.before:
        Color:
            rgba: 0, 0, 0, 1
        Rectangle:
            pos: self.pos
            size: self.size
    Widget:
        size: 40, 40
        pos: 120, 120
        id: food
        canvas.before:
            Color:
                rgba: random.random(), random.random(), random.random(), 1
            Rectangle:
                pos: self.pos
                size: self.size

""")

class SnakePart(Widget):
    pass

class GameScreen(Widget):

    step_size = 40
    movement_x = 0
    movement_y = 0
    snake_parts = []

    def new_game(self):
        to_be_removed = []
        for child in self.children:
            if isinstance(child, SnakePart):
                to_be_removed.append(child)
        for child in to_be_removed:
            self.remove_widget(child)

        self.snake_parts = []
        self.movement_x = 0
        self.movement_y = 0
        head = SnakePart()
        head.pos = 0, 0
        self.snake_parts.append(head)
        self.add_widget(head)

    def on_touch_up(self, touch):
        dx = touch.x - touch.opos[0]
        dy = touch.y - touch.opos[1]
        if abs(dx) > abs(dy):
            # Move horizontally
            self.movement_y = 0
            if dx > 0:
                self.movement_x = self.step_size
            else:
                self.movement_x = -self.step_size
        else:
            # Move vertically
            self.movement_x = 0
            if dy > 0:
                self.movement_y = self.step_size
            else:
                self.movement_y = -self.step_size

    def collides_widget(self, w1, w2):
        if w1.x < w2.x + w2.width and w1.x + w1.width > w2.x and w1.y < w2.y + w2.height and w1.y + w1.height > w2.y:
            return True
        return False

    def next_frame(self, *args):
        # Move the head
        head = self.snake_parts[0]
        food = self.ids.food
        last_x = self.snake_parts[-1].x
        last_y = self.snake_parts[-1].y

        # Move the body
        for i, part in enumerate(self.snake_parts):
            if i == 0:
                continue
            part.new_x = self.snake_parts[i-1].x
            part.new_y = self.snake_parts[i-1].y
        for part in self.snake_parts[1:]:
            part.y = part.new_y
            part.x = part.new_x

        head.x += self.movement_x 
        head.y += self.movement_y
        #Check for snake colliding with food
        if self.collides_widget(head, food):
            food.x = randint(0, Window.width-food.width)
            food.y = randint(0, Window.height-food.height)
            new_part = SnakePart()
            new_part.x = last_x
            new_part.y = last_y
            self.snake_parts.append(new_part)
            self.add_widget(new_part)

        # Check for snake colliding with itself
        for part in self.snake_parts[1:]:
            if self.collides_widget(part, head):
                self.new_game()

        # Check for snake colliding with the wall
        if not self.collides_widget(head, self):
            self.new_game()
    pass

class MainApp(App):
    def build(self):
        return GameScreen()

    def on_start(self):
        self.root.new_game()
        Clock.schedule_interval(self.root.next_frame, .5)
    pass

MainApp().run()