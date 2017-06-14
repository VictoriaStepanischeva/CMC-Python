import math
import model
import cython_verlet
import threading
import numpy
from scipy.integrate import odeint
import matplotlib.pyplot as plot
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

def verlet(particles):
    G = 6.67 * (10 ** -11)
    for p in particles:
        new_x = sum(map(lambda e:
            G * e.mass * (e.coords['x'] - p.coords['x'])
            / (math.sqrt(
                (e.coords['x'] - p.coords['x'])**2 +
                (e.coords['y'] - p.coords['y'])**2
            )) , filter(lambda e: not e is p, particles)
        ))
        new_y = sum(map(lambda e:
            G * e.mass * (e.coords['y'] - p.coords['y'])
            / (math.sqrt(
                (e.coords['x'] - p.coords['x'])**2 +
                (e.coords['y'] - p.coords['y'])**2
            )), filter(lambda e: not e is p, particles)
        ))
        if not (p.a['a_x'] is None and p.a['a_y'] is None):
            p.coords['x'] += p.speed['u_x'] + 0.5 * p.a['a_x']
            p.coords['y'] += p.speed['v_y'] + 0.5 * p.a['a_y']
        p.lifetime -= 1
        p.speed['u_x'] += 0.5 * (0 if p.a['a_x'] is None else p.a['a_x'] + new_a_x)
        p.speed['v_y'] += 0.5 * (0 if p.a['a_y'] is None else p.a['a_y'] + new_a_y)
        p.a['a_x'] = new_a_x
        p.a['a_y'] = new_a_y
    return [p.coords for p in particles]

def verlet_worker(particles, begin, end):
    G = 6.67 * (10 ** -11)
    for p in particles[begin : end]:
        new_a = sum(map(lambda e:
            G * e.mass * (e.coords['x'] - p.coords['x'])
            / (math.sqrt(
                (e.coords['x'] - p.coords['x'])**2 +
                (e.coords['y'] - p.coords['y'])**2
            )) , filter(lambda e: not e is p, particles)
        ))
        new_b = sum(map(lambda e:
            G * e.mass * (e.position['y'] - p.position['y'])
            / (math.sqrt(
                (e.position['x'] - p.position['x'])**2 +
                (e.position['y'] - p.position['y'])**2
            )), filter(lambda e: not e is p, particles)
        ))
        if not (p.a['a_x'] is None and p.a['a_y'] is None):
            p.coords['x'] += p.speed['u_x'] + 0.5 * p.a['a_x']
            p.coords['y'] += p.speed['v_y'] + 0.5 * p.a['a_y']
        p.lifetime -= 1
        p.speed['u_x'] += 0.5 * (0 if p.a['a_x'] is None else p.a['a_x'] + new_a_x)
        p.speed['v_y'] += 0.5 * (0 if p.a['a_y'] is None else p.a['a_y'] + new_a_y)
        p.a['a_x'] = new_a_x
        p.a['a_y'] = new_a_y

def threads(particles):
    procs = []
    for i in range(len(particles)):
        proc = threading.Thread(target = verlet_worker, args = (particles, i, i+1))
        proc.start()
        procs.append(proc)
    for j in procs:
        j.join()
    return [p.coords for p in particles]

class ParticleController:
    defaults = {
        'mass': 1250 * 1000,
        'lifetime': 4,
        'speed': {'u_x': 5, 'v_y': 7},
        'coords': {'x': 0, 'y': 0},
        'a' : None,
        'color': (1, 0, 0),
        'method': 0
    }

    def __init__(self):
        self._mass = __class__.defaults['mass']
        self._lifetime = __class__.defaults['lifetime']
        self._speed = __class__.defaults['speed']
        self._coords = __class__.defaults['coords']
        self._color = __class__.defaults['color']
        self.method = __class__.defaults['method']
        self.particles = []
        self.updaters = [
            verlet,
            cython_verlet.cython_verlet,
            threads,
            lambda particles: [ p.coords for p in particles ]
        ]
        self.methods = [
            "Verlet",
            "Cython",
            "Multiprocess",
        ]

    def __add_particle(self):
        self.particles.append(model.Particle(
            self.coords['x'], self.coords['y'],
            self.speed['u_x'], self.speed['v_y'],
            self.mass, self.color, self.lifetime
        ) )

    @property
    def coords(self):
        return self._coords

    @coords.setter
    def coords(self, value):
        self._coords = value

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        self._speed = value

    @property
    def a(self):
        return self._a

    @a.setter
    def a(self, value):
        self._a = value

    @property
    def mass(self):
        return self._mass

    @mass.setter
    def mass(self, value):
        self._mass = value

    @property
    def lifetime(self):
        return self._lifetime

    @lifetime.setter
    def lifetime(self, value):
        self._lifetime = value

    @property
    def color(self):
        return self._color

    @color.setter
    def color_set(self, value):
        self._color = value


class ParticlePlot(FigureCanvasQTAgg):
    def __init__(self, parent, width, height, dpi, size_policy):
        figure = Figure(figsize = (width, height), dpi = dpi, facecolor = 'white')
        self.axes = figure.add_axes([0.005,0.005,0.990,0.990], frameon=True, aspect=1)
        FigureCanvasQTAgg.__init__(self, figure)
        self.setParent(parent)
        FigureCanvasQTAgg.setSizePolicy(self, size_policy, size_policy)
        FigureCanvasQTAgg.updateGeometry(self)
        self.figure.canvas.draw()

    def update_plot(self, particles, updater):
        self.axes.cla()
        self.axes.set_xlim(-25, 25), self.axes.set_xticks([])
        self.axes.set_ylim(-25, 25), self.axes.set_yticks([])
        data = updater(particles)
        mass_data = [p.mass / 1000 for p in particles if p]
        color_data = [p.color for p in particles if p]
        x_data = [ p['x'] for p in data if p ]
        y_data = [ p['y'] for p in data if p ]
        self.scatter = self.axes.scatter(x_data, y_data, s = mass_data, lw = 0.5,
            c = color_data)
        self.figure.canvas.draw()

