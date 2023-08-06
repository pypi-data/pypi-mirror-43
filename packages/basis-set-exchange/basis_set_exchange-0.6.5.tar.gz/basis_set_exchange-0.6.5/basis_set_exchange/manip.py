"""
Common basis set manipulations

This module contains functions for uncontracting and merging basis set
data, as well as some other small functions.
"""

import copy

from . import lut


def contraction_string(element):
    """
    Forms a string specifying the contractions for an element

    ie, (16s,10p) -> [4s,3p]
    """

    # Does not have electron shells (ECP only?)
    if 'electron_shells' not in element:
        return ""

    cont_map = dict()
    for sh in element['electron_shells']:
        nprim = len(sh['exponents'])
        ngeneral = len(sh['coefficients'])

        # is a combined general contraction (sp, spd, etc)
        is_spdf = len(sh['angular_momentum']) > 1

        for am in sh['angular_momentum']:
            # If this a general contraction (and not combined am), then use that
            ncont = ngeneral if not is_spdf else 1

            if am not in cont_map:
                cont_map[am] = (nprim, ncont)
            else:
                cont_map[am] = (cont_map[am][0] + nprim, cont_map[am][1] + ncont)

    primstr = ""
    contstr = ""
    for am in sorted(cont_map.keys()):
        nprim, ncont = cont_map[am]

        if am != 0:
            primstr += ','
            contstr += ','
        primstr += str(nprim) + lut.amint_to_char([am])
        contstr += str(ncont) + lut.amint_to_char([am])

    return "({}) -> [{}]".format(primstr, contstr)


def merge_element_data(dest, sources):
    """
    Merges the basis set data for an element from multiple sources
    into dest.

    The destination is not modified, and a (shallow) copy of dest is returned
    with the data from sources added.
    """

    if dest is not None:
        ret = dest.copy()
    else:
        ret = {}

    # Note that we are not copying notes/data_sources
    for s in sources:
        if 'electron_shells' in s:
            if 'electron_shells' not in ret:
                ret['electron_shells'] = []
            ret['electron_shells'].extend(s['electron_shells'])
        if 'ecp_potentials' in s:
            if 'ecp_potentials' in ret:
                raise RuntimeError('Cannot overwrite existing ECP')
            ret['ecp_potentials'] = s['ecp_potentials']
            ret['element_ecp_electrons'] = s['element_ecp_electrons']
        if 'references' in s:
            if 'references' not in ret:
                ret['references'] = []
            for ref in s['references']:
                if not ref in ret['references']:
                    ret['references'].append(ref)

    # Sort the shells by angular momentum
    # Note that I don't sort ECP - ECP can't be composed, and
    # it should be sorted in the only source with ECP
    if 'electron_shells' in ret:
        ret['electron_shells'].sort(key=lambda x: x['angular_momentum'])

    return ret


def prune_basis(basis):
    """
    Removes primitives that have a zero coefficient, and
    removes duplicate shells

    This only finds EXACT duplicates, and is meant to be used
    after uncontracting

    The input basis set is not modified.
    """

    new_basis = copy.deepcopy(basis)

    for k, el in new_basis['elements'].items():
        if not 'electron_shells' in el:
            continue

        for sh in el['electron_shells']:
            new_exponents = []
            new_coefficients = []

            exponents = sh['exponents']

            # transpose of the coefficient matrix
            coeff_t = list(map(list, zip(*sh['coefficients'])))

            # only add if there is a nonzero contraction coefficient
            for i in range(len(sh['exponents'])):
                if not all([float(x) == 0.0 for x in coeff_t[i]]):
                    new_exponents.append(exponents[i])
                    new_coefficients.append(coeff_t[i])

            # take the transpose again, putting the general contraction
            # as the slowest index
            new_coefficients = list(map(list, zip(*new_coefficients)))

            sh['exponents'] = new_exponents
            sh['coefficients'] = new_coefficients

        # Remove any duplicates
        shells = el.pop('electron_shells')
        el['electron_shells'] = []

        for sh in shells:
            if sh not in el['electron_shells']:
                el['electron_shells'].append(sh)

    return new_basis


