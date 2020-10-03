# programme d'initialisation
print DEBUT DE LA SIMULATION

busy 10
fork 
exec process_1.s

print on essaye ca
print entree dans une boucle
fork 
exec boucle_1.s

print on a quitté les boucles
