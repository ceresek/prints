#!/usr/bin/env python3

from solid import *

from components.common import OVERLAP


SEGMENTS = 66


PIPE_DIAMETER = 50
HOLE_DIAMETER = 9.8

BALD_DIAMETER = 14
HEAD_DIAMETER = 26
HEAD_THICKNESS = 2.2
HEAD_SEPARATION_HATTED = 2.2
HEAD_SEPARATION_GASKET = 2.0

CATCH_EXTENSION = 0.8
CATCH_REDUCTION = 1.3
CATCH_ATTACK = 1
CATCH_DECAY = 8

GROOVE_WIDTH = 3.33
GROOVE_HEIGHT = 30


# Components

def stalk (separation):

    body = cylinder (HOLE_DIAMETER/2, PIPE_DIAMETER + separation)
    body = translate ((0, 0, 0 - separation)) (body)

    tip_attack = cylinder (r1 = HOLE_DIAMETER/2, r2 = HOLE_DIAMETER/2 + CATCH_EXTENSION, h = CATCH_ATTACK)

    tip_decay = cylinder (r1 = HOLE_DIAMETER/2 + CATCH_EXTENSION, r2 = HOLE_DIAMETER/2 - CATCH_REDUCTION, h = CATCH_DECAY)
    tip_decay = translate ((0, 0, CATCH_ATTACK)) (tip_decay)

    tip_wrap_height = CATCH_ATTACK + CATCH_DECAY
    tip_wrap = cube ((HOLE_DIAMETER + 2*CATCH_EXTENSION, HOLE_DIAMETER, tip_wrap_height), center = True)
    tip_wrap = translate ((0, 0, tip_wrap_height/2)) (tip_wrap)

    tip = (tip_attack + tip_decay) * tip_wrap
    tip = translate ((0, 0, PIPE_DIAMETER)) (tip)

    groove_slot = cube ((GROOVE_WIDTH, HOLE_DIAMETER + 2*CATCH_EXTENSION + 2*OVERLAP, GROOVE_HEIGHT + OVERLAP), center = True)
    groove_slot = translate ((0, 0, GROOVE_HEIGHT/2)) (groove_slot)

    groove_depth = HOLE_DIAMETER + 2*CATCH_EXTENSION + 2*OVERLAP
    groove_bottom = cylinder (GROOVE_WIDTH/2, groove_depth)
    groove_bottom = rotate ((270, 0, 0)) (groove_bottom)
    groove_bottom = translate ((0, 0 - groove_depth/2, 0)) (groove_bottom)

    groove = groove_slot + groove_bottom
    groove = translate ((0, 0, PIPE_DIAMETER + CATCH_ATTACK + CATCH_DECAY - GROOVE_HEIGHT)) (groove)

    stalk = body + tip - groove

    return stalk


def pin_with_hat ():

    head_outer = cylinder (HEAD_DIAMETER/2, HEAD_THICKNESS + HEAD_SEPARATION_HATTED + PIPE_DIAMETER/2)
    head_outer = translate ((0, 0, 0 - HEAD_THICKNESS - HEAD_SEPARATION_HATTED)) (head_outer)

    head_inner = cylinder (HEAD_DIAMETER/2 - HEAD_THICKNESS, PIPE_DIAMETER/2 + HEAD_SEPARATION_HATTED + OVERLAP)
    head_inner = translate ((0, 0, 0 - HEAD_SEPARATION_HATTED)) (head_inner)

    head_wrap = cylinder (PIPE_DIAMETER/2, HEAD_DIAMETER)
    head_wrap = rotate ((0, 90, 0)) (head_wrap)
    head_wrap = translate ((0 - HEAD_DIAMETER/2, 0, PIPE_DIAMETER/2)) (head_wrap)

    head = head_outer - head_inner - head_wrap

    pin = head + stalk (HEAD_SEPARATION_HATTED)

    return pin


def pin_bald_pin ():

    head = cylinder (BALD_DIAMETER/2, HEAD_THICKNESS)
    head = translate ((0, 0, 0 - HEAD_THICKNESS - HEAD_SEPARATION_GASKET)) (head)

    pin = head + stalk (HEAD_SEPARATION_GASKET)

    return pin


# Main

scad_render_to_file (pin_with_hat (), 'pin-with-hat.scad', file_header = f'$fn = {SEGMENTS};')
scad_render_to_file (pin_bald_pin (), 'pin-bald-pin.scad', file_header = f'$fn = {SEGMENTS};')
