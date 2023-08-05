import re
from grapheneapi.exceptions import RPCError


def decodeRPCErrorMsg(e):
    """ Helper function to decode the raised Exception and give it a
        python Exception class
    """
    found = re.search(
        (
            "(10 assert_exception: Assert Exception\n|"
            "3030000 tx_missing_posting_auth)"
            ".*: (.*)\n"
        ),
        str(e),
        flags=re.M)
    if found:
        return found.group(2).strip()
    else:
        return str(e)


class MissingRequiredActiveAuthority(RPCError):
    pass


class NoMethodWithName(RPCError):
    pass


class UnhandledRPCError(RPCError):
    pass


class NumRetriesReached(Exception):
    pass


class OperationInProposalExistsException(Exception):
    """ An operation in a proposal was already seen by the API node and will
        not be accepted for rebroadcast
    """
    pass
