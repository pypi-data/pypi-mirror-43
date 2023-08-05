import csemver as cs
from unittest import TestCase
from unittest import SkipTest
import sys

class TestCsemver(TestCase):
	def test_valid_string(self):
		s = cs.csemver("1.0.0");
		self.assertTrue(isinstance(s, cs.csemver));

	def test_parse_empty(self):
		s = cs.parse();
		self.assertEqual(str(s), "0.1.0");

	def test_parse_with_value(self):
		s = cs.parse("1.0.0");
		self.assertEqual(str(s), "1.0.0");

	def test_inc_major(self):
		s = cs.parse("0.1.1");
		s.incMajor();
		self.assertEqual(str(s),"1.0.0")

	def test_inc_minor(self):
		s = cs.parse("0.1.1");
		s.incMinor();
		self.assertEqual(str(s),"0.2.0");

	def test_inc_patch(self):
		s = cs.parse("0.1.1");
		s.incPatch();
		self.assertEqual(str(s), "0.1.2");

	def test_inc_build(self):
		a = cs.parse("0.2.2+build0")
		b = cs.parse("0.2.2+build1")
		a.incBuild()
		self.assertEqual(a,b)

	def test_inc_pre(self):
		a = cs.parse("0.1.0-rc0")
		b = cs.parse("0.1.0-rc1")
		a.incPrerelease()
		self.assertEqual(a,b)

	def test_number_descriptor(self):
		s = cs.parse("1.2.3-pre+build");
		self.assertEqual(s.number, "1.2.3-pre+build");

	def test_assign_version(self):
		if sys.version_info < (3, 0):
			raise SkipTest("must be Python 3.0 or greater")
		s = cs.parse("0.1.0");
		s.number = "1.0.0";
		self.assertEqual(str(s),"1.0.0");

	def test_set_version(self):
		s = cs.parse("0.1.0");
		s.setNumber("1.0.0");
		self.assertEqual(str(s),"1.0.0");

	def test_del_version(self):
		s = cs.parse("0.1.1")
		s.delNumber()
		self.assertEqual(str(s),"0.1.0")

	def test_del_op(self):
		if sys.version_info < (3,0):
			raise SkipTest("mustbe Python 3.0 or greater")
		s = cs.parse("1.0.0")
		self.assertEqual(s,"1.0.0")
		del s.number
		self.assertEqual(s, "0.1.0")

	def test_addition(self):
		a = cs.parse("0.0.1");
		b = cs.parse("0.2.0");
		self.assertEqual(str(a+b),"0.2.0");
		
		a = cs.parse("0.1.1")
		b = cs.parse("0.2.1")
		self.assertEqual(str(a+b),"0.3.1");

		a = cs.parse("0.1.1")
		b = cs.parse("0.0.10")
		self.assertEqual(str(a+b),"0.1.11")

	def test_add_and_assign(self):
		a = cs.parse("0.1.1");
		oldId = id(a);
		b = cs.parse("0.0.4");
		a += b;
		self.assertEqual(oldId, id(a))
		self.assertEqual(str(a),"0.1.5");

	def test_comprehension_greater(self):
		a = cs.parse("2.0.0");
		b = cs.parse("1.0.0");
		self.assertTrue(a>b);
		self.assertFalse(b>a)
		a = cs.parse("2.0.0");
		b = cs.parse("2.0.0-pre");
		self.assertTrue(a>b);
		self.assertFalse(b>a)

		a = cs.parse("0.1.0-pre1");
		b = cs.parse("0.1.0-pre");
		self.assertTrue(a>b);
		self.assertFalse(b>a)

		a = cs.parse("0.1.0-pre.1")
		b = cs.parse("0.1.0-pre")
		self.assertTrue(a>b)
		self.assertFalse(b>a)
		self.assertTrue(a > "0.1.0-pre")

	def test_comprehension_smaller(self):
		a = cs.parse("1.0.0");
		b = cs.parse("2.0.0");
		self.assertTrue(a<b);
		self.assertFalse(b<a);
		a = cs.parse("1.0.0-pre");
		b = cs.parse("1.0.0");
		self.assertTrue(a<b);
		self.assertFalse(b<a);

		a = cs.parse("0.1.0-pre");
		b = cs.parse("0.1.0-pre1");
		self.assertTrue(a<b);
		self.assertFalse(b<a)

		a = cs.parse("0.1.0-pre")
		b = cs.parse("0.1.0-pre.1")
		self.assertTrue(a<b)
		self.assertFalse(b<a)
		self.assertTrue(a < "0.1.0-pre.1")

	def test_comprehension_equal(self):
		a = cs.parse("1.0.0");
		b = cs.parse("1.0.0");
		self.assertTrue(a == b);

		a = cs.parse("1.0.0-pre");
		b = cs.parse("1.0.0-pre");
		self.assertTrue(a == b);

		a = cs.parse("1.0.0-pre+build");
		b = cs.parse("1.0.0-pre+build");
		self.assertTrue(a == b);

		a = cs.parse("1.0.0-pre+build");
		b = cs.parse("1.0.0-pre+build1");
		self.assertTrue(a == b);

		a = cs.parse("1.0.0-pre1+build");
		b = cs.parse("1.0.0-pre+build");
		self.assertFalse(a == b);

		a = cs.parse("1.0.0")
		self.assertTrue(a == "1.0.0")
		self.assertFalse(a == "0.1.0")

	def test_comprehension_not_equal(self):
		a = cs.parse("1.0.0-pre+build");
		b = cs.parse("1.0.0-pre+build1");
		self.assertFalse(a != b);
		self.assertTrue(a == b);
		a = cs.parse("1.0.0")
		self.assertTrue(a != "0.1.0")


	def test_index_ops(self):
		a = cs.parse(); # defaults to 0.1.0
		a['major'] = 2
		self.assertEqual(a.number,"2.1.0")
		a['minor'] = 2
		self.assertEqual(a.number,"2.2.0")
		a['patch'] = 1
		self.assertEqual(a.number,"2.2.1")
		a['prerelease'] = "dev"
		self.assertEqual(a.number,"2.2.1-dev")
		a['build'] = "build0"
		self.assertEqual(a.number,"2.2.1-dev+build0")
		a['build'] = None
		self.assertEqual(a.number,"2.2.1-dev")

	def test_wrong_index_op_value_raises_exception(self):
		a = cs.parse(); # defaults to 0.1.0
		with self.assertRaises(ValueError) as e:
			a['major'] = "02"
		with self.assertRaises(ValueError) as e:
			a['minor'] = "01"
		with self.assertRaises(ValueError) as e:
			a['patch'] = "03"
		with self.assertRaises(ValueError) as e:
			a['prerelease'] = "+dev"
		with self.assertRaises(ValueError) as e:
			a['build'] = "+build0"

		with self.assertRaises(TypeError) as e:
			a['major'] = []
		with self.assertRaises(TypeError) as e:
			a['minor'] = []
		with self.assertRaises(TypeError) as e:
			a['patch'] = []
		with self.assertRaises(TypeError) as e:
			a['prerelease'] = 3
		with self.assertRaises(TypeError) as e:
			a['build'] = 5

	def test_wrong_number_raises_exception(self):
		self.assertRaises(ValueError, cs.parse,"0.1.1d")
		self.assertRaises(TypeError, cs.parse, 5)

	def test_wrong_comprehension_type_raise_exception(self):
		a = cs.parse("1.0.0")
		with self.assertRaises(TypeError) as e:
			a == 3
		with self.assertRaises(TypeError) as e:
			a < 3
		with self.assertRaises(TypeError) as e:
			a > 3
		with self.assertRaises(TypeError) as e:
			a != 3
		with self.assertRaises(TypeError) as e:
			a >= 3
		with self.assertRaises(TypeError) as e:
			a <= 3

	def test_greater_equal(self):
		a = cs.parse("1.0.0-pre")
		b = cs.parse("1.0.0")
		self.assertFalse(a >= b)
		self.assertTrue(b >= a)
		self.assertTrue(a >= a)
		self.assertTrue(b >= "1.0.0-pre")
		self.assertTrue(b >= "1.0.0")
		self.assertFalse(b >= "1.1.0")

		a = cs.parse("1.0.0-pre.1.3")
		b = cs.parse("1.0.0-pre.1")
		self.assertTrue(a >= b)
		self.assertFalse(b >= a)
		self.assertTrue(a >= a)


	def test_less_equal(self):
		a = cs.parse("1.0.0-pre")
		b = cs.parse("1.0.0")
		self.assertTrue(a <= b)
		self.assertFalse(b <= a)
		self.assertTrue(a <= a)
		self.assertTrue(b <= "1.0.1")

	def test_len(self):
		a = cs.parse("1.0.0")
		self.assertEqual(len(a),3)
		a = cs.parse("1.0.0-pre.d")
		self.assertEqual(len(a),4)
		a = cs.parse("1.0.0-pre.d+build.1")
		self.assertEqual(len(a),5)

	def test_iterate_over_version(self):
		a = cs.parse("1.0.0-pre")
		expect = [1,0,0,"pre"]
		for i,v in zip(a,expect):
			self.assertEqual(i,v)

	def test_non_existing_key_raises_exception(self):
		a = cs.parse("1.0.0")
		with self.assertRaises(KeyError) as e:
			val = a['nonexistingkey']
		with self.assertRaises(KeyError) as e:
			a['nokey'] = "d"

	def test_del_item_Python3(self):
		a = cs.parse("1.1.1-pre")
		del a['prerelease']
		self.assertEqual(str(a),"1.1.1")

	def test_del_wrong_key_raises_exception(self):
		a = cs.parse("1.1.1")
		with self.assertRaises(KeyError) as e:
			del a['nokey']
		with self.assertRaises(KeyError) as e:
			del a['major']

	def test_dictionary_conversation(self):
		a = cs.parse("1.0.0-pre+build")
		b = dict(a)
		for k in b:
			self.assertEqual(a[k],b[k])

	def test_value_view(self):
		a = cs.parse("1.0.0-pre+build")
		b = a.values()
		a['major'] = 2
		a['minor'] = 1
		a['build'] = "build.2"
		for i,v in zip(a,b):
			self.assertEqual(i,v)

	def test_tuple_conversation(self):
		a = cs.parse("1.0.0")
		b = tuple(a)
		self.assertEqual(b,(1,0,0))