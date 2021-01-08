import math
import os
import tkinter as tk

from PIL import Image


class SpiderChart(tk.Canvas):
    def __init__(self, master, data, concentrics=10, scale=200, width=500, height=500):
        super().__init__(master, width=width, height=height)
        self.scale = scale
        self.center = width // 2, height // 2  # Tuple

        self.labels = tuple(d[0] for d in data)
        self.values = tuple(d[1] for d in data)

        self.num_pts = len(self.labels)
        self.concentrics = [n / (concentrics) for n in range(1, concentrics + 1)]

        self.draw()

    def position(self, x, y):
        cx, cy = self.center

        return x + cx, cy - y

    def draw_circle_from_radius_center(self, radius):
        rad = radius * self.scale

        x0, y0 = self.position(-rad, rad)
        x1, y1 = self.position(rad, -rad)

        return self.create_oval(x0, y0, x1, y1, dash=(1, 3))

    def draw_label(self, idx, label):
        angle = idx * (2 * math.pi) / self.num_pts
        d = self.concentrics[-1] * self.scale
        x, y = d * math.cos(angle), d * math.sin(angle)

        self.create_line(*self.center, *self.position(x, y), dash=(1, 3))

        d *= 1.1
        x, y = d * math.cos(angle), d * math.sin(angle)

        self.create_text(*self.position(x, y), text=label)

    def draw_polygon(self):
        points = []

        for idx, val in enumerate(self.values):
            d = (val / 100) * self.scale
            angle = idx * (2 * math.pi) / self.num_pts
            x, y = d * math.cos(angle), d * math.sin(angle)

            points.append(self.position(x, y))

        self.create_polygon(points, fill="dark turquoise")

    def draw(self):
        self.draw_polygon()

        for concentric in self.concentrics:
            self.draw_circle_from_radius_center(concentric)

        for idx, label in enumerate(self.labels):
            self.draw_label(idx, label)

    def save_as(self, filename, fmt="png"):
        self.update()
        self.postscript(
            file=f"{filename}.ps", colormode="color",
        )

        img = Image.open(f"{filename}.ps")
        img.save(f"{filename}.{fmt}")

        os.remove(f"{filename}.ps")


class StellarChart(SpiderChart):
    def draw_polygon(self):
        da = math.pi / self.num_pts  # To be between labels
        b = 0.05 * self.scale

        points = []

        for idx, val in enumerate(self.values):
            d = (val / 100) * self.scale
            angle = idx * (2 * math.pi) / self.num_pts
            x, y = d * math.cos(angle), d * math.sin(angle)

            points.append(self.position(x, y))

            xb, yb = b * math.cos(angle + da), b * math.sin(angle + da)

            points.append(self.position(xb, yb))

        self.create_polygon(points, width=3, outline="red", fill="pink", join=tk.ROUND)


if __name__ == "__main__":
    data = [
        ("stamina", 70),
        ("python-skill", 100),
        ("strength", 80),
        ("break-dance", 66),
        ("speed", 45),
        ("health", 72),
        ("healing", 90),
        ("energy", 12),
        ("libido", 100),
    ]

    root = tk.Tk()

    stellar = StellarChart(root, data)
    stellar.pack(side=tk.LEFT)

    spider = SpiderChart(root, data)
    spider.pack(side=tk.LEFT)

    stellar.save_as("stellar_chart")

    root.mainloop()
