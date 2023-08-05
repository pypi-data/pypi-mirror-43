#a################################################################
#                                                               #
#   ########     ###    ########   ######  ######## ########    #
#   ##     ##   ## ##   ##     ## ##    ## ##       ##     ##   #
#   ##     ##  ##   ##  ##     ## ##       ##       ##     ##   #
#   ########  ##     ## ########   ######  ######   ########    #
#   ##        ######### ##   ##         ## ##       ##   ##     #
#   ##        ##     ## ##    ##  ##    ## ##       ##    ##    #
#   ##        ##     ## ##     ##  ######  ######## ##     ##   #
#                                                               #
#################################################################

# Written by Florian Marmuse, January 2018

# Requirements for the input text file :
# # is to comment
# $$ shall only appear in section titles
# finish with $$ ENDFILE $$
# The '+' and '->' in reactions must be ' + ' and ' -> '

# Best pratices for the input text file :
# Write e- first in the species, so n_e is y[0] as in older codes.

import numpy as np
import datetime
from toolbox_functions import reaction_elements, list_of_reactions, relevant_lines, remove_charge, format_rate,\
    format_energy, lines_in_section, get

# for the profiler
from cProfile import Profile
from pstats import Stats


################################################################
#                                                              #
#  ######  ########  ########  ######  #### ########  ######   #
# ##    ## ##     ## ##       ##    ##  ##  ##       ##    ##  #
# ##       ##     ## ##       ##        ##  ##       ##        #
#  ######  ########  ######   ##        ##  ######    ######   #
#       ## ##        ##       ##        ##  ##             ##  #
# ##    ## ##        ##       ##    ##  ##  ##       ##    ##  #
#  ######  ##        ########  ######  #### ########  ######   #
#                                                              #
################################################################


# make a list of the species
def list_of_species(text_file):
    """Return a list of the species declared, for example ['e^-','Xe','Xe^+'].
    Example: list_of_species('input_xenon.txt')
    """

    lines = lines_in_section('SPECIES', text_file)
    return [line.split('=')[0].strip() for line in lines]


def number_of_species(text_file):
    """With this, Te is y[number_of_species] and Tg is y[number_of_species+1].
    number_of_species('input_xenon.txt')

    """
    return len(list_of_species(text_file))


#####################


def read_charge(element):
    """Returns an integer corresponding to the charge of the element, up to 9.
    Example: read_charge('Xe^2+')
    """

    if element.endswith('+'):
        try:
            return int(element.split('+')[0][-1:])  # return the last character before the + if it can be converted to an int.
        except ValueError:
            return 1

    elif element.endswith('-'):
        try:
            return - int(element.split('-')[0][-1:])  # return the last character before the - if it can be converted to an int.
        except ValueError:
            return -1

    else:
        return 0

#########################


def ng_line(input_txt):
    """Text definition of the gas density.
    ng_line('input_xenon.txt').
    """

    species = list_of_species(input_txt)
    neutral_species = [a for a in species if read_charge(a) == 0]

    ng = ''
    for element in neutral_species:
        index = species.index(element)
        ng += '+ y[{}] '.format(index)

    return 'ng = '+ng.strip()

def h_line(input_txt):
    """Text definition of the h factor"""
    species = list_of_species(input_txt)
    neutral_species = [a for a in species if read_charge(a) == 0]
    n = neutral_species[0]
    return "h = thruster.h(n_e, ng, Te, Tg, params.B0, mass('{}'), R['{}']['e^-']['ELASTIC'].K(Te))".format(n,n)


def get_main_element(input_txt):
    lines = lines_in_section('MAIN SPECIES', input_txt)
    return [line.strip() for line in lines][0]  # à réecrire propre


###################################################################################
#                                                                                 #
#  ######  ##     ## ######## ##     ## ####  ######  ######## ########  ##    ## #
# ##    ## ##     ## ##       ###   ###  ##  ##    ##    ##    ##     ##  ##  ##  #
# ##       ##     ## ##       #### ####  ##  ##          ##    ##     ##   ####   #
# ##       ######### ######   ## ### ##  ##   ######     ##    ########     ##    #
# ##       ##     ## ##       ##     ##  ##        ##    ##    ##   ##      ##    #
# ##    ## ##     ## ##       ##     ##  ##  ##    ##    ##    ##    ##     ##    #
#  ######  ##     ## ######## ##     ## ####  ######     ##    ##     ##    ##    #
#                                                                                 #
###################################################################################


