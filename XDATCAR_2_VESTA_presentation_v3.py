# KG 7/17/2021

import numpy as np

###################### Input variables
# put the name and address to the XDARCAR file here
filename = "../XDATCAR_40atoms_1100C"
# write the species name that you want the trajectory for
species_to_track = 'O'
# output the coordinates of the desired species every this timestep
every_this = 100
######################

# Outfile initiation
out = []

# Open XDATCAR
with open(filename, "r") as f:
    lines = f.readlines()
    for i in np.arange(0,8,1):
        out.append(lines[i])
    out[7] = "Direct\n"

    # Read the atom species
    templ = lines[5].split() 
    atomsp = []
    Nspecies = len(templ)
    for i in range(0,Nspecies,1):
        atomsp.append(templ[i])

    # Read the atom numbers for each species
    templ = lines[6].split()
    atomNs = np.empty(0, dtype='int')
    for i in range(0,Nspecies,1):
        atomNs = np.append(atomNs, int(templ[i]))
    Natoms = np.sum(atomNs)

    # finding N1 & N2 indices corresponding to species_to_track
    N1 = N2 = 0
    for i in np.arange(0,Nspecies):
        temp = N2
        N2 += atomNs[i]
        N1 = temp
        if (atomsp[i] == species_to_track): 
            break

    # Calculating the number of snapshots available in the XDATCAR
    Ntimes = int(np.floor((len(lines)-7)/(Natoms+1)))
    print("\nTotal number of snapshots in the XDATCAR: %d\n" % (Ntimes))

    countl = 7
    count_line_species_track = 0 # tracking the number of lines added to the end of POSCAR to track the species of interest
    for n in np.arange(0,Ntimes,1):
        countl += 1 # ignore the Direct Configuration line
        if n==0: # for the first snapshot read all the lines
            for i in range(0,Natoms,1):
                out.append(lines[countl])
                countl += 1
        else:
            for i in range(0,Natoms,1):
                if i>=N1 and i<N2:
                    if n % every_this == 0:
                        out.append(lines[countl])
                        count_line_species_track += 1
                countl += 1

# Wrting a comment in the first line
out[0] = "POSCAR made from XDATCAR by tracking species: " + species_to_track + "\n"
# Correcting the species line in the new POSCAR
atomsp.append('He')
s = ""
for i in np.arange(0,len(atomsp),1):
    s += '%7s' % (atomsp[i])
s += "\n"
out[5] = s

# Correcting the number of elements in the new POSCAR
atomNs = np.append(atomNs,count_line_species_track)
s = ""
for i in np.arange(0,len(atomNs),1):
    s  += '%7d' % (atomNs[i])
s += "\n"
out[6] = s

# save and close the open files
f.close()
out_file = open("POSCAR_tracked_species", "w")
out_file.writelines(out)
out_file.close()

