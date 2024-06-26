import tests
import utils
import logging
import sys
import parse_template


logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

source, expected_output = tests.test_sources[-1]

#for source, expected_output in tests.test_sources:
#utils.analysis(source, verbose=True, expected_stdout=expected_output, compile=False)

#tests.run_tests()

parse_template.Parser()