def uncontract_spdf(basis, max_am=0):
    """
    Removes sp, spd, spdf, etc, contractions from a basis set

    The general contractions are replaced by uncontracted versions

    Contractions up to max_am will be left in place. For example,
    if max_am = 1, spd will be split into sp and d

    The input basis set is not modified. The returned basis
    may have functions with coefficients of zero and may have duplicate
    shells.
    """

    new_basis = copy.deepcopy(basis)

    for k, el in new_basis['elements'].items():

        if not 'electron_shells' in el:
            continue
        newshells = []

        for sh in el['electron_shells']:

            # am will be a list
            am = sh['angular_momentum']
            coeff = sh['coefficients']

            # if this is an sp, spd,...  orbital
            if len(am) > 1:
                newsh = sh.copy()
                newsh['angular_momentum'] = []
                newsh['coefficients'] = []

                ngen = len(sh['coefficients'])
                for g in range(ngen):
                    if am[g] > max_am:
                        newsh2 = sh.copy()
                        newsh2['angular_momentum'] = [am[g]]
                        newsh2['coefficients'] = [coeff[g]]
                        newshells.append(newsh2)
                    else:
                        newsh['angular_momentum'].append(am[g])
                        newsh['coefficients'].append(coeff[g])

                newshells.insert(0, newsh)

            else:
                newshells.append(sh)

        el['electron_shells'] = newshells

    return new_basis


def uncontract_general(basis):
    """
    Removes the general contractions from a basis set

    The input basis set is not modified. The returned basis
    may have functions with coefficients of zero and may have duplicate
    shells.
    """

    new_basis = copy.deepcopy(basis)

    for k, el in new_basis['elements'].items():

        if not 'electron_shells' in el:
            continue

        newshells = []

        for sh in el['electron_shells']:
            # Don't uncontract sp, spd,.... orbitals
            # leave that to uncontract_spdf
            if len(sh['angular_momentum']) == 1:
                for c in sh['coefficients']:
                    # copy, them replace 'coefficients'
                    newsh = sh.copy()
                    newsh['coefficients'] = [c]
                    newshells.append(newsh)
            else:
                newshells.append(sh)

        el['electron_shells'] = newshells

    return prune_basis(new_basis)


def uncontract_segmented(basis):
    """
    Removes the segmented contractions from a basis set

    This implicitly removes general contractions as well,
    but will leave sp, spd, ... orbitals alone

    The input basis set is not modified. The returned basis
    may have functions with coefficients of zero and may have duplicate
    shells.
    """

    new_basis = copy.deepcopy(basis)

    for k, el in new_basis['elements'].items():

        if not 'electron_shells' in el:
            continue

        newshells = []

        for sh in el['electron_shells']:
            exponents = sh['exponents']
            nam = len(sh['angular_momentum'])

            for i in range(len(exponents)):
                newsh = sh.copy()
                newsh['exponents'] = [exponents[i]]
                newsh['coefficients'] = [["1.00000000"] * nam]

                # Remember to transpose the coefficients
                newsh['coefficients'] = list(map(list, zip(*newsh['coefficients'])))

                newshells.append(newsh)

        el['electron_shells'] = newshells

    return new_basis


