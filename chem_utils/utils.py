from pydantic import validate_arguments


@validate_arguments
def glue_blocks(block_1: str, block_2: str):
    try:
        if block_1[-1] == block_2[0]:
            return block_1[:-1] + block_2
    except IndexError:
        pass
    return block_1 + block_2


@validate_arguments
def generate_prefix(number: int):
    if number in [1, 2, 3, 4]:
        return None  # no idea where chemists get these prefixes from.
    if number == 11:
        return "undeca"  # latin, not greek.
    if number == 21:
        return "heneicosa"  # Weird 'i'

    string = str(number)
    name = ""

    # Take care of ones first
    ones_prefix = {
        0: "",
        1: "hene",
        2: "do",
        3: "tri",
        4: "tetra",
        5: "penta",
        6: "hexa",
        7: "hepta",
        8: "octa",
        9: "nona",
    }
    name += ones_prefix[int(string[-1])]

    if len(string) == 2:
        if string[-2] == "1":
            name = glue_blocks(name, "deca")
        elif string[-2] == "2":
            name = glue_blocks(name, "cosa")
        else:
            name = glue_blocks(name, glue_blocks(ones_prefix[int(string[-2])], "aconta"))
    if len(string) > 2:
        raise ValueError("Doesn't yet support chain lengths beyond 99.")

    return name