def chemistry_set(text_file):
    """Return a new reaction set, or add chemical reactions to a previous one.
    The output line order is the input species order.
    Example: chemistry_set('input_xenon.txt')
    """

    species = list_of_species(text_file) # you get the number of a species with species.index('Xe') for example
    output_chem = ['' for a in species]  # initialisation

    reactions = list_of_reactions(text_file)

    for element in species:
        element_index = species.index(element)

        output_line = ''
        for reaction in reactions:
            [reactants, products, type, rate_given] = reaction_elements(reaction)

            if (element in reactants) or (element in products):
                net_creation = products.count(element) - reactants.count(element)

                if net_creation == 0:
                    continue

                new_factor = '+ ({}) * {} '.format(str("%+d" % net_creation), format_rate(reaction))

                for reactant in reactants:
                    new_factor += '* y[{}] '.format(species.index(reactant))

                output_line += new_factor + '\\\n        '

        output_chem[element_index] += output_line

    return output_chem


##########################################################
#                                                        #
#  #### ##    ## ######## ##        #######  ##      ##  #
#   ##  ###   ## ##       ##       ##     ## ##  ##  ##  #
#   ##  ####  ## ##       ##       ##     ## ##  ##  ##  #
#   ##  ## ## ## ######   ##       ##     ## ##  ##  ##  #
#   ##  ##  #### ##       ##       ##     ## ##  ##  ##  #
#   ##  ##   ### ##       ##       ##     ## ##  ##  ##  #
#  #### ##    ## ##       ########  #######   ###  ###   #
#                                                        #
##########################################################


def inflow_set(text_file):
    """Return a new reaction set with gas inflow, or add the inflow to an existing one.
    Example: inflow_set('input_xenon.txt')."""

    species = list_of_species(text_file)
    output_in = ['' for a in species]

    inputs = lines_in_section('INFLOW', text_file)

    for element in inputs:
        output_in[species.index(element)] += '+ (params.Q0 / thruster.volume()) \\\n        '

    return output_in


#####################################################
#                                                   #
#  ##      ##    ###    ##       ##        ######   #
#  ##  ##  ##   ## ##   ##       ##       ##    ##  #
#  ##  ##  ##  ##   ##  ##       ##       ##        #
#  ##  ##  ## ##     ## ##       ##        ######   #
#  ##  ##  ## ######### ##       ##             ##  #
#  ##  ##  ## ##     ## ##       ##       ##    ##  #
#   ###  ###  ##     ## ######## ########  ######   #
#                                                   #
#####################################################


def recombination_set(text_file):
    """Hardcoded for two-atom molecules."""

    rec = lines_in_section('RECOMBINATION', text_file)
    species = list_of_species(text_file)
    output_reco = ['' for a in species]

    for reaction in rec:
        reactant = reaction.split('&')[0].strip()
        product = reaction.split('&')[1].strip()
        reco_rate = reaction.split('&')[2].strip()

        index = species.index(reactant)
        output_reco[index] += '\\\n\t\t- 0.25 * y[{}] * v_th(Tg, "{}") * (thruster.total_area() - thruster.open_area_neutrals())/thruster.volume() * {}'.format(index, reactant, reco_rate)

        index_pro = species.index(product)
        output_reco[index_pro] += '\\\n\t\t+ 0.5 * 0.25 * y[{}] * v_th(Tg, "{}") * (thruster.total_area() - thruster.open_area_neutrals())/thruster.volume() * {}'.format(index, reactant, reco_rate)

    return output_reco


##############################

def losses_set(text_file):
    """Return.

    Need a special case for electrons..."""

    species = list_of_species(text_file)
    positive_species = [a for a in species if read_charge(a) > 0]
    neutral_species = [b for b in species if read_charge(b) == 0]

    output_walls = ['' for a in species]

    main_element = get_main_element(text_file)

    # positively charged species
    for element in positive_species:
        index = species.index(element)
        output_walls[index] += '\\\n\t\t- h * y[{}] * uB(Te, "{}") * d**(-1) '.format(index, main_element)

    # neutral species
    for element in neutral_species:
        index = species.index(element)
        output_walls[index] += '- 0.25 * y[{}] * v_th(Tg, "{}") * thruster.open_area_neutrals()/thruster.volume()'.format(index, element)

        for other_element in positive_species:
            if remove_charge(other_element) == element:
                other_index = species.index(other_element)
                output_walls[index] += '\\\n\t\t+ h * y[{}] * uB(Te, "{}") * (thruster.total_area() - thruster.open_area_ions())/thruster.volume()'.format(other_index, main_element)

    # electrons
    index_electrons = species.index('e^-')
    Gamma_e = '('

    for element in positive_species:
        index = species.index(element)
        Gamma_e += '+ h * y[{}] * uB(Te, "{}") '.format(index, main_element)

    Gamma_e += ')'
    output_walls[index_electrons] += '- {} * d**(-1)'.format(Gamma_e)

    return output_walls


