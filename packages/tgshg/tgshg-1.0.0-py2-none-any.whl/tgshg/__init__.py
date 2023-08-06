
name = "tgshg"

# __modules__, __all__, __doc__ = \
#   __import__(__name__ + "._internals", fromlist=[__name__]
#             ).init_package(__path__, __name__, __doc__)

# # Import all modules contents to the main namespace
# exec(("from .{} import *\n" * len(__modules__)).format(*__modules__))