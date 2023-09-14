from django.test import TestCase
from search.forms import MultiscopeForm 
from http import HTTPStatus

class TestSeachForm(TestCase):

    def test_form_search_get(self):
        self.client.login(username="testuser",password="testpass")
        response = self.client.get("/account/login/?next=/graph.html")
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_form_input_selection_field(self):
        form = SearchForm()
        self.assertTrue(form.fields['input_query'].label is None or \
                        form.fields['input_query'].label == 'this is a simple test')

    def test_search_post_response_success(self):

        self.client.login(username="testuser",password="testpass")
        response = self.client.post(
            "/graph.html",
            data = {'query':'test','type':'PERSON','deep':'1'})
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_search_form_fails(self):
        form = SearchForm(data={'renewal_date': date})
        self.assertFalse(form.is_valid())
        

    def test_search_form_success(self):
        pass
      

        
        




 # def test_form_input_selection_field(self):
    #     form = SearchForm()
    #     self.assertTrue(form.fields['input_query'].label is None or \
    #                     form.fields['input_query'].label == 'this is a simple test')
 
    # def test_form_search_input(self):
    #     self.client.login(username="testuser",password="testpass")
    #     data = {'query':'Nerio Marino','type':'PERSON','deep':'1'}
    #     form = SearchForm(data={'data_graph':data})
    #     self.assertFalse(form.is_valid())

        

        
        
