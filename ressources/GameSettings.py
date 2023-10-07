steps_per_frame = 1 #please do not change or the time spent between 


out_of_bound = 40 # distance from the blackhole at which the ship is oncisdered out of bound

# defines what a player starts with.
starting_inventory = {
    "Heavy" : 5,
    "Light" : 5
}


# enables or disables periodic boundary conditons.
periodic_boundary_condition_is_active = True


# ======== COLOR TABLE ==========
# # https://keiwando.com/color-picker/
# assigns a colorr to an object type. 
# color names type are used for debug or if you wish
# to use the simulation for other things. the renderer understands those colors
color_table = {
            "red" : [1, 0, 0],
            "green": [0, 1, 0],
            "blue": [0, 0, 1],
            "cyan": [0, 1, 1],
            "pink": [1, 0, 1],
            "white":[1, 1, 1],
            "yellow": [1, 1, 0],
            "orange": [1, 0.5, 0],
            "neongreen": [0.31, 0.92, 1],
            "black": [0, 0, 0],

            "Ship": [0,1,0],
            "Heavy": [0.11, 0.62, 0.99],
            "Light": [1.00, 0.67, 0.22],
            "Target": [1.00, 0.17, 0.00]
        }


#========= PROJECTILES DEFAULT VALUES =======
#default raidus are set to 0.5 for display reasons. Raiduses are not passed
#to the shader, thus not rendered to the right size. currently hardcoded to 0.5
projectiles_default = {
    "Heavy" : {
        "mass": 2.5e4,
        "radius": 0.5,
        "speed": 0.4
    },

    "Light" : {
        "mass": 500,
        "radius": 0.5,
        "speed": 0.5
    }
}


#========= AESTHETICSSSSS =========
#still experimental but these values give a somehat good result
background_color = [0.05, 0.13, 0.18]
# background_color = [33/255, 33/255, 33/255]
fade_off = 0.03
color_distance_treshold = 0.2
# ^ will reimplement the background color, will have to do for now



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