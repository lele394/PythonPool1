
# number of steps to pass until it prints status
conf_statusPrintModulo = 100000
conf_statusDebug = False

#collision grace period
conf_collisionGracePeriod = 0 #number of steps where collisions are not checked
conf_debugCollisions = False #prints some info when collisions are detected


#dynamic deltat
conf_computeDeltaClamp = (0 , 5) #(min, max), no longer used
conf_computeDeltaDeltatFactor = 1000 #number of sample points on an orbit. the higher, the more precise the simulation.


#integrator out of bound
conf_outOfBoundMin = 1 #fixed to black hole radius
conf_outOfBoundMax = 50
