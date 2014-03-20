from . import BaseTestMixin
from nose.plugins.attrib import attr
#def _registerRoutes(config):
    #config.add_route('home', '/')
    #config.add_route('project_new', '/project/new')
    #config.add_route('project', '/project/{project}')
    #config.add_route('project_edit', '/project/{project}/edit')
    #config.add_route('project_partition', '/project/{project}/partition')
    #config.add_route('project_partition_grid', '/project/{project}/partition/grid')
    #config.add_route('project_partition_import', '/project/{project}/partition/import')

#class UnitTestBase(unittest.TestCase):

    #def setUp(self):
        #self.config = testing.setUp(request=testing.DummyRequest())
        #super(UnitTestBase, self).setUp()
        #_registerRoutes(self.config)

#class TestProject(UnitTestBase):

    #def test_it(self):

        #from ..models import (
            #Project,
            #)
        #p = Project(
            #u'Short project description',
        #)

        #DBSession.add(p)

        #from ..views.project import project
        #request = testing.DummyRequest()

        #request.matchdict = {'project': 2}
        #info = project(request)
        #self.assertEqual(info['project'], DBSession.query(Project).get(2))

    #def test_doesnt_exist(self):
        #from ..views.project import project
        #request = testing.DummyRequest()

        ## doesn't exist
        #request.matchdict = {'project': 1}
        #response = project(request)
        #self.assertEqual(response.location, 'http://example.com/')

#class TestProjectNew(UnitTestBase):

    #def tearDown(self):
        #DBSession.remove()
        #testing.tearDown()

    #def test_not_submitted(self):
        #from ..views.project import project_new

        #request = testing.DummyRequest()
        #info = project_new(request)
        #self.assertEqual(info['page_id'], 'project_new')

    #def test_submitted_grid(self):
        #from ..views.project import project_new
        #self.config.testing_securitypolicy(userid=321)

        #request = testing.DummyRequest()
        #request.params = {
            #'form.submitted': True,
            #'name':u'NewProject',
            #'type': 'grid'
        #}
        #response = project_new(request)
        #self.assertEqual(response.location, 'http://example.com/project/3/partition/grid')

    #def test_submitted_import(self):
        #from ..views.project import project_new
        #self.config.testing_securitypolicy(userid=321)

        #request = testing.DummyRequest()
        #request.params = {
            #'form.submitted': True,
            #'name':u'NewProject',
            #'type': 'import'
        #}
        #response = project_new(request)
        #self.assertEqual(response.location, 'http://example.com/project/4/partition/import')


@attr(functional=True)
class TestHome(BaseTestMixin):

    def test_home(self):
        res = self.testapp.get('', status=200)
        self.assertTrue('Short project description' in res.body)

@attr(functional=True)
class TestProject(BaseTestMixin):


    def test_project(self):
        res = self.testapp.get('/project/1', status=200)
        self.assertTrue('Short project description' in res.body)