def make_general(basis):
    """
    Makes one large general contraction for each angular momentum

    If split_spdf is True, sp... orbitals will be split apary
    """

    zero = '0.00000000'

    new_basis = uncontract_spdf(basis)

    for k, el in new_basis['elements'].items():
        if not 'electron_shells' in el:
            continue

        # See what we have
        all_am = []
        for sh in el['electron_shells']:
            if not sh['angular_momentum'] in all_am:
                all_am.append(sh['angular_momentum'])

        all_am = sorted(all_am)

        newshells = []
        for am in all_am:
            # TODO - Check all shells to make sure region and harmonic type are consistent
            newsh = {
                'angular_momentum': am,
                'exponents': [],
                'coefficients': [],
                'region': 'combined',
                'harmonic_type': 'spherical'
            }

            # Do exponents first
            for sh in el['electron_shells']:
                if sh['angular_momentum'] != am:
                    continue
                newsh['exponents'].extend(sh['exponents'])

            # Number of primitives in the new shell
            nprim = len(newsh['exponents'])

            cur_prim = 0
            for sh in el['electron_shells']:
                if sh['angular_momentum'] != am:
                    continue

                ngen = len(sh['coefficients'])

                for g in range(ngen):
                    coef = [zero] * cur_prim
                    coef.extend(sh['coefficients'][g])
                    coef.extend([zero] * (nprim - len(coef)))
                    newsh['coefficients'].append(coef)

                cur_prim += len(sh['exponents'])

            newshells.append(newsh)

        el['electron_shells'] = newshells

    return new_basis


def _is_single_column(col):
    return sum(float(x) != 0.0 for x in col) == 1


def _is_zero_column(col):
    return sum(float(x) != 0.0 for x in col) == 0


def _nonzero_range(vec):
    for idx, x in enumerate(vec):
        if float(x) != 0.0:
            first = idx
            break

    for idx, x in enumerate(reversed(vec)):
        if float(x) != 0.0:
            last = (len(vec) - idx)
            break

    if first is None:
        return (None, None)
    else:
        return (first, last)


def _find_block(mat):

    # Initial range of rows
    row_range = _nonzero_range(mat[0])
    rows = range(row_range[0], row_range[1])

    # Find the right-most column with a nonzero in it
    col_range = (0, 0)
    for r in rows:
        x, y = _nonzero_range([col[r] for col in mat])
        col_range = (min(col_range[0], x), max(col_range[1], y))

    cols = range(col_range[0], col_range[1])

    # Columns may be jagged also
    # Iterate until we don't see any change
    while True:
        row_range_old = row_range
        col_range_old = col_range
        for c in cols:
            x, y = _nonzero_range(mat[c])
            row_range = (min(row_range[0], x), max(row_range[1], y))

        rows = range(row_range[0], row_range[1])

        for r in rows:
            x, y = _nonzero_range([col[r] for col in mat])
            col_range = (min(col_range[0], x), max(col_range[1], y))

        cols = range(col_range[0], col_range[1])

        if col_range == col_range_old and row_range == row_range_old:
            break

    return (rows, cols)


