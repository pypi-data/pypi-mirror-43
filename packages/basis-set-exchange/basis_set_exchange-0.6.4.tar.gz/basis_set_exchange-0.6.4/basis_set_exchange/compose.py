"""
Functions related to composing basis sets from individual components
"""

import os
from . import fileio, manip, memo


def _whole_basis_types(basis):
    '''
    Get a list of all the types of features in this basis set.

    '''

    all_types = set()

    for v in basis['basis_set_elements'].values():
        if 'element_electron_shells' in v:
            for sh in v['element_electron_shells']:
                tstr = '{}_{}'.format(sh['shell_harmonic_type'], sh['shell_function_type'])
                all_types.add(tstr)

        if 'element_ecp' in v:
            for pot in v['element_ecp']:
                all_types.add(pot['potential_ecp_type'] + '_ecp')

    return sorted(list(all_types))


def compose_elemental_basis(file_relpath, data_dir):
    """
    Creates an 'elemental' basis from an elemental json file

    This function reads the info from the given file, and reads all the component
    basis set information from the files listed therein. It then composes all the
    information together into one 'elemental' basis dictionary
    """

    # Do a simple read of the json
    el_bs = fileio.read_json_basis(os.path.join(data_dir, file_relpath))

    # construct a list of all files to read
    component_files = set()
    for k, v in el_bs['basis_set_elements'].items():
        component_files.update(set(v['element_components']))

    # Read all the data from these files into a big dictionary
    component_map = {k: fileio.read_json_basis(os.path.join(data_dir, k)) for k in component_files}

    # Broadcast the basis_set_references to each element
    # Use the basis_set_description for the reference description
    for k, v in component_map.items():
        for el, el_data in v['basis_set_elements'].items():
            el_data['element_references'] = [{
                'reference_description': v['basis_set_description'],
                'reference_keys': v['basis_set_references']
            }]

    # Compose on a per-element basis
    for k, v in el_bs['basis_set_elements'].items():

        components = v.pop('element_components')

        # all of the component data for this element
        el_comp_data = [component_map[c]['basis_set_elements'][k] for c in components]

        # merge all the data
        v = manip.merge_element_data(v, el_comp_data)
        el_bs['basis_set_elements'][k] = v

    return el_bs


@memo.BSEMemoize
def compose_table_basis(file_relpath, data_dir):
    """
    Creates a 'table' basis from an table json file

    This function reads the info from the given file, and reads all the elemental
    basis set information from the files listed therein. It then composes all the
    information together into one 'table' basis dictionary
    """

    # Do a simple read of the json
    file_path = os.path.join(data_dir, file_relpath)
    table_bs = fileio.read_json_basis(file_path)

    # construct a list of all elemental files to read
    element_files = set()
    for v in table_bs['basis_set_elements'].values():
        element_files.add(v['element_entry'])

    # Create a map of the elemental basis data
    # (maps file path to data contained in that file)
    element_map = {k: compose_elemental_basis(k, data_dir) for k in element_files}

    # Replace the basis set for all elements in the table basis with the data
    # from the elemental basis
    for k, v in table_bs['basis_set_elements'].items():
        entry = v['element_entry']
        data = element_map[entry]

        table_bs['basis_set_elements'][k] = data['basis_set_elements'][k]

    # Add the version to the dictionary
    file_base = os.path.basename(file_relpath)
    table_bs['basis_set_version'] = file_base.split('.')[-3]

    # Add whether the entire basis is spherical or cartesian
    table_bs['basis_set_function_types'] = _whole_basis_types(table_bs)

    # Read and merge in the metadata
    # This file must be in the same location as the table file
    meta_dirpath, table_filename = os.path.split(file_path)
    meta_filename = table_filename.split('.')[0] + '.metadata.json'
    meta_filepath = os.path.join(meta_dirpath, meta_filename)
    bs_meta = fileio.read_json_basis(meta_filepath)
    table_bs.update(bs_meta)

    # Remove the molssi schema (which isn't needed here)
    table_bs.pop('molssi_bse_schema')

    return table_bs
