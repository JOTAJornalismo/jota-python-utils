from unittest import TestCase
from jota_utils.models import django_unique_upload_to_filename


class ModelTest(TestCase):
    
    def test_deve_gerar_um_id_com_sucesso(self):
        generated_id = django_unique_upload_to_filename("",filename='myfile.txt')
        self.assertIsNotNone(generated_id)
        self.assertTrue(generated_id.endswith('_myfile.txt'))