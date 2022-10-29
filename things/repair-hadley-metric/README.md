# Overview

These are various bits used to build the [Hadley Telescope by Maff](https://www.printables.com/model/224383-astronomical-telescope-hadley-an-easy-assembly-hig)
on metric hardware. I have started with the [Official Metric Remix](https://www.printables.com/model/259710-hadley-official-m4metric-remix),
which is mostly adjusted for M4 screws and 12 mm rods, and adjusted as needed.

# Printing

Everything printed with variable layer height, 0.2 mm base profile,
3 perimeters, minimum 1.2 mm bottom and top shell, 30% gyroid infill.

When printing the spider, I have used the `WrapSpiderNut` pieces to house
M4 nuts inside the larger holes of the print. In my copy, I was putting
the pieces with the plastic side up, and for the second layer, made
sure M4 bolts can be threaded all the way to the first layer.
After printing, the M4 bolts encounter slight resistance,
similar to that encountered with nyloc nuts, which
I guess is fine.

# Assembly

As advised in the original model comments, I have used M4 metric nuts
and bolts everywhere. The assembly appears sturdy enough, although
perhaps M5 would have been a better choice in some places. The
rods are 12 mm OD, 2 mm wall, aluminium.

For the primary mirror holder bolts, I used M4x50 HX in plastic inserts
from the original model, 3 pieces needed. The assembly sketch for the
original model strangely suggests placing bolts with their heads in
the inserts and shafts pointing towards the mirror, this felt
upside down so I put the heads in the `Cell` piece with
the shafts sticking away from the mirror.

The center piece with the rocker worked perfectly with
M4 nuts and M4x16 FH bolts, 8 pieces needed.

The spider assembly was perhaps the strangest, with the middle bolt
working against the collimation nuts and the spring apparently not
useful. I would have expected the spring to pull the secondary
mirror towards the spider, and the collimation bolts pushing
away, but that is obviously not the intended design.
In the end, I have placed the middle bolt shaft inside `WrapSpiderBolt`, terminated with a nyloc nut to prevent the secondary mirror holder from rotating freely,
and added `SpiderBoltGuide` to better align the collimation bolts, inspired by [this design](https://www.printables.com/model/266322-hadley-secondary-mirror-holder-m4-slotted-bolt-rem).

The `WrapFocuserNut` is for the focuser nuts, which are otherwise too wobbly.

For the overall dimensions, the distance between the outer edges of the top
and the bottom assemblies in my scope is 855 mm, I have used 995 mm rods
and have the ends sticking out equally on both scope ends.

Although I did have the sights printed, in the end I have removed them.
It seems easy enough to point the scope using the bolt heads sticking
out from the assemblies. If I were to use the sights, I would opt
for the [versions with support rings](https://www.printables.com/model/237379-hadley-114900-telescope-remix).

# Stand

With four 495 mm rods left over from my purchase (the rods were cut from 6000 mm piece),
I have modified [this rocker frame](https://www.printables.com/model/262764-hadley-telescope-rocker-frame)
to accept 12 mm OD rods, the `WrapStandNut` helps with M4 nuts and bolts. I have also made the bottom part
somewhat sturdier so that it does not need the wood base. Overall, my experience with the stand is
acceptable, but viewing does suffer from vibrations when the stand wobbles on uneven ground, so
a heavier wood base as shown in other makes is probably more reasonable.

The `ShelfStand` model is for when I want to put the scope on a shelf.

# Collimation

I was worried about collimation but in the end it went surprisingly well and took just a few minutes.

I have used the [center spot finder model](https://www.printables.com/model/245036-center-spot-finder) to mark the primary mirror center, a marker has served instead of a round sticker seen on many pictures.

The `CollimationCap` model is inspired by the [advanced collimation cap model](https://www.printables.com/model/8465-advanced-telescope-collimation-cap), with the rim removed for easier printing and the outer shell made longer to reach as far as the focuser bolts.