losses_set('input_xenon.txt')
losses_set('input_iodine.txt')


####################################################
#                                                  #
#  ########  ########  ######     ###    ########  #
#  ##     ## ##       ##    ##   ## ##   ##     ## #
#  ##     ## ##       ##        ##   ##  ##     ## #
#  ########  ######   ##       ##     ## ########  #
#  ##   ##   ##       ##       ######### ##        #
#  ##    ##  ##       ##    ## ##     ## ##        #
#  ##     ## ########  ######  ##     ## ##        #
#                                                  #
####################################################

def init_differentials(text_file):
    """Returns the vector of the dy.

    For example ['ydot[0] = ', 'ydot[1] = ', 'ydot[2] = '].
    """
    species = list_of_species(text_file) # you get the number of a species with species.index('Xe') par exemple
    return ['ydot[{}] = '.format(species.index(a)) for a in species]


init_differentials('input_xenon.txt')

####################################


def density_evolution_set(text_file):
    a = init_differentials(text_file)
    b = chemistry_set(text_file)
    c = inflow_set(text_file)
    d = losses_set(text_file)
    e = recombination_set(text_file)

    return ["".join(x) for x in zip(a, b, c, d, e)]


density_evolution_set('input_xenon.txt')


##################################################################################
#                                                                                #
#  ######## ######## ##     ## ########     ######## ##       ########  ######   #
#     ##    ##       ###   ### ##     ##    ##       ##       ##       ##    ##  #
#     ##    ##       #### #### ##     ##    ##       ##       ##       ##        #
#     ##    ######   ## ### ## ########     ######   ##       ######   ##        #
#     ##    ##       ##     ## ##           ##       ##       ##       ##        #
#     ##    ##       ##     ## ##           ##       ##       ##       ##    ##  #
#     ##    ######## ##     ## ##           ######## ######## ########  ######   #
#                                                                                #
##################################################################################

# to add: reprendre chaque réaction, + elastic collision electron contre chaque neutre, between all.

def electronic_temp_evolution(text_file):
    """Return the equation of evolution of Te."""

    species = list_of_species(text_file)
    reactions = list_of_reactions(text_file)
    reactions = [r for r in reactions if 'e^-' in reaction_elements(r)[0]]

    output = 'Ploss ='

#    reac_short("Xe_e_ela")

    # chemistry
    for reaction in reactions:
        [reactants, products, reaction_type, rate_given] = reaction_elements(reaction)

        output += '\\\n\t\t+ {} * e * {}(Te-Tg)'.format(format_rate(reaction), format_energy(reaction))

        for element in reactants:
            element_index = species.index(element)
            output += '* y[{}] '.format(element_index)

    # elastic collisions
#    for element in [a for a in species if read_charge(a) == 0]: # only neutral collisions
#        index_element = species.index(element)
#        output += '+ 3 * (m_e / prop.m["{}"]) * e * (Te-Tg) * n_e * y[{}] * K_el_{}(Te) '.format(element, index_element, element)
    
    # CHECK POWER BALANCE
    # big flaw here, careful in writing Ploss.. takes only the main element mass to compute uB.
    main_element = get_main_element(text_file)

    # electron kinetic energy
    output += '\\\n\t\t+ 2 * e * Te * h * y[{}] * uB(Te, "{}") * d**(-1)'.format(species.index('e^-'), main_element)

    # ion presheath kinetic energy
    output += '\\\n\t\t+ 0.5 * e * Te * h * y[{}] * uB(Te, "{}") * d**(-1)'.format(species.index('e^-'), main_element)

    # sheath potential
    for element in species:
        if read_charge(element) > 0:
            output += '\\\n\t\t+ 0.5 * np.log(mass("{}") / (2 * pi * m_e)) * e * Te * h * y[{}] * uB(Te, "{}") * d**(-1)'.format(element, species.index('e^-'), element)

    return output.strip().replace('Tg', 'y[{}]'.format(number_of_species(text_file)+1)).replace('Te', 'y[{}]'.format(number_of_species(text_file)))



