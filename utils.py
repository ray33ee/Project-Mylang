import ast
import custom_unparser
import rustify
import sugar
import symbol_table
import post
import deduction
import translator
import tempfile
import shutil
import os
import subprocess
import difflib

import logging

logger = logging.getLogger(__name__)


def analysis(source, exe=None, verbose=False, expected_stdout=None, compile=True):

    # prepend the source with mylang's std:
    with open("./docs/mylang_std") as fh:
        source = source + fh.read()

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

    logger.debug(ast.dump(p, indent=4))

    logger.debug("##################################")
    logger.debug("Final rust code")
    logger.debug("##################################")

    s = rustify.rustify(p)

    logger.debug(s)

    if compile:

        template_path = "C:\\Users\\Will\\Documents\\GitHub\\mylang_template"

        cwd = os.getcwd()

        with tempfile.TemporaryDirectory() as td:

            try:
                root = td + "\\template"
                main_rs = root + "\\src\\main.rs"
                target = root + "\\target"
                executable = target + "\\debug\\mylang_template.exe"

                logger.info("Copying template to temporary location...")
                # Copy the Rust template to the temporary directory
                shutil.copytree(template_path, root)

                if os.path.exists(target):
                    shutil.rmtree(target)

                logger.info("Writing Rust source...")
                # Open main.rs with append and write then write the source to the end
                with open(main_rs, "a") as fh:
                    fh.write(s)

                # Change the working directory to root
                os.chdir(root)

                logger.info("Compiling Rust code (cargo build)...")
                subprocess.run(["cargo", "build"])

                if not os.path.exists(executable):
                    raise "Cargo build command failed"

                if exe is not None:
                    shutil.copy(executable, exe)

                logger.info("Executing code...")
                r = subprocess.run([executable], capture_output=True)

                logger.info("stdout: " + str(r.stdout))
                logger.info("stderr: " + str(r.stderr))

                if expected_stdout is not None:
                    if r.stdout != expected_stdout:
                        logger.warning("Expected output does not match actual output for test")
                        logger.info("Expected output: " + repr(expected_stdout))
                        logger.info("Actual output: " + repr(r.stdout))
                        assert r.stdout == expected_stdout
                        logger.info("Stdout test passed.")


            finally:

                os.chdir(cwd)

    if not verbose:
        logging.root.setLevel(prior_level)







