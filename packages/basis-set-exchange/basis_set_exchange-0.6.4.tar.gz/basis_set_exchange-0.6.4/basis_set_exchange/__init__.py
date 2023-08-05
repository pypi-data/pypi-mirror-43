'''
Basis Set Exchange

Contains utilities for reading, writing, and converting
basis set information
'''

# Just import the basic user API
from .api import (get_basis, lookup_basis_by_role, get_metadata, get_reference_data, get_all_basis_names,
                  get_references, get_basis_family, filter_basis_sets, get_families, get_family_notes, get_basis_notes,
                  has_basis_notes, has_family_notes, get_schema, get_formats, get_reference_formats, get_roles,
                  version, get_data_dir)
from .bundle import create_bundle, get_archive_types

# Handle versioneer
from ._version import get_versions
versions = get_versions()
__version__ = versions['version']
__git_revision__ = versions['full-revisionid']
del get_versions, versions
