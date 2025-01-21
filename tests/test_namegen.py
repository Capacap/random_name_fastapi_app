import unittest
import namegen as ng

class TestNameGen(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Load and process the CSV data for testing
        cls.filepath = './data/firstnames.csv'
        cls.df = ng.process_csv_data(cls.filepath)

    def test_process_csv_data(self):
        """Test the process_csv_data function."""
        df = ng.process_csv_data(self.filepath)
        self.assertIn('name', df.columns)
        self.assertIn('male', df.columns)
        self.assertIn('female', df.columns)
        self.assertNotIn('gender', df.columns)
        self.assertTrue(all(df.columns.str.islower()))
        self.assertTrue(all(' ' not in col for col in df.columns if col not in ['male', 'female']))
        self.assertTrue(all('.' not in col for col in df.columns if col not in ['male', 'female']))

    def test_get_countries(self):
        """Test the get_countries function."""
        countries = ng.get_countries(self.df)
        self.assertIsInstance(countries, list)
        self.assertIn('sweden', countries)
        self.assertNotIn('name', countries)
        self.assertNotIn('male', countries)
        self.assertNotIn('female', countries)

    def test_get_random_names(self):
        """Test the get_random_names function."""
        country = 'sweden'
        count = 10
        random_names = ng.get_random_names(self.df, country, count)
        self.assertEqual(len(random_names), count)
        self.assertIsInstance(random_names, list)

    def test_get_random_male_names(self):
        """Test the get_random_male_names function."""
        country = 'sweden'
        count = 10
        random_names = ng.get_random_male_names(self.df, country, count)
        self.assertEqual(len(random_names), count)
        self.assertIsInstance(random_names, list)

    def test_get_random_female_names(self):
        """Test the get_random_female_names function."""
        country = 'sweden'
        count = 10
        random_names = ng.get_random_female_names(self.df, country, count)
        self.assertEqual(len(random_names), count)
        self.assertIsInstance(random_names, list)

if __name__ == '__main__':
    unittest.main()
