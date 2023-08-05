from django.db.models import options

__version__ = '0.5.41'
options.DEFAULT_NAMES += (
'rdf_type', 'auto_author', 'view_set', 'container_path', 'permission_classes', 'serializer_fields', 'nested_fields')
