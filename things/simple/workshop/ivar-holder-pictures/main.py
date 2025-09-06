#!/usr/bin/env python3

from solid import *
from solid.utils import *

from helpers import ivar

SEGMENTS = 33


HOLDER_WIDTH = 11

CATCH_OVERLAP_UPPER = ivar.SHELF_HEIGHT
CATCH_OVERLAP_LOWER = ivar.SHELF_HEIGHT
CATCH_THICKNESS = 6.66

ARM_THICKNESS = 0.86

HOOK_GAP = 2.2
HOOK_WIDTH = 6.66
HOOK_HEIGHT = 6.66
HOOK_THICKNESS = 2.2


def hanger (length):

    catch_upper = cube ((CATCH_OVERLAP_UPPER + CATCH_THICKNESS, HOLDER_WIDTH, CATCH_THICKNESS))
    catch_upper = translate ((0 - CATCH_THICKNESS, 0, ivar.SHELF_HEIGHT)) (catch_upper)

    catch_side = cube ((CATCH_THICKNESS, HOLDER_WIDTH, ivar.SHELF_HEIGHT + 2*CATCH_THICKNESS))
    catch_side = translate ((0 - CATCH_THICKNESS, 0, 0 - CATCH_THICKNESS)) (catch_side)

    catch_lower = cube ((CATCH_OVERLAP_LOWER + CATCH_THICKNESS, HOLDER_WIDTH, CATCH_THICKNESS))
    catch_lower = translate ((0 - CATCH_THICKNESS, 0, 0 - CATCH_THICKNESS)) (catch_lower)

    catch = catch_upper + catch_side + catch_lower

    arm = cube ((ARM_THICKNESS, HOLDER_WIDTH, length))
    arm = translate ((CATCH_OVERLAP_LOWER, 0, 0 - length)) (arm)

    tip_height = (HOLDER_WIDTH - HOOK_WIDTH)/2
    tip = polygon ([(0, 0), (HOLDER_WIDTH, 0), (HOLDER_WIDTH/2 + HOOK_WIDTH/2, tip_height), (HOLDER_WIDTH/2 - HOOK_WIDTH/2, tip_height)])
    tip = linear_extrude (ARM_THICKNESS) (tip)

    bar = cube ((HOOK_WIDTH, HOOK_WIDTH, HOOK_GAP))
    bar = translate ((HOLDER_WIDTH/2 - HOOK_WIDTH/2, tip_height - HOOK_WIDTH, ARM_THICKNESS)) (bar)

    bin = cube ((HOOK_WIDTH, HOOK_WIDTH + HOOK_HEIGHT, HOOK_THICKNESS))
    bin = translate ((HOLDER_WIDTH/2 - HOOK_WIDTH/2, tip_height - HOOK_WIDTH - HOOK_HEIGHT, ARM_THICKNESS + HOOK_GAP)) (bin)

    hook = tip + bar + bin

    hook = rotate ((270, 0, 90)) (hook)
    hook = translate ((CATCH_OVERLAP_LOWER + ARM_THICKNESS, 0, 0 - length)) (hook)

    return catch + arm + hook


for length in range (20, 100, 10):
    scad_render_to_file (hanger (length), f'hanger-{length}.scad', file_header = f'$fn = {SEGMENTS};')
