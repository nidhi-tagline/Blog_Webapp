from django.test.testcases import TestCase
from django.test.client import Client
from .models import Author
from blog.models import Blog
from django.urls.base import reverse

class AuthorModelTests(TestCase):
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
        
    # check if author username is correct
    def test_author_username(self):
        author = self.get_author()
        expected_name = "Test_author"
        self.assertEqual(expected_name, author.username)
        
    # check if author bio detail is correct
    def test_author_bio_detail(self):
        author = self.get_author()
        expected_bio = "This is sample bio"
        self.assertEqual(author.bio_detail, expected_bio)
        
class AuthorProfileUpdateTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Author.objects.create(username="Test_author",bio_detail="This is sample bio")
        cls.client = Client()
        
    # check if authenticated user can update profile page
    def test_profile_update_for_authenticated_user(self):
        author = Author.objects.get(id=1)
        self.client.force_login(author)
        response = self.client.post(reverse("author:author-profile-update",kwargs={"pk": author.pk}),{'username':'Test_author','bio_detail':'updated bio'})
        self.assertEqual(response.status_code, 302)
        
        author.refresh_from_db()
        self.assertEqual(author.bio_detail,"updated bio")
        
    # check if other user cannot update profile
    def test_update_profile_not_accessible(self):
        author = Author.objects.get(id=1)
        self.client.post(reverse("author:author-profile-update",kwargs={"pk": author.pk}),{'username':'Test_author','bio_detail':'updated bio'})
        
        author.refresh_from_db()
        self.assertNotEqual(author.bio_detail,"updated bio")
        
class AuthorProfileViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        author1 = Author.objects.create(username="author1", bio_detail="author1 bio")
        author2 = Author.objects.create(username="author2", bio_detail="author2 bio")
        cls.client = Client()
        
        num_of_blogs = 6
        # create blogs for author1
        for i in range(num_of_blogs):
            Blog.objects.create(title=f"blog{i} title",content=f"blog{i} content",author=author1)
            
        # create blog for author2
        Blog.objects.create(title=f"sample blog",content=f"sample blog content",author=author2)
            
    # check only blogs by author are shown on their own profile
    def test_author_profile_blog_list(self):
        author = Author.objects.get(username="author1")
        # login author1 to visit his profile
        self.client.force_login(author)
        response = self.client.get(reverse("author:author-profile",kwargs={'pk':author.pk}))
        
        # get blog created by author2
        blog = Blog.objects.get(pk=7)
        self.assertNotIn(blog,response.context['blogs'])
        self.assertEqual(len(response.context['blogs']),6)
        self.assertEqual(response.status_code, 200)
        
    # check that logged in author cannot see other authors profile
    def test_url_cannot_be_manipulated(self):
        author = Author.objects.get(username="author1")
        # login as author1 and try accessing another authors profile
        self.client.force_login(author)
        wrong_user_url = reverse('author:author-profile', kwargs={'pk':2})
        response = self.client.get(wrong_user_url)  
        self.assertEqual(response.status_code,404)
