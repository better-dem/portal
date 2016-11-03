from django.test import TestCase
import core.models as cm

class SurveyAppUnitTests(TestCase):
    def setup(self):
        pass
        
    def test_gis_models_and_functionality(self):
        m = cm.GeoTag(name = "californiaish", polygon = "POLYGON(( 41.998 -124.211, 41.972 -120.022, 38.987 -120.036, 32.854 -114.718, 32.373 -123.881, 41.998 -124.211 ))")
        m.save()

        num_tags_covering_contra_costa = cm.GeoTag.objects.filter(polygon__covers="POINT( 37.764 -121.837 )").count()
        self.assertEqual(num_tags_covering_contra_costa, 1)

        num_tags_covering_nyc = cm.GeoTag.objects.filter(polygon__covers="POINT( 40.683 -73.893 )").count()
        self.assertEqual(num_tags_covering_nyc, 0)

    def test_registered_participation_app_views_exist(self):
        for app in cm.get_registered_participation_apps():
            if not "views_module" in app.__dict__:
                raise Exception("app missing views module: "+app.name)
            required_views = ["new_project", "administer_project", "participate"]
            for v in required_views:
                if not v in app.views_module.__dict__:
                    raise Exception("app "+app.name+" missing view: "+v)
