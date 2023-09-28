
# number of steps to pass until it prints status
_statusPrintModulo = 100000

#collision grace period
_collisionGracePeriod = 10 #number of steps where collisions are not checked

#dynamic deltat
_computeDeltaClamp = (0 , 5) #(min, max)
_computeDeltaDeltatFactor = 1000


#integrator out of bound
_outOfBoundMin = 1 #fixed to black hole radius
_outOfBoundMax = 30
