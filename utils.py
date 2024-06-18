import ast
import custom_unparser
import rustify
import sugar
import symbol_table
import post
import deduction
import translator

import logging

logger = logging.getLogger(__name__)


def analysis(source, verbose=False):

    # If verbosity is off, set the debugging level of the root logger to INFO level
    if not verbose:
        prior_level = logging.root.level
        logging.root.setLevel(logging.INFO)

    logger.debug("##################################")
    logger.debug("Source")
    logger.debug("##################################")

    logger.debug("\n" + source)

    # Create a python AST from the source code
    my_ast = ast.parse(source, mode='exec')

    # Convert certain operations in to their syntactic sugar equivalent
    sugar.sugar(my_ast)

    logger.debug("##################################")
    logger.debug("Abstract Syntax Tree")
    logger.debug("##################################")

    logger.debug(ast.dump(my_ast, indent=4))

    logger.debug("##################################")
    logger.debug("Unparsed content")
    logger.debug("##################################")

    logger.debug(custom_unparser.unparse(my_ast))

    logger.debug("##################################")
    logger.debug("Symbol Table")
    logger.debug("##################################")

    # Get the Mylang AST
    t = symbol_table.Table(my_ast)
    logger.debug(t)

    logger.debug("##################################")
    logger.debug("Mangler and Demangler tests")
    logger.debug("##################################")

    import mangle
    mangle.run_mangler_tests()

    logger.debug("##################################")
    logger.debug("Deduction")
    logger.debug("##################################")

    tree = deduction.deduce(t)

    logger.debug("POpoksdpf[d")
    logger.debug(tree)
    logger.debug(tree.symbol_map)

    logger.debug("##################################")
    logger.debug("Translation")
    logger.debug("##################################")

    _ir = translator.translate(tree)

    logger.debug(ast.dump(_ir, indent=4))

    logger.debug("##################################")
    logger.debug("Post processing")
    logger.debug("##################################")

    p = post.post_processing(_ir)

    # logger.debug(ast.dump(p, indent=4))

    logger.debug("##################################")
    logger.debug("Final rust code")
    logger.debug("##################################")

    s = rustify.rustify(p)

    logger.debug(s)

    if not verbose:
        logging.root.setLevel(prior_level)







