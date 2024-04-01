from django.urls.base import reverse
from django.test import TestCase
from .models import Blog, Author, Comment
from datetime import datetime

class BlogModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_author = Author.objects.create(username="test_auther",bio_detail="This is a bio for test auther.")
        Blog.objects.create(title="sample blog",content="This is a sample blog",author=test_author)

    def get_blog(self):
        return Blog.objects.get(id=1)
    
    def test_object_name(self):
        blog = self.get_blog()
        expected_name = blog.title
        self.assertEqual(expected_name, str(blog))
        
    def test_title_label(self):
        blog = self.get_blog()
        field_label =  blog._meta.get_field('title').verbose_name
        self.assertEqual(field_label , 'title')
    
    def test_title_max_length(self):
        blog = self.get_blog()
        max_length = blog._meta.get_field('title').max_length
        self.assertEqual(max_length ,100)
        
    def test_created_at_field(self):
        blog = self.get_blog()
        expected_date = blog.created_at.date()
        self.assertEqual(expected_date,datetime.now().date())
        
    def test_content_label(self):
        blog = self.get_blog()
        field_name = blog._meta.get_field('content').verbose_name
        self.assertEqual(field_name,'content')
        
class CommentModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_author1 = Author.objects.create(username="test_auther1", bio_detail="This is a bio for test auther1.")
        test_author2 = Author.objects.create(username="testuser2", bio_detail="I am just a user")
        blog = Blog.objects.create(title="sample blog", content="This is a sample blog", author=test_author1)
        Comment.objects.create(comment="this is test comment", post=blog, created_by=test_author2)
    
    def get_comment(self):
        return Comment.objects.get(id=1)
    
    def test_object_name(self):
        comment = self.get_comment()
        expected_name = f"{comment.comment}"
        self.assertEqual(expected_name,str(comment))
        
    def test_post_object(self):
        comment = self.get_comment()
        post = comment.post
        self.assertIsInstance(post,Blog)
        
    def test_commentor_object(self):
        comment = self.get_comment()
        created_by = comment.created_by
        self.assertIsInstance(created_by,Author)


class BlogListViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_author = Author.objects.create(username="test_auther",bio_detail="This is a bio for test auther.")
        blog_list = 10
        for i in range(blog_list):
            Blog.objects.create(title=f"Blog {i}",content=f"Content of the blog {i}",author=test_author)
        
    def test_view_url_exists_at_location(self):
        response = self.client.get('/blogs/blogs/')
        self.assertEqual(response.status_code,200)
        
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("blog:all-blogs"))
        self.assertEqual(response.status_code,200)
        
    def test_view_has_expected_template(self):
        response = self.client.get(reverse('blog:all-blogs'))
        self.assertTemplateUsed(response,'blog/all_blogs.html')
        
    def test_view_pagination(self):
        response = self.client.get(reverse('blog:all-blogs'))
        self.assertTrue(response.context['is_paginated'],True)
        self.assertEqual(len(response.context['blog_posts']),5)