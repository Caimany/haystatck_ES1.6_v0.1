from django.conf import settings
from haystack.backends.elasticsearch_backend import \
        ElasticsearchSearchBackend, ElasticsearchSearchEngine
from elasticsearch_2 import Elasticsearch2SearchEngine,Elasticsearch2SearchBackend,DJANGO_CT,DJANGO_ID,FIELD_MAPPINGS,DEFAULT_FIELD_MAPPING

class ConfigurableElasticBackend(ElasticsearchSearchBackend):


    def __init__(self, connection_alias, **connection_options):
        super(ConfigurableElasticBackend, self).__init__(
                                connection_alias, **connection_options)

        user_settings = getattr(settings, 'ELASTICSEARCH_INDEX_SETTINGS')
        user_analyzer = getattr(settings, 'ELASTICSEARCH_DEFAULT_ANALYZER')

        if user_settings:
            setattr(self, 'DEFAULT_SETTINGS', user_settings)
        if user_analyzer:
            setattr(self, 'DEFAULT_ANALYZER', user_analyzer)

    def build_schema(self, fields):
        content_field_name, mapping = super(ConfigurableElasticBackend,
                                              self).build_schema(fields)

        for field_name, field_class in fields.items():
            field_mapping = mapping[field_class.index_fieldname]

            if field_mapping['type'] == 'string' and field_class.indexed:
                if not hasattr(field_class, 'facet_for') and not \
                                  field_class.field_type in('ngram', 'edge_ngram'):
                    field_mapping['analyzer'] = self.DEFAULT_ANALYZER
            mapping.update({field_class.index_fieldname: field_mapping})
        return (content_field_name, mapping)

class ConfigurableElasticSearchEngine(ElasticsearchSearchEngine):
    backend = ConfigurableElasticBackend



class ConfigurableElasticBackend2(Elasticsearch2SearchBackend):

    def __init__(self, connection_alias, **connection_options):
        super(ConfigurableElasticBackend2, self).__init__(
            connection_alias, **connection_options)

        # user_settings = getattr(settings, 'ELASTICSEARCH_INDEX_SETTINGS')
        # user_analyzer = getattr(settings, 'ELASTICSEARCH_DEFAULT_ANALYZER')
        #
        #
        #
        # if user_settings:
        #     setattr(self, 'DEFAULT_SETTINGS', user_settings)
        # if user_analyzer:
        #     setattr(self, 'DEFAULT_ANALYZER', user_analyzer)




    def build_schema(self, fields):
        # content_field_name, mapping = super(ConfigurableElasticBackend2,
        #                                     self).build_schema(fields)
        #
        # for field_name, field_class in fields.items():
        #     field_mapping = mapping[field_class.index_fieldname]
        #
        #     if field_mapping['type'] == 'string' and field_class.indexed:
        #         if not hasattr(field_class, 'facet_for') and not \
        #                         field_class.field_type in ('ngram', 'edge_ngram'):
        #             field_mapping['analyzer'] = self.DEFAULT_ANALYZER
        #     mapping.update({field_class.index_fieldname: field_mapping})



        # user_fieldsmapping = getattr(settings, 'Fields_Mapping')

        # return (content_field_name, mapping)

        content_field_name = ''
        mapping = {
            DJANGO_CT: {'type': 'string', 'index': 'not_analyzed', 'include_in_all': False},
            DJANGO_ID: {'type': 'string', 'index': 'not_analyzed', 'include_in_all': False},
        }

        for field_name, field_class in fields.items():
            # print field_name,field_class
            field_mapping = FIELD_MAPPINGS.get(field_class.field_type, DEFAULT_FIELD_MAPPING).copy()

            # print field_mapping

            if field_class.boost != 1.0:
                field_mapping['boost'] = field_class.boost

            if field_class.document is True:
                content_field_name = field_class.index_fieldname

            # Do this last to override `text` fields.
            if field_mapping['type'] == 'string':
                if field_class.indexed is False or hasattr(field_class, 'facet_for'):
                    field_mapping['index'] = 'not_analyzed'
                    del field_mapping['analyzer']
                else:
                    if field_name in self.Fields_Mapping.keys():
                        # print field_name,self.Fields_Mapping[field_name]
                        field_mapping['analyzer']=self.Fields_Mapping[field_name]





            mapping[field_class.index_fieldname] = field_mapping

        print content_field_name
        return (content_field_name, mapping)


class ConfigurableElasticSearchEngine2(Elasticsearch2SearchEngine):
    backend = ConfigurableElasticBackend2

