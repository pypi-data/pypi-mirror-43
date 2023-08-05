from unittest import TestCase
from seneca.engine.interface import SenecaInterface
from seneca.engine.interpreter import SenecaInterpreter, ReadOnlyException, CompilationException
from os.path import join
from tests.utils import captured_output, TestInterface
import redis, unittest, seneca

test_contracts_path = seneca.__path__[0] + '/test_contracts/'

class TestRedis(TestInterface):

    def test_read_only_variables(self):
        with self.assertRaises(CompilationException) as context:
            self.si.execute_code_str("""
__contract__ = 'hacks'
            """)

    def test_read_only_variables_custom(self):
        with self.assertRaises(ReadOnlyException) as context:
            self.si.execute_code_str("""
bird = 'hacks'
            """, {'bird': '123'})

    def test_read_only_variables_aug_assign(self):
        with self.assertRaises(ReadOnlyException) as context:
            self.si.execute_code_str("""
bird += 1
            """, {'bird': 123})

    def test_import_datatypes(self):
        self.si.execute_code_str("""
from seneca.libs.datatypes import hmap
hmap('balance', str, int)
        """)

    def test_import_datatypes_reassign(self):
        with self.assertRaises(ReadOnlyException) as context:
            self.si.execute_code_str("""
from seneca.libs.datatypes import hmap
hmap = 'hacked'
            """)
        with self.assertRaises(ReadOnlyException) as context:
            self.si.execute_code_str("""
seed = 'hacked'
            """)

    def test_store_meta(self):
        self.si.execute_code_str("""
from seneca.libs.datatypes import hmap
@export
def callit(a,b,c=1,d=2):
    return 1,2
some_map = hmap('balance', str, int)
t, r = 2,3
x = 45
        """)

if __name__ == '__main__':
    unittest.main()
