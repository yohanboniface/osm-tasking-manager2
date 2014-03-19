import unittest
import transaction

from pyramid import testing

from ..models import (
    Base,
    DBSession,
    )

from geoalchemy2 import (
    Geometry,
    shape,
    elements,
    )

from sqlalchemy import create_engine
from sqlalchemy_i18n.manager import translation_manager
from sqlalchemy.orm import configure_mappers

translation_manager.options.update({
    'locales': ['en'],
    'get_locale_fallback': True
})
SQLALCHEMY_URL = 'postgresql://www-data@localhost/osmtm_tests'
engine = create_engine(SQLALCHEMY_URL)
DBSession.configure(bind=engine)
configure_mappers()
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

def _registerRoutes(config):
    config.add_route('home', '/')
    config.add_route('project_new', '/project/new')
    config.add_route('project', '/project/{project}')
    config.add_route('project_edit', '/project/{project}/edit')
    config.add_route('project_partition', '/project/{project}/partition')
    config.add_route('project_partition_grid', '/project/{project}/partition/grid')
    config.add_route('project_partition_import', '/project/{project}/partition/import')

class UnitTestBase(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp(request=testing.DummyRequest())
        super(UnitTestBase, self).setUp()
        _registerRoutes(self.config)

class TestProject(UnitTestBase):

    def test_it(self):

        from ..models import (
            Project,
            )
        p = Project(
            u'Short project description',
        )

        DBSession.add(p)

        from ..views.project import project
        request = testing.DummyRequest()

        request.matchdict = {'project': 1}
        info = project(request)
        self.assertEqual(info['project'], DBSession.query(Project).get(1))

    def test_doesnt_exist(self):
        from ..views.project import project
        request = testing.DummyRequest()

        # doesn't exist
        request.matchdict = {'project': 1}
        response = project(request)
        self.assertEqual(response.location, 'http://example.com/')

class TestProjectNew(UnitTestBase):

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()

    def test_not_submitted(self):
        from ..views.project import project_new

        request = testing.DummyRequest()
        info = project_new(request)
        self.assertEqual(info['page_id'], 'project_new')

    def test_submitted_grid(self):
        from ..views.project import project_new
        self.config.testing_securitypolicy(userid=321)

        request = testing.DummyRequest()
        request.params = {
            'form.submitted': True,
            'name':u'NewProject',
            'type': 'grid'
        }
        response = project_new(request)
        self.assertEqual(response.location, 'http://example.com/project/2/partition/grid')

    def test_submitted_import(self):
        from ..views.project import project_new
        self.config.testing_securitypolicy(userid=321)

        request = testing.DummyRequest()
        request.params = {
            'form.submitted': True,
            'name':u'NewProject',
            'type': 'import'
        }
        response = project_new(request)
        self.assertEqual(response.location, 'http://example.com/project/3/partition/import')
