import os
import pytest
from pytest_girder.web_client import runWebClientTest

from girder.models.folder import Folder
from girder.models.item import Item

from .girder_utilities import girderWorker  # noqa


@pytest.mark.usefixtures('girderWorker')  # noqa
@pytest.mark.plugin('large_image')
@pytest.mark.parametrize('spec', (
    'imageViewerSpec.js',
    'largeImageSpec.js',
))
def testWebClient(boundServer, fsAssetstore, db, spec, girderWorker):  # noqa
    spec = os.path.join(os.path.dirname(__file__), 'web_client_specs', spec)
    runWebClientTest(boundServer, spec, 15000)


@pytest.mark.usefixtures('girderWorker')  # noqa
@pytest.mark.plugin('large_image')
@pytest.mark.plugin('large_image_annotation')
@pytest.mark.parametrize('spec', (
    'annotationListSpec.js',
    'geojsAnnotationSpec.js',
    'geojsSpec.js',
))
def testWebClientWithAnnotation(boundServer, fsAssetstore, db, spec, girderWorker):  # noqa
    spec = os.path.join(os.path.dirname(__file__), 'web_client_specs', spec)
    runWebClientTest(boundServer, spec, 15000)


@pytest.mark.usefixtures('girderWorker')  # noqa
@pytest.mark.plugin('large_image')
@pytest.mark.plugin('large_image_annotation')
def testWebClientAnnotationSpec(boundServer, fsAssetstore, db, admin, girderWorker):  # noqa
    # Create an item in the Public folder
    publicFolder = next(
        folder for folder in Folder().childFolders(parent=admin, parentType='user', user=admin)
        if folder['public'] is True)
    Item().createItem('Empty', admin, publicFolder)

    spec = os.path.join(os.path.dirname(__file__), 'web_client_specs', 'annotationSpec.js')

    runWebClientTest(boundServer, spec, 15000)
