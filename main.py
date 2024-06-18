import tests
import utils
import logging
import sys



logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

utils.analysis(tests.test_sources[-1], True)

tests.run_tests()