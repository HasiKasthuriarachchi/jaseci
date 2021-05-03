import sys
import io

from jaseci.utils.mem_hook import mem_hook
from jaseci.actor.sentinel import sentinel
from jaseci.graph.graph import graph
import jaseci.jac.tests.dot_code as dtc

from unittest import TestCase
from jaseci.utils.utils import TestCaseHelper


class test_dot(TestCaseHelper, TestCase):
    """Unit test for DOT support"""

    def setUp(self):
        super().setUp()
        self.gph = graph(h=mem_hook())
        self.sent = sentinel(h=self.gph._h)
        self.old_stdout = sys.stdout
        self.new_stdout = io.StringIO()
        sys.stdout = self.new_stdout

    def tearDown(self):
        sys.stdout = self.old_stdout
        super().tearDown()

    def to_screen(self):
        sys.stdout = self.old_stdout
        print("output: ", self.new_stdout.getvalue())
        sys.stdout = self.new_stdout

    def test_dot_node(self):
        """Test node in dot"""
        self.sent.register_code(dtc.dot_node)
        gen_walker = self.sent.walker_ids.get_obj_by_name('init')
        gen_walker.prime(self.gph)
        gen_walker.run()
        self.assertEqual(self.new_stdout.getvalue(), "graph_root_node_name\n")

    def test_dot_node_overwrite_name(self):
        """Test node in dot with name overwrite"""
        self.sent.register_code(dtc.dot_node_overwrite_name)
        gen_walker = self.sent.walker_ids.get_obj_by_name('init')
        gen_walker.prime(self.gph)
        gen_walker.run()
        self.assertTrue("node:subnode:real_name" in self.new_stdout.getvalue())

    def test_dot_node_multi_stmts(self):
        """Test node in dot, defined with multiple statements."""
        self.sent.register_code(dtc.dot_node_multi_stmts)
        gen_walker = self.sent.walker_ids.get_obj_by_name('init')
        gen_walker.prime(self.gph)
        gen_walker.run()
        self.assertEqual(self.new_stdout.getvalue(),
                         "real_test_node\n"
                         "2021\n")

    def test_dot_edge(self):
        """Test edge in dot."""
        self.sent.register_code(dtc.dot_edge)
        gen_walker = self.sent.walker_ids.get_obj_by_name('init')
        gen_walker.prime(self.gph)
        gen_walker.run()
        self.assertEqual(self.new_stdout.getvalue(),
                         "root\n"
                         "node_1\n"
                         "node_2\n")

    def test_dot_edge_with_attrs(self):
        """Test edge in dot with attrs"""
        self.sent.register_code(dtc.dot_edge_with_attrs)
        gen_walker = self.sent.walker_ids.get_obj_by_name('init')
        gen_walker.prime(self.gph)
        gen_walker.run()
        self.assertEqual(self.new_stdout.getvalue(),
                         "root\n"
                         "node_1\n")

    def test_dot_graph_parses(self):
        self.sent.register_code(dtc.dot_graph)
        gen_walker = self.sent.walker_ids.get_obj_by_name('init')
        gen_walker.prime(self.gph)
        gen_walker.run()

    def test_dot_str(self):
        self.sent.register_code(dtc.dot_graph)
        gen_walker = self.sent.walker_ids.get_obj_by_name('init')
        gen_walker.prime(self.gph)
        gen_walker.run()
        dot_str = self.gph.graph_dot_str()
        self.assertTrue('strict digraph basic' in dot_str)