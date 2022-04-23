from solid import *
from solid.utils import *
import numpy as np
import itertools
import functools as fn 
import qrcode
import colour
from typing import NamedTuple

np.random.seed(47)
EPS = 0.001
BOX_DOT_WITH = 1 
BOX_DOT_HEIGHT = 2 
TAZA_WIDTH = 10 
TAZA_HEIGHT = 15 
HANDLE_WITHT = 2
HANDLE_HEIGHT = 10 
HANDLE_OUT = -1 
HANDLE_SCALE = 1.2
TAZA_BORDER = 1.0

def qr_shape_from_data(data: str) -> OpenSCADObject:
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=2,
    )
    qr.add_data(data)

    qr.make(fit=True)
    qr_matrix = np.array(qr.get_matrix())
    r = np.random.randn
    qr = [(translate([i * BOX_DOT_WITH - EPS, k * BOX_DOT_WITH - EPS, 0])
            (cube([BOX_DOT_WITH + 2 * EPS, BOX_DOT_WITH + 2 * EPS, BOX_DOT_HEIGHT])))
            for i, k in np.ndindex(qr_matrix.shape)
            if not qr_matrix[i, k]]

    qr = [color([0.5, 0.4, 0.4])(c) for c in qr]
    qr_shape = fn.reduce(lambda a, b: a + b, qr) 
    return qr_shape


class CoffeCupInfo(NamedTuple):
    cup: OpenSCADObject
    hole: OpenSCADObject

def coffe_cup() -> CoffeCupInfo: 
    taza = square([TAZA_WIDTH, TAZA_WIDTH], center=True)
    taza = linear_extrude(height=TAZA_HEIGHT, scale=2.0)(taza)

    taza_hole = square([TAZA_WIDTH - TAZA_BORDER, TAZA_WIDTH - TAZA_BORDER], center=True)
    taza_hole = linear_extrude(height=TAZA_HEIGHT + EPS, scale=2.0)(taza_hole)
    taza_hole = translate([0, 0, TAZA_BORDER])(taza_hole)

    handle = cube([HANDLE_HEIGHT, HANDLE_WITHT, HANDLE_HEIGHT])
    handle_triangle_drill = rotate([0, 45, 0])(cube([HANDLE_HEIGHT + 2 * EPS, HANDLE_WITHT + 2 * EPS, HANDLE_HEIGHT]))
    handle = handle - translate([HANDLE_HEIGHT / 2 - EPS, -EPS, 0])(handle_triangle_drill)
    handle = scale([HANDLE_SCALE, 1, 1])(handle)

    handle = translate([HANDLE_WITHT + TAZA_WIDTH + HANDLE_OUT, TAZA_WIDTH , TAZA_HEIGHT / 3])(handle)
    taza = translate([TAZA_WIDTH, TAZA_WIDTH, 0])(taza)
    taza_hole = translate([TAZA_WIDTH, TAZA_WIDTH, 0])(taza_hole)
    return CoffeCupInfo(cup = taza + handle - taza_hole,
                        hole = taza_hole)

qr = translate([TAZA_BORDER * 2, TAZA_BORDER * 2, TAZA_HEIGHT - EPS * 4])(
        (scale(0.68)(qr_shape_from_data("random link")))
        )

drink = translate([TAZA_BORDER, TAZA_BORDER, 0])(scale(0.95)(coffe_cup().hole))

scad_render_to_file( qr + drink, "result.scad")



