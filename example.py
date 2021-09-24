from polygenerator import (
    random_polygon,
    random_star_shaped_polygon,
    random_convex_polygon,
)


# these two are only for demonstration
import matplotlib.pyplot as plt
import random


def plot_polygon(polygon, out_file_name):
    plt.figure()
    plt.gca().set_aspect("equal")

    for i, (x, y) in enumerate(polygon):
        plt.text(x, y, str(i), horizontalalignment="center", verticalalignment="center")

    # just so that it is plotted as closed polygon
    polygon.append(polygon[0])

    xs, ys = zip(*polygon)
    plt.plot(xs, ys, "r-", linewidth=0.4)

    plt.savefig(out_file_name, dpi=300)
    plt.close()


# this is just so that you can reproduce the same results
random.seed(5)

polygon = random_polygon(num_points=20)

print(polygon)
# [(0.633385213909564, 0.7365967958574935), (0.5480555383950588, 0.6616499553124763), (0.5526824773965012, 0.5399082630833278), (0.47651656975044715, 0.1562847171200224), (0.211780263278101, 0.11985024210702566), (0.011563117103044742, 0.12131343894869698), (0.02776777678478965, 0.41297620242381444), (0.2831882595429206, 0.9411514041596818), (0.0, 0.8884881505484779), (0.20701109399057388, 0.9700145767610514), (0.2932049212796463, 0.9940396395241987), (0.7024623622191127, 1.0), (0.809077387585075, 0.9717422011442743), (1.0, 0.889663530991249), (0.9601646445268924, 0.6278354104701399), (0.9168705153810578, 0.0), (0.8110693657038247, 0.02995395054812518), (0.6278284961406966, 0.01581195981039065), (0.7790276993942304, 0.05437135270534656), (0.752691110661913, 0.948158571633034)]

plot_polygon(polygon, "random_polygon.png")


polygon = random_star_shaped_polygon(num_points=20)
plot_polygon(polygon, "random_star_shaped_polygon.png")


polygon = random_convex_polygon(num_points=20)
plot_polygon(polygon, "random_convex_polygon.png")
