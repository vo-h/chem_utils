"""Functions that generate molecules based on functional groups. Super rudimentary at the moment."""

import cirpy
from typing import List, Literal
from chem_utils.utils import glue_blocks, generate_prefix
from pydantic import validate_arguments
from collections import defaultdict


@validate_arguments
def generate_molecule_by_carbon_length(
    major_length: int,
    chemistry: Literal["alkane", "func", "aldehyde", "carboxylic acid"] = "alkane",
    branch_locations: List[int] = [],
    branch_identities: List[str] = [],
    validate_molecule=True,
):

    suffix_dict = {"alkane": "ane", "func": "yl", "aldehyde": "anal", "carboxylic acid": "anoic acid"}

    suffix = suffix_dict[chemistry]
    name = ""

    if len(branch_locations) != len(branch_identities):
        raise ValueError("len(branch_locations) != len(branch_identities)")

    for ind, branch in enumerate(branch_identities):
        branch_location = branch_locations[ind]
        name = glue_blocks(name, f"{branch_location}-{branch} ")

    if major_length == 1:
        return "meth" + suffix
    elif major_length == 2:
        return "eth" + suffix
    elif major_length == 3:
        prefix = "prop" + suffix
    elif major_length == 4:
        prefix = "but" + suffix
    else:
        prefix = glue_blocks(generate_prefix(major_length)[:-1], suffix)

    name = glue_blocks(name, prefix)

    if validate_molecule:
        if cirpy.resolve(name, "smiles"):
            return name
    else:
        return name
