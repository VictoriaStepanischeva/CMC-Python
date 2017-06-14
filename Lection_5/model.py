class Particle:
    def __init__(self, x, y, u, v, mass, color, lifetime):
        self.fps = 24
        self.coords = { "x": x, "y": y }
        self.speed = { "u_x": float(u) / self.fps, "v_y": float(v) / self.fps }
        self.a = { "a_x": None, "a_y": None }
        self.mass = mass
        self.color = color
        self.lifetime = self.fps * lifetime


    def __str__(self):
        return "Particle at ({}, {}): m = {}; speed: ({}, {}) acc: ({}, {})".format(
            self.coords["x"], self.coords["y"], self.mass,
            self.speed["u_x"], self.speed["v_y"],
            self.a["a_x"], self.a["a_y"]
        )

    __repr__ = __str__
