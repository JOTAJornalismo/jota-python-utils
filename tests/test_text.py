from unittest import TestCase
from jota_utils.text import remove_accents

class ValidateRemoveAccents(TestCase):
    
    def test_deve_remover_acentos(self):
        text = "isso é um texto com acentuação"
        self.assertEqual(remove_accents(text), "isso e um texto com acentuacao")