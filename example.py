from polygenerator import (
    random_polygon,
    random_star_shaped_polygon,
    random_convex_polygon,
)

from plot import plot_polygon

# this is just so that you can reproduce the same results
import random

random.seed(5)


polygon = random_polygon(num_points=20)

print(polygon)
# [(0.752691110661913, 0.948158571633034), (0.7790276993942304, 0.05437135270534656), ..., (0.633385213909564, 0.7365967958574935)]

plot_polygon(polygon, "random_polygon.png")


polygon = random_star_shaped_polygon(num_points=20)
plot_polygon(polygon, "random_star_shaped_polygon.png")


polygon = random_convex_polygon(num_points=20)
plot_polygon(polygon, "random_convex_polygon.png")
