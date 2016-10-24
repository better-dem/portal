from django.test import TestCase
from core.models import GeoTag

class SurveyAppUnitTests(TestCase):
    def setup(self):
        pass
        
    def test_gis_models_and_functionality(self):
        m = GeoTag(tag_name = "californiaish", polygon = "POLYGON(( 41.998 -124.211, 41.972 -120.022, 38.987 -120.036, 32.854 -114.718, 32.373 -123.881, 41.998 -124.211 ))")
        m.save()

        num_tags_covering_contra_costa = GeoTag.objects.filter(polygon__covers="POINT( 37.764 -121.837 )").count()
        self.assertEqual(num_tags_covering_contra_costa, 1)

        num_tags_covering_nyc = GeoTag.objects.filter(polygon__covers="POINT( 40.683 -73.893 )").count()
        self.assertEqual(num_tags_covering_nyc, 0)

