"""Functions that generate molecules based on functional groups. Super rudimentary at the moment."""

import cirpy
from typing import List, Literal
from chem_utils.utils import glue_blocks, generate_prefix
from pydantic import validate_arguments


@validate_arguments
def generate_moles_with_functional_tail(
    major_length: int,
    branch_locations: List[int] = [],
    branch_identies: List[str] = [],
    suffix: Literal["ane", "yl", "anal", "ol"] = "ane",
    validate=True,
):
    name = ""

    if len(branch_locations) != len(branch_identies):
        raise ValueError("len(branch_locations) != len(branch_identies)")

    for ind, branch in enumerate(branch_identies):
        branch_location = branch_locations[ind]
        name = glue_blocks(name, f"{branch_location}-{branch} ")

    if major_length == 1:
        return "methane"
    if major_length == 2:
        return "ethane"
    if major_length == 3:
        prefix = "propane"
    if major_length == 4:
        prefix = "butane"
    if major_length >= 5:
        prefix = glue_blocks(generate_prefix(major_length)[:-1], suffix)

    name = glue_blocks(name, prefix)

    if validate:
        if cirpy.resolve(name, "smiles"):
            return name
    else:
        return name
