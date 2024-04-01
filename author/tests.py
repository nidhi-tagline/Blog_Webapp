from django.test import TestCase
from .models import Author

class AuthorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Author.objects.create(username="Test_author",bio_detail="This is sample bio")
        
    def get_author(self):
        return Author.objects.get(id=1)
    
    def test_username_label(self):
        author = self.get_author()
        field_label = author._meta.get_field('username').verbose_name
        self.assertEqual(field_label , 'username')
        
    def test_username_max_length(self):
        author = self.get_author()
        max_length = author._meta.get_field('username').max_length
        self.assertEqual(max_length,50)
        
    def test_bio_detail_label(self):
        author = self.get_author()
        field_label = author._meta.get_field('bio_detail').verbose_name
        self.assertEqual(field_label,'bio detail')
        
    def test_object_name(self):
        author = self.get_author()
        expected_name = author.username
        self.assertEqual(expected_name, str(author))
        