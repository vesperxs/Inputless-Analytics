# from django.test import TestCase
# from django.urls import reverse

# import unittest

# # Create your tests here.

# class TestSearchModule(TestCase):
    
#     def test_graph_exist_at_desired_location(self):
#         # test if the the page return a correct status_code
#         print("graph_views exist")
#         response = self.client.get('/graph.html') 
#         self.assertEqual(response.status_code, 200)

#     def test_table_exist_at_desired_location(self):
#         # test if the the page return a correct status_code
#         print("table_view exist")
#         response = self.client.get('/login/?next=/tables_view.html') 
#         self.assertEqual(response.status_code, 200)

#     def test_filter_exist_at_desired_location(self):
#         # test if the the page return a correct status_code
#         print("filter_results exist")
#         response = self.client.get('/login/?next=/search_options.html') 
#         self.assertEqual(response.status_code, 200)

#     def test_graph_view_response(self):
#         response = self.client.get('/login/?next=/graph_views',data={'query': 'contino', 'deep': 1, 'type': 'PERSON'}

                                   
#         )
#         print(response)

#         self.assertEqual(response.status_code, 200)
       
