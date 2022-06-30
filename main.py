# This is a Python script to calculate jun-ChS energy.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

#Create a file to complete with energy values
import os.path


def gen_input_file():

    global filename
    status = True
    filename = input('Please insert name for input energy file: \n') + ".txt"
    f = open(filename, "a")
    filesize = os.path.getsize(filename)
    if filesize == 0:
        status = False
        f.write("#Insert here energy values \n")
        f.write("#Most accurate value to be corrected:\n")
        f.write("CCSD(T)/jun-cc-pVTZ = \n")
        f.write("#Energy values at HF level for the calculation of HF energy at CBS limit:\n")
        f.write("HF/jun-cc-pVTZ = \n")
        f.write("HF/jun-cc-pVQZ = \n")
        f.write("HF/jun-cc-pV5Z = \n")
        f.write("#Energy values at MP2 level for the calculation of MP2 energy at CBS limit, note that when corr only correlation energy is needed:\n")
        f.write("MP2/jun-cc-pVTZ = \n")
        f.write("MP2corr/jun-cc-pVTZ = \n")
        f.write("MP2corr/jun-cc-pVQZ = \n")
        f.write("#Energy values at MP2 level for the core-valence correlation estimate\n")
        f.write("MP2/ae = \n")
        f.write("MP2/fc = \n")

    f.close()

    return (filename, status)

#Read in energy values from previously generated file
def extract_energy_values():

    global energy_values
    energy_values = list()
    with open(filename) as f:
        for line in f:
            li=line.strip()
            if not li.startswith("#"):
                energy_values.append(float(line.partition("=")[2]))

    return (energy_values)

def calculate_jChS():

    global HF_CBS
    global Delta_MP2_CBS
    global E_CV
    global E_jChS

    #First extrapolate HF/CBS
    HF_jTZ = energy_values[1]
    HF_jQZ = energy_values[2]
    HF_j5Z = energy_values[3]

    HF_CBS = ((HF_j5Z*HF_jTZ) - (HF_jQZ**2))/(HF_j5Z - (HF_jQZ*2) + HF_jTZ)

    #Then proceed with the extrapolated MP2/CBS
    MP2_jTZ = energy_values[4]
    MP2corr_jTZ = energy_values[5]
    MP2corr_jQZ = energy_values[6]

    MP2corr_CBS = ((4**3)*MP2corr_jQZ - (3**3)*MP2corr_jTZ) / ((4**3) - (3**3))
    Delta_MP2_CBS = HF_CBS + MP2corr_CBS - MP2_jTZ

    #Core-valence correction
    E_ae = energy_values[7]
    E_fc = energy_values[8]

    E_CV = E_ae - E_fc

    #Finally your jun-ChS energy
    CC_jTZ = energy_values[0]

    E_jChS = CC_jTZ + Delta_MP2_CBS + E_CV

    return ()

def write_output():

    #Append to original file results from jun-ChS scheme
    f = open(filename, "a")

    f.write('\n'+
            20*' ' + 16*' ' + 6*'*' + 2*' ' + '*' + 9*' ' + 5*'*' + '\n' +
            20*' ' + 15*' ' + '*' + 8*' ' + '*' + 8*' ' + '* \n' +
            20*' ' + 15*' ' + '*' + 8*' ' + '*' + 8*' ' + '* \n' +
            20*' ' + 15*' ' + '*' + 9*' ' + 5*'*' + 4*' ' + 5*'*' + '\n' +
            20*' ' + 6*'*' + 9*' ' + '*' + 8*' ' + '*' + 5*' ' + '*' + 8*' ' + '* \n' +
            20*' ' + 2*' ' + 2*'*' + 5*' ' + 4*'*' + 2*' ' + '*' + 8*' ' + '*' + 5*' ' + '*' + 8*' ' + '* \n' +
            20*' ' + 2*' ' + 2*'*' + 12*' ' + 6*'*' + 2*' ' + '*' + 5*' ' + '*' + 3*' ' + 5*'*' + '\n' +
            20*' ' + 2*' ' + 2*'*' + '\n' +
            20*' ' + '*' + ' ' + 2*'*' + '\n' +
            20*' ' + ' ' + 2*'*' + '\n' +
            '\n'
            )

    f.write('Extrapolated energy with jun-ChS: \n' + 'E(jChS) = ' + str(E_jChS) + '\n')
    f.close()

    return

file, status = gen_input_file()

if status == True:
    extract_energy_values()
    calculate_jChS()
    write_output()
