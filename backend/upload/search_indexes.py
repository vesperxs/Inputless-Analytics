import datetime
from haystack import indexes
from upload.models import DocumentDataStore



""" Define a SearchIndex object and schema definition for Haystack """
class DocumentIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    # Autocomplete

    #content_auto = indexes.EdgeNgramField(model_attr='content')
    
    def get_model(self):
        return DocumentDataStore
    
    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(title__lte=datetime.datetime.now())
    
    def get_updated_field(self):
        return "updated"
    
