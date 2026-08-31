"""
Draw the filter bandpass figure used on the homepage.

This is a one-off: run it if you want to change which filters are shown,
then commit the regenerated _includes/bandpasses.svg.

    python scripts/make_bandpass_figure.py
"""

import numpy as np

# JWST NIRCam filters: name, pivot wavelength in microns, width in microns.
wide_filters = [
    ("F115W", 1.15, 0.23),
    ("F150W", 1.50, 0.32),
    ("F200W", 1.99, 0.46),
    ("F277W", 2.76, 0.68),
    ("F356W", 3.57, 0.79),
    ("F444W", 4.40, 1.02),
]

medium_filters = [
    ("F182M", 1.85, 0.24),
    ("F210M", 2.09, 0.21),
    ("F250M", 2.50, 0.18),
    ("F300M", 2.99, 0.32),
    ("F335M", 3.36, 0.35),
    ("F410M", 4.08, 0.44),
]

# Colours match the three research topics plus the site accent.
medium_colours = ["#3b4c99", "#3b4c99", "#1b6f62", "#1b6f62", "#4a2545", "#a32e1e"]

WIDTH = 1000.0
HEIGHT = 196.0
LEFT = 10.0
RIGHT = 990.0
BASE = 168.0
TOP = 22.0

LAM_MIN = 0.85
LAM_MAX = 5.10


def to_x(lam):
    """Wavelength in microns to horizontal position in the drawing."""
    frac = (lam - LAM_MIN) / (LAM_MAX - LAM_MIN)
    return LEFT + frac * (RIGHT - LEFT)


def to_y(throughput):
    """Throughput between 0 and 1 to vertical position in the drawing."""
    return BASE - throughput * (BASE - TOP)


def band_path(pivot, width, peak):
    """A smooth bump standing in for one filter transmission curve."""
    sigma = width / 2.2
    lam = np.linspace(pivot - 3.0 * sigma, pivot + 3.0 * sigma, 90)
    throughput = peak * np.exp(-0.5 * ((lam - pivot) / sigma) ** 2)

    points = []
    for i in range(len(lam)):
        points.append("{:.1f},{:.1f}".format(to_x(lam[i]), to_y(throughput[i])))

    return "M " + " L ".join(points)


lines = []
lines.append('<svg viewBox="0 0 {:.0f} {:.0f}" xmlns="http://www.w3.org/2000/svg" '
             'role="img" aria-label="Transmission curves of JWST NIRCam wide and '
             'medium band filters between 1 and 5 microns">'.format(WIDTH, HEIGHT))

# Wide filters sit behind, in a neutral grey.
lines.append('<g fill="currentColor" opacity="0.075" class="band-fill">')
for name, pivot, width in wide_filters:
    path = band_path(pivot, width, 0.62)
    closing = " L {:.1f},{:.1f} L {:.1f},{:.1f} Z".format(
        to_x(pivot + 1.4 * width), BASE, to_x(pivot - 1.4 * width), BASE)
    lines.append('<path d="{}{}"/>'.format(path, closing))
lines.append("</g>")

# Medium filters sit in front, in the topic colours.
for i in range(len(medium_filters)):
    name, pivot, width = medium_filters[i]
    colour = medium_colours[i]
    lines.append('<path class="band-line" d="{}" fill="none" stroke="{}" '
                 'stroke-width="2" stroke-linejoin="round"/>'.format(
                     band_path(pivot, width, 0.92), colour))

# Baseline and wavelength ticks.
lines.append('<line x1="{:.1f}" y1="{:.1f}" x2="{:.1f}" y2="{:.1f}" '
             'stroke="currentColor" stroke-width="1" opacity="0.3"/>'.format(
                 LEFT, BASE, RIGHT, BASE))

for lam in [1, 2, 3, 4, 5]:
    x = to_x(lam)
    lines.append('<line x1="{:.1f}" y1="{:.1f}" x2="{:.1f}" y2="{:.1f}" '
                 'stroke="currentColor" stroke-width="1" opacity="0.3"/>'.format(
                     x, BASE, x, BASE + 5))
    lines.append('<text class="tick-label" x="{:.1f}" y="{:.1f}" fill="currentColor" '
                 'opacity="0.55" font-family="Public Sans, sans-serif" font-size="12" '
                 'text-anchor="middle">{}</text>'.format(x, BASE + 20, lam))

lines.append("</svg>")

with open("_includes/bandpasses.svg", "w") as f:
    f.write("\n".join(lines) + "\n")

print("wrote _includes/bandpasses.svg")