###########################################################################################
#                                                                                         #
#   ######   ######## ##    ## ######## ########     ###    ########  #######  ########   #
#  ##    ##  ##       ###   ## ##       ##     ##   ## ##      ##    ##     ## ##     ##  #
#  ##        ##       ####  ## ##       ##     ##  ##   ##     ##    ##     ## ##     ##  #
#  ##   #### ######   ## ## ## ######   ########  ##     ##    ##    ##     ## ########   #
#  ##    ##  ##       ##  #### ##       ##   ##   #########    ##    ##     ## ##   ##    #
#  ##    ##  ##       ##   ### ##       ##    ##  ##     ##    ##    ##     ## ##    ##   #
#   ######   ######## ##    ## ######## ##     ## ##     ##    ##     #######  ##     ##  #
#                                                                                         #
###########################################################################################


def replace_Te_and_Tg(output_file, input_file):
    """Take the output file, and replace n_e, Te and Tg by their number."""
    species = list_of_species(input_file)
    index_Te = number_of_species(input_file)
    index_Tg = index_Te + 1
    index_ne = species.index('e^-')

    # Read in the file
    with open(output_file, 'r') as file:
        filedata = file.read()

    # Replace the target string
    filedata = filedata.replace('n_e', 'y[{}]'.format(index_ne)).replace('Te','y[{}]'.format(index_Te)).replace('Tg','y[{}]'.format(index_Tg))

    # Write the file out again
    with open(output_file, 'w') as file:
        file.write(filedata)

####################################


def replace_tabs(output_file):
    # Read in the file
    with open(output_file, 'r') as file:
        filedata = file.read()

    # Replace the target string
    filedata = filedata.replace('\t', '    ')

    # Write the file out again
    with open(output_file, 'w') as file:
        file.write(filedata)


###################################
# SCRIPT TO GENERATE THE DIFF.py  #
###################################

def profile(func):
    def timed_function(*args, **kwargs):
        pr = Profile()
        pr.enable()
        func(*args, **kwargs)
        pr.disable()
        pr.dump_stats('profile_output')
        return Stats('profile_output')
    return timed_function


@profile
def gen_diff(input_file):
    with open('./generated_diff.py', 'w') as gd:
        species = list_of_species(input_file)
        number_species = number_of_species(input_file)

        imports = '\n'.join([
                            'from rates import *', #K_in_Xe, K_iz_Xe, K_exc_Xe, K_el_Xe',
                            'from scipy.constants import pi, e, k, m_e',
                            'from toolbox_functions import uB, v_th, mass',
                            'import numpy as np',
                            'from objects_generator import Reaction'
                            ])

        gd.write(imports+'\n\n\n')

        gd.write('def differentials(t, y, ydot, case):\n')
        gd.write('\t"""This function has been generated by parser.py at {}."""\n\n'.format(datetime.datetime.now()))

        gd.write('\tglobal thruster, params\n\t[thruster, params, chem] = case\n\tR = chem.R\n\n')

        gd.write('\t' + ng_line(input_file) + '\n\t' + 'd = thruster.volume()/thruster.total_area()' + '\n\n')
        gd.write('\t' + h_line(input_file) + '\n\n')

        for line_number in range(number_species):
            gd.write('\t# Species {}\n'.format(species[line_number]))
            gd.write('\t' + density_evolution_set(input_file)[line_number])
            gd.write('\n\n')

        gd.write('\t# Electronic temperature\n')
        gd.write('\t' + electronic_temp_evolution(input_file) + '\n\n')

        gd.write('\tydot[{}] = (y[{}] * e)**(-1) * ((2/3)*(params.Pabs - Ploss) - e * y[{}] * ydot[{}])\n\n'.format(number_species, species.index('e^-'), number_species, species.index('e^-')))

        if 'iodine' in input_file: # TODO pas beau
            gd.write('\t# Gas temperature\n\tydot[7] = 0\n')
        else:
            gd.write('\t# Gas temperature\n\tydot[4] = 0\n')

    replace_Te_and_Tg('./generated_diff.py', input_file)
    replace_tabs('./generated_diff.py')

    print('\ngenerated_diff.py est ok!')

#########################
