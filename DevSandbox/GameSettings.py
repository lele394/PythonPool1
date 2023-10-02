steps_per_frame = 1 #please do not change or the time spent between 


"""
Visual aid for win/loss conditions

collisions truth table:

type1   type2   result

heavy   light   both destroy
heavy   heavy   elastic
heavy   target  elastic
heavy   ship    elastic

light   light   both destroy
light   heavy   both destroy
light   target  game win
light   ship    game loss

target  heavy   elastic
target  light   game win
target  ship    game win   <- we assume a game win as the ship can easily destroy the target from CQC

ship    heavy   elastic
ship    light   game loss
ship    target  game win   <- we assume a game win as the ship can easily destroy the target from CQC


when elastic is detected, we don't do anything as it is the default behvior of objects












"""