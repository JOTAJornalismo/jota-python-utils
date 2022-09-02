import uuid


def django_unique_upload_to_filename(_, filename):
    """
    Unique filename generator for FileField fields.

    Usage:

    class MyModel(models.Model):
        file = ImageField(upload_to=unique_upload_to_filename)
    """
    return f'{uuid.uuid4()}_{filename}'
