formulas = ["E<> R1.WHITE && R2.RED",
            "E<> R1.MOVING_HW && R2.MOVING_HW",
            "A[] not deadlock", "E[] R1.WHITE && R2.RED",
            "A<> R1.WHITE && R2.RED",
            "E<> R1.WHITE && R2.RED && (RedRegion==1  || WhiteRegion==1 )",
            "E<> R1.WHITE && R2.RED && RedRegion==1",
            "E<> RedRegion!=1"
            ]


def checker(formula: str):
    property = ""

    # check str is blank or not
    if not formula or "deadlock" in formula:
        return

    """
    if formula.find("E<>"):
        property += "Once"

        print(formula)
    elif formula.find("A[]"):
        property += "Historically"
    """

    temp = ""
    # Eliminate E<> or A[]
    for f in formula.split(" ")[1:]:
        if "&&" in f:
            temp += " and "
        elif "||" in f:
            temp += " or "
        elif "." in f:
            temp += str(f.split(".")[0]) + "_state: " + str(f.split(".")[1])
        else:
            temp += f

    temp = "{" + temp + "}"

    print(formula, "  <<==>>  ", temp)


for formula in formulas:
    checker(formula)
