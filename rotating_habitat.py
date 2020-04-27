import matplotlib.pyplot as plt
from matplotlib import animation
import math
import numpy

class Ball:

    def __init__(self, initial_position: numpy.ndarray, initial_speed: numpy.ndarray, time_step):
        if time_step <= 0:
            raise ValueError("'time_step' must be positive.")
        self.position = initial_position
        self.speed = initial_speed
        self.time_step = time_step

    def move(self):
        self.position = numpy.add(self.position, self.speed * self.time_step)

class Cylinder:

    def __init__(self, angular_speed, time_step):
        self.theta = 0 # this angle defines where the observer is
        self.w = angular_speed * math.pi/30 # angular speed is provided in RPM, but we work in radians/s
        self.time_step = time_step

    def __rotate(self):
        self.theta += self.w * self.time_step

    def __relative_position(self, ball: Ball):
        # finds the position of the ball relative to the observer
        # we apply a rotation matrix of - theta to the (copy of) position of the ball
        # we do not want to modify the real position of the ball
        ball_position = ball.position
        rot = numpy.array([[math.cos(self.theta), math.sin(self.theta)],
                           [-math.sin(self.theta), math.cos(self.theta)]])
        ball_position = rot.dot(ball_position)
        return ball_position

    def __isInside(self, ball: Ball):
        d = numpy.linalg.norm(ball.position)
        if d > 1:
            return False
        else:
            return True

    def __loop(self, ball: Ball):
        count = 0.0
        max = 1000000.0
        x_list = []
        y_list = []
        while self.__isInside(ball) and count < max:
            relative_position = self.__relative_position(ball)
            x_list.append(relative_position[0][0])
            y_list.append(relative_position[1][0])
            self.__rotate()
            ball.move()
            count += 1
            print("Límite: {:.2f}%".format(count/max * 100))
        return {"x": x_list, "y": y_list}

    def throw_still(self, ball_position, ball_speed):
        # creates a ball and throws it, better for use only when w is 0
        if self.w != 0:
            raise ValueError("'throw_still' requieres angular speed to be zero.")
        r_x = ball_position[0]
        r_y = ball_position[1]
        v_x = ball_speed[0]
        v_y = ball_speed[1]
        ball = Ball(numpy.array([[r_x], [r_y]]),
                    numpy.array([[v_x], [v_y]]),
                    self.time_step)
        return self.__loop(ball)

    def throw_ball(self, relative_position, ball_speed):
        # relative_position is given as a fraction f of the radius of the cylinder [0, (f-1)*1]
        # speed is given as magnitude relative to spin speed and angle, where 0 is spinwards.
        y = relative_position -1
        alpha = ball_speed[1] * math.pi/180 # degrees to radians
        rotational_speed = abs(y) * self.w
        speed = rotational_speed * ball_speed[0]
        v_x = speed * math.cos(alpha) + rotational_speed # inertia gives it some speed
        v_y = speed * math.sin(alpha)
        ball = Ball(numpy.array([[0], [y]]),
                    numpy.array([[v_x], [v_y]]),
                    self.time_step)
        return self.__loop(ball)

# obtenemos los valores
#cyl = Cylinder(0)
#cyl.throw_still([0.3, 0.1], [0, 0])
time_step = 0.01
cyl = Cylinder(2, time_step)
data = cyl.throw_ball(0.2, [0.8, 135])

# creamos la animacion
fig = plt.figure()
ax = fig.add_subplot(111, aspect='equal', autoscale_on=False,
                     xlim=(-1.1, 1.1), ylim=(-1.1, 1.1))
k = numpy.linspace(0, 2*math.pi, 1000)
x = [math.cos(value) for value in k]
y = [math.sin(value) for value in k]
ax.plot(x, y, marker="o")
line, = ax.plot([], [], marker=".")
time_text = ax.text(0.02, 0.95, "", transform=ax.transAxes)

def init():
    line.set_data([], [])
    time_text.set_text("")
    return line, time_text

def animate(i):
    line.set_data(data["x"][:i], data["y"][:i])
    time_text.set_text("Time: {:.2f}s".format(time_step * i))
    return line, time_text
ani = animation.FuncAnimation(fig, animate, frames=len(data["x"]),
                              interval=time_step, blit=True, init_func=init, repeat=False)

plt.show()
