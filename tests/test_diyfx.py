import unittest

import diyfx

class TestDiyfx(unittest.TestCase):
    def test_template_to_regex(self):
        data = {'/a/static/path': '^\/a\/static\/path$',
                '/{year:\d\d\d\d}/{month:\d\d}/{slug}': '^\/(?P<year>\d\d\d\d)\/(?P<month>\d\d)\/(?P<slug>[^/]+)$'
        }
        for template in data:
            self.assertEqual(data[template], diyfx.template_to_regex(template))
