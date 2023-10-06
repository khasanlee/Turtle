# This example is not working in Spyder directly (F5 or Run)
# Please type '!python turtle_runaway.py' on IPython console in your Spyder.
import tkinter as tk
import turtle, random


class RunawayGame:
    def __init__(self, canvas, runner, chaser, score=0, timer=600, playing = True, catch_radius=50):
        self.canvas = canvas
        self.runner = runner
        self.chaser = chaser
        self.catch_radius2 = catch_radius**2

        # Initialize 'runner' and 'chaser'
        self.runner.shape('turtle')
        self.runner.color('yellow')
        self.runner.penup()

        self.chaser.shape('turtle')
        self.chaser.color('green')
        self.chaser.penup()

        # Instantiate an another turtle for drawing
        self.drawer = turtle.RawTurtle(canvas)
        self.drawer.hideturtle()
        self.drawer.penup()

        self.drawer2 = turtle.RawTurtle(canvas)
        self.drawer2.hideturtle()
        self.drawer2.penup()

        self.score = score
        self.timer = timer
        self.playing = playing

    def is_catched(self):
        p = self.runner.pos()
        q = self.chaser.pos()
        dx, dy = p[0] - q[0], p[1] - q[1]
        return dx**2 + dy**2 < self.catch_radius2

    def start(self, init_dist=400, ai_timer_msec=50):
        if self.playing == True:
            self.runner.setpos((-init_dist / 2, 0))
            self.runner.setheading(0)
            self.chaser.setpos((+init_dist / 2, 0))
            self.chaser.setheading(180)

        # TODO) You can do something here and follows.
            self.ai_timer_msec = ai_timer_msec
            self.canvas.ontimer(self.step, self.ai_timer_msec)
        else:
            self.end()
        

    def step(self):
        self.runner.run_ai(self.chaser.pos(), self.chaser.heading())
        self.chaser.run_ai(self.runner.pos(), self.runner.heading())

        # TODO) You can do something here and follows.
        is_catched = self.is_catched()
        self.drawer.undo()
        self.drawer.penup()
        self.drawer.setpos(-75, 300)
        
        if is_catched == True:
           self.score += 1

        self.timer-=1

        if self.timer<=0:
            self.playing = False
            return self.end()
        

        self.drawer.write(f'Is catched? {is_catched}\ntimer : {self.timer//10},\nscore : {self.score}')
        

        # Note) The following line should be the last of this function to keep the game playing
        self.canvas.ontimer(self.step, self.ai_timer_msec)

    def end(self):
        if self.playing == False:
            self.canvas.clear()
            self.drawer.undo()
            self.drawer.penup()
            self.drawer.setpos(0,0)
            self.drawer.write(f'your score : {self.score}')

class ManualMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=10, step_turn=10):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn

        # Register event handlers
        canvas.onkeypress(lambda: self.forward(self.step_move), 'Up')
        canvas.onkeypress(lambda: self.backward(self.step_move), 'Down')
        canvas.onkeypress(lambda: self.left(self.step_turn), 'Left')
        canvas.onkeypress(lambda: self.right(self.step_turn), 'Right')
        canvas.listen()

    def run_ai(self, opp_pos, opp_heading):
        pass

class RandomMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=15, step_turn=10):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn

    def run_ai(self, opp_pos, opp_heading):
        mode = random.randint(0, 2)
        if mode == 0:
            self.forward(self.step_move)
        elif mode == 1:
            self.left(self.step_turn)
        elif mode == 2:
            self.right(self.step_turn)

if __name__ == '__main__':
    # Use 'TurtleScreen' instead of 'Screen' to prevent an exception from the singleton 'Screen'
    root = tk.Tk()
    canvas = tk.Canvas(root, width=700, height=700)
    canvas.pack()
    screen = turtle.TurtleScreen(canvas)

    # TODO) Change the follows to your turtle if necessary
    runner = RandomMover(screen)
    chaser = ManualMover(screen)

    game = RunawayGame(screen, runner, chaser)
    while game.playing == True:
        screen.bgcolor("#C0C0C0")
        game.start()
        screen.mainloop()
