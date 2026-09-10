def origin_stabilizer(register):

    return sum(register.bits[0:4]) >= 0


def authorship_stabilizer(register):

    return sum(register.bits[4:8]) >= 0


def sovereignty_stabilizer(register):

    return sum(register.bits[8:12]) >= 0


def warp_stabilizer(register):

    return sum(register.bits[12:16]) >= 0


def metric_stabilizer(register):

    return sum(register.bits[16:20]) >= 0