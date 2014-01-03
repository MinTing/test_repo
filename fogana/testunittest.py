

# This is a python file.

class SomeClass(object):
    def __init__(self, x):
        print "Hi"
        self._x = 10

if __name__ == "__main__":
    import unittest

    class SomeUnitTest(unittest.TestCase):
        def setUp(self):
            # perform common initialization.
            pass
            
        def tearDown(self):
            # clean-up after tests
            pass

        def test_some_tests(self):
            a = SomeClass(10)
            self.assertEquals(a._x, 10)

    unittest.main()