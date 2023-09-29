
# number of steps to pass until it prints status
_statusPrintModulo = 100000

#collision grace period
_collisionGracePeriod = 10 #number of steps where collisions are not checked
_debugCollisions = True #prints some info when collisions are detected


#dynamic deltat
_computeDeltaClamp = (0 , 5) #(min, max)
_computeDeltaDeltatFactor = 100


#integrator out of bound
_outOfBoundMin = 1 #fixed to black hole radius
_outOfBoundMax = 100000
