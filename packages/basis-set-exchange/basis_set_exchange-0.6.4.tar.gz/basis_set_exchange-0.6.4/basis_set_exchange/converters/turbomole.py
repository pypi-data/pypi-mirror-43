'''
Conversion of basis sets to Turbomole format
'''

from .. import lut
from .. import manip
from .common import write_matrix


def write_turbomole(basis):
    '''Converts a basis set to Gaussian format
    '''

    s = '$basis\n'
    s += '*\n'

    # TM basis sets are completely uncontracted
    basis = manip.uncontract_general(basis)
    basis = manip.uncontract_spdf(basis)
    basis = manip.sort_basis(basis)

    # Elements for which we have electron basis
    electron_elements = [k for k, v in basis['basis_set_elements'].items() if 'element_electron_shells' in v]

    # Elements for which we have ECP
    ecp_elements = [k for k, v in basis['basis_set_elements'].items() if 'element_ecp' in v]

    # Electron Basis
    if len(electron_elements) > 0:
        for z in electron_elements:
            data = basis['basis_set_elements'][z]
            sym = lut.element_sym_from_Z(z, False)
            s += '{} {}\n'.format(sym, basis['basis_set_name'])
            s += '*\n'

            for shell in data['element_electron_shells']:
                exponents = shell['shell_exponents']
                coefficients = shell['shell_coefficients']
                ncol = len(coefficients) + 1
                nprim = len(exponents)

                am = shell['shell_angular_momentum']
                amchar = lut.amint_to_char(am, hij=True)
                s += '    {}   {}\n'.format(nprim, amchar)

                point_places = [8 * i + 15 * (i - 1) for i in range(1, ncol + 1)]
                s += write_matrix([exponents, *coefficients], point_places, convert_exp=True)

            s += '*\n'

    # Write out ECP
    if len(ecp_elements) > 0:
        s += '$ecp\n'
        s += '*\n'
        for z in ecp_elements:
            data = basis['basis_set_elements'][z]
            sym = lut.element_sym_from_Z(z)
            s += '{} {}-ecp\n'.format(sym, basis['basis_set_name'])
            s += '*\n'

            max_ecp_am = max([x['potential_angular_momentum'][0] for x in data['element_ecp']])
            max_ecp_amchar = lut.amint_to_char([max_ecp_am], hij=True)

            # Sort lowest->highest, then put the highest at the beginning
            ecp_list = sorted(data['element_ecp'], key=lambda x: x['potential_angular_momentum'])
            ecp_list.insert(0, ecp_list.pop())

            s += '  ncore = {}   lmax = {}\n'.format(data['element_ecp_electrons'], max_ecp_am)

            for pot in ecp_list:
                rexponents = pot['potential_r_exponents']
                gexponents = pot['potential_gaussian_exponents']
                coefficients = pot['potential_coefficients']

                am = pot['potential_angular_momentum']
                amchar = lut.amint_to_char(am, hij=True)

                if am[0] == max_ecp_am:
                    s += '{}\n'.format(amchar)
                else:
                    s += '{}-{}\n'.format(amchar, max_ecp_amchar)

                point_places = [9, 23, 32]
                s += write_matrix([*coefficients, rexponents, gexponents], point_places, convert_exp=True)
            s += '*\n'

    s += '$end\n'
    return s
