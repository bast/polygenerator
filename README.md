[![license](https://img.shields.io/badge/license-%20MIT-blue.svg)](LICENSE)
[![test status](https://github.com/bast/polygenerator/workflows/Test/badge.svg)](https://github.com/bast/polygenerator/actions)


# polygenerator

Generates random polygons. This can be useful to test computational geometry
algorithms or to generate maps.


## Installation

...


## Example

...


## API

There are 3 functions and each returns a list of (x, y) tuples:
```
- `random_convex_polygon(num_points)`
- `random_polygon(num_points)`
- `random_star_shaped_polygon(num_points)`
```

The generated polygon is made to fit the bounding box (0.0, 0.0) ... (1.0, 1.0)
and you can then scale and translate it to where you need it.


## Notes

- For the generation of a concave/general polygon, algorithms with better
  scaling exist but this was good enough for me since for testing I did not
  need polygons with more than 100 points. Improvements welcome.