def optimize_general(basis):
    """
    Optimizes the general contraction using the method of Hashimoto et al

    .. seealso :: | T. Hashimoto, K. Hirao, H. Tatewaki
                  | 'Comment on Dunning's correlation-consistent basis set'
                  | Chemical Physics Letters v243, Issues 1-2, pp, 190-192 (1995)
                  | https://doi.org/10.1016/0009-2614(95)00807-G

    """

    new_basis = copy.deepcopy(basis)
    for k, el in new_basis['elements'].items():

        if not 'electron_shells' in el:
            continue

        elshells = el.pop('electron_shells')
        el['electron_shells'] = []
        for sh in elshells:
            exponents = sh['exponents']
            coefficients = sh['coefficients']
            nprim = len(exponents)
            nam = len(sh['angular_momentum'])

            if nam > 1 or len(coefficients) < 2:
                el['electron_shells'].append(sh)
                continue

            # First, find columns (general contractions) with a single non-zero value
            single_columns = [idx for idx, c in enumerate(coefficients) if _is_single_column(c)]

            # Find the corresponding rows that have a value in one of these columns
            # Note that at this stage, the row may have coefficients in more than one
            # column. That is ok, we are going to split it off anyway
            single_rows = []
            for col_idx in single_columns:
                col = coefficients[col_idx]
                for row_idx in range(nprim):
                    if float(col[row_idx]) != 0.0:
                        single_rows.append(row_idx)

            # Split those out into new shells, and remove them from the
            # original shell
            new_shells_single = []
            for row_idx in single_rows:
                newsh = copy.deepcopy(sh)
                newsh['exponents'] = [exponents[row_idx]]
                newsh['coefficients'] = [['1.00000000000']]
                new_shells_single.append(newsh)

            exponents = [x for idx, x in enumerate(exponents) if idx not in single_rows]
            coefficients = [x for idx, x in enumerate(coefficients) if idx not in single_columns]
            coefficients = [[x for idx, x in enumerate(col) if not idx in single_rows] for col in coefficients]

            # Remove Zero columns
            #coefficients = [ x for x in coefficients if not _is_zero_column(x) ]

            # Find contiguous rectanglar blocks
            new_shells = []
            while len(exponents) > 0:
                block_rows, block_cols = _find_block(coefficients)

                # add as a new shell
                newsh = copy.deepcopy(sh)
                newsh['exponents'] = [exponents[i] for i in block_rows]
                newsh['coefficients'] = [[coefficients[colidx][i] for i in block_rows] for colidx in block_cols]
                new_shells.append(newsh)

                # Remove from the original exponent/coefficient set
                exponents = [x for idx, x in enumerate(exponents) if idx not in block_rows]
                coefficients = [x for idx, x in enumerate(coefficients) if idx not in block_cols]
                coefficients = [[x for idx, x in enumerate(col) if not idx in block_rows] for col in coefficients]

            # I do this order to mimic the output of the original BSE
            el['electron_shells'].extend(new_shells)
            el['electron_shells'].extend(new_shells_single)

        # Fix coefficients for completely uncontracted shells to 1.0
        for sh in el['electron_shells']:
            if len(sh['coefficients']) == 1 and len(sh['coefficients'][0]) == 1:
                sh['coefficients'][0][0] = '1.0000000'

    return new_basis


def sort_shells(shells):
    """
    Sort a list of basis set shells into a standard order

    The order within a shell is by decreasing value of the exponent.

    The order of the shell list is in increasing angular momentum, and then
    by decreasing number of primitives, then decreasing value of the largest exponent.

    The original data is not modified.
    """

    new_shells = copy.deepcopy(shells)

    for sh in new_shells:
        # Sort primitives within a shell
        # Transpose of coefficients
        tmp_c = list(map(list, zip(*sh['coefficients'])))

        # Zip together exponents and coeffs for sorting
        tmp = zip(sh['exponents'], tmp_c)

        # Sort by decreasing value of exponent
        tmp = sorted(tmp, key=lambda x: -float(x[0]))

        # Unpack, and re-transpose the coefficients
        tmp_c = [x[1] for x in tmp]
        sh['exponents'] = [x[0] for x in tmp]
        sh['coefficients'] = list(map(list, zip(*tmp_c)))

    # Sort by increasing AM, then general contraction level, then decreasing highest exponent
    return list(
        sorted(
            new_shells,
            key=lambda x: (max(x['angular_momentum']), -len(x['exponents']), -len(x['coefficients']), -float(x[
                'exponents'][0]))))


def sort_potentials(potentials):
    """
    Sort a list of ECP potentials into a standard order

    The order within a potential is not modified.

    The order of the shell list is in increasing angular momentum, with the largest
    angular momentum being moved to the front.

    The original data is not modified, and a deep copy is returned.
    """

    new_potentials = copy.deepcopy(potentials)

    # Sort by increasing AM, then move the last element to the front
    new_potentials = list(sorted(new_potentials, key=lambda x: x['angular_momentum']))
    new_potentials.insert(0, new_potentials.pop())
    return new_potentials


def sort_basis(basis):
    """
    Sorts all the information in a basis set into a standard order

    The original data is not modified.
    """

    new_basis = copy.deepcopy(basis)

    for k, el in new_basis['elements'].items():
        if 'electron_shells' in el:
            el['electron_shells'] = sort_shells(el['electron_shells'])

    return new_basis
