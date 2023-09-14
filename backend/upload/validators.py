import os
from django.core.exceptions import ValidationError



def validate_file_extension(value):
    limit = 10485760

    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 10 MiB.')

    
    
    if value.file.content_type != 'application/msword' \
       and value.file.content_type != 'application/pdf' \
           and value.file.content_type != 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' \
               and value.file.content_type != 'application/vnd.ms-excel' \
                   and value.file.content_type != 'application/vnd.oasis.opendocument.text' \
                       and value.file.content_type != 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' \
                           and value.file.content_type != 'text/csv' \
                               and value.file.content_type != 'text/plain':
        raise ValidationError(u'Error message')

    
    
