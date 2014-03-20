
import unittest

from pyramid import testing

from ..models import (
    Base,
    DBSession,
    Project,
    Area,
    User,
    )

from sqlalchemy import create_engine
from sqlalchemy.orm import configure_mappers

SQLALCHEMY_URL = 'postgresql://www-data@localhost/osmtm_tests'
engine = create_engine(SQLALCHEMY_URL)
DBSession.configure(bind=engine)
configure_mappers()
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

def populate():
    #configure_mappers()

    import shapely
    import geojson
    from geoalchemy2 import (
        shape,
        )

    geometry = '{"type":"Polygon","coordinates":[[[7.237243652343749,41.25922682850892],[7.23175048828125,41.12074559016745],[7.415771484374999,41.20552261955812],[7.237243652343749,41.25922682850892]]]}'
    geometry = geojson.loads(geometry, object_hook=geojson.GeoJSON.to_instance)
    geometry = shapely.geometry.asShape(geometry)
    geometry = shape.from_shape(geometry, 4326)

    area = Area(geometry)

    project = Project(
        u'Short project description',
    )
    project.area = area
    DBSession.add(project)
    project.auto_fill(12)

    user = User(321, 'foo', admin=True)
    DBSession.add(user)

class BaseTestMixin(unittest.TestCase):

    def setUp(self):
        from webtest import TestApp
        from osmtm import main

        self.setupDb()
        app = main({}, **{
            'sqlalchemy.url': SQLALCHEMY_URL,
            'available_languages': 'en fr',
            'pyramid.default_locale_name': 'en',
            })
        self.testapp = TestApp(app)

        populate()

    def setupDb(self):
        tables = Base.metadata.tables
        DBSession.execute('TRUNCATE %s RESTART IDENTITY;' \
                % ', '.join(tables))

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()
