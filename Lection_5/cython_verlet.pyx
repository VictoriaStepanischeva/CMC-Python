import math

def cython_verlet(particles):
    G_num = 0.0667
    G_den = 1000000000
    for i in range(len(particles)):
        p = particles[i]
        new_a_x = new_a_y = 0
        for j in range(len(particles)):
            if j != i:
                e = particles[j]
                new_a_x += G_num * e.mass *                            \
                    (e.coords['x'] - p.coords['x'])          \
                    / (math.sqrt(                                \
                        (e.coords['x'] - p.coords['x'])**2 + \
                        (e.coords['y'] - p.coords['y'])**2   \
                    ) * G_den)
                new_a_y += G_num * e.mass *                            \
                    (e.coords['y'] - p.coords['y'])          \
                    / (math.sqrt(                                \
                        (e.coords['x'] - p.coords['x'])**2 + \
                        (e.coords['y'] - p.coords['y'])**2   \
                    ) * G_den)

        if not (p.a['a_x'] is None and p.a['a_y'] is None):
            p.coords['x'] += p.speed['u_x'] + 0.5 *p.a['a_x']
            p.coords['y'] += p.speed['v_y'] + 0.5 *p.a['a_y']
        p.lifetime -= 1
        p.speed['u_x'] += 0.5 * (0 if p.a['a_x'] is None else p.a['a_x'] + new_a_x)
        p.speed['v_y'] += 0.5 * (0 if p.a['a_y'] is None else p.a['a_y'] + new_a_y)
        p.a['a_x'] = new_a_x
        p.a['a_y'] = new_a_y
    return [p.coords for p in particles]
