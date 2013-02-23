# -*- coding: utf8 -*-

class TestUtilitiesLibrary():

    def setup(self):
        from library.utilities import Utilities
        self.utilities = Utilities()

    def teardown(self):
        pass

    def test_create_slug_raises_exception_on_non_str_type(self):
        test_data = [' aB c_[9-']
        try:
            self.utilities.create_slug(test_data)
        except AttributeError:
            return True
        return False

    def test_create_slug_with_plain_string(self):
        test_data = ' aB c_[9-'
        expected_return = u'ab-c-9'
        return_data = self.utilities.create_slug(test_data)
        assert return_data == expected_return

    def test_create_slug_with_raw_string(self):
        test_data = r' aB c_[9-'
        expected_return = u'ab-c-9'
        return_data = self.utilities.create_slug(test_data)
        assert return_data == expected_return

    def test_create_slug_with_unicode_special_chars(self):
        test_data = u' äB c_[9-'
        expected_return = u'ab-c-9'
        return_data = self.utilities.create_slug(test_data)
        assert return_data == expected_return

    def test_create_title_from_slug_with_plain_string(self):
        test_data = ' Abc_t[9-'
        expected_return = 'Abc T[9'
        return_data = self.utilities.create_title_from_slug(test_data)
        assert return_data == expected_return

    def test_create_title_from_slug_with_raw_string(self):
        test_data = r' Abc_t[9-'
        expected_return = 'Abc T[9'
        return_data = self.utilities.create_title_from_slug(test_data)
        assert return_data == expected_return

    def test_create_title_from_slug_with_unicode_special_chars(self):
        test_data = u' äB c_[9-'
        expected_return = 'Abc T[9'
        return_data = self.utilities.create_title_from_slug(test_data)
        assert return_data == expected_return

    def test_create_title_from_slug_without_plain_string(self):
        a_list = ['test']
        a_tuple = ['test']

        error_type = TypeError
        test_function = self.utilities.create_title_from_slug
        test_runner = self.function_raises_exception_type
        assert test_runner(error_type, test_function, a_tuple)
        assert test_runner(error_type, test_function, a_list)

    def function_raises_exception_type(self, exception_type, test_function, \
                              *args, **kwargs):
        try:
            test_function(*args, **kwargs)
            print(test_function(*args, **kwargs))
        except exception_type:
            return True
        return False

