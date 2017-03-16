__author__ = 'mj'
import datetime
from haystack import indexes
from basesearch.models import Note


# from celery_haystack.indexes import CelerySearchIndex



class NoteIndex(indexes.SearchIndex, indexes.Indexable):
    # class NoteIndex(CelerySearchIndex, indexes.Indexable):


    # *******************************demo***************************************
    # text = indexes.NgramField(document=True, use_template=True)
    # text = indexes.CharField(document=True, use_template=True)
    # datafacet = indexes.CharField(use_template=True, faceted=True)
    # #text2 = indexes.CharField(use_template=True, faceted=True)
    # text2 = indexes.DateField(model_attr='pub_date', faceted=True)
    #
    # author = indexes.CharField(model_attr='author', faceted=True)
    # pub_date = indexes.DateField(model_attr='pub_date',faceted=True)
    # #content_auto = indexes.EdgeNgramField(model_attr='content')
    # suggestions = indexes.FacetCharField()
    #
    # def prepare(self, obj):
    #     prepared_data = super(NoteIndex, self).prepare(obj)
    #     prepared_data['suggestions'] = prepared_data['text']
    #     return prepared_data
    # ********************************demo***************************************

    # *******************************ghwsx***************************************

    # text = indexes.CharField(document=True, use_template=True)
    # locationfacet = indexes.CharField(use_template=True, faceted=True)
    # profession = indexes.FacetMultiValueField( )
    # # locationfacet = indexes.FacetMultiValueField( )
    # ebtypefacet = indexes.IntegerField(use_template=True, faceted=True)
    # applytime = indexes.IntegerField(model_attr='applytime',faceted=True)

    # *******************************ghwsx***************************************


    # *******************************test****************************************

    # professfacet = indexes.CharField(use_template=True, faceted=True)
    # author = indexes.CharField(model_attr='author', faceted=True)
    # pub_date = indexes.DateField(model_attr='pub_date',faceted=True)
    # content_auto = indexes.EdgeNgramField(model_attr='content')
    # suggestions = indexes.FacetCharField()

    # *******************************test*****************************************
    text = indexes.CharField(document=True, use_template=True)
    textdate = indexes.DateTimeField(model_attr='textdate', null=True)
    title = indexes.CharField(model_attr='title', boost=5)
    content = indexes.CharField(model_attr='content')
    webid = indexes.IntegerField(model_attr='webid',boost=0)
    degree = indexes.IntegerField(model_attr='degree',boost=0)
    autolink = indexes.CharField(model_attr='autolink',boost=0)

    # *******************************ghwsx***************************************
    # def prepare_profession(self, obj):
    #     return [str(profess) for (profess,) in obj.profession if profess!=',']
    # *******************************ghwsx***************************************

    def get_model(self):
        return Note

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

    def get_updated_field(self):
        return "updated"
