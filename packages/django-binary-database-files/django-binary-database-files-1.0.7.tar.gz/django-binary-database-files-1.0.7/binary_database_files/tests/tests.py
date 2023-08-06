# -*- coding: utf-8 -*-
import os
import shutil
import tempfile
from zipfile import ZipFile

import six

from django.conf import settings
from django.core import files
from django.core.files import File as DjangoFile
from django.core.files.storage import default_storage
from django.core.management import call_command
from django.db import models
from django.test import TestCase

from binary_database_files.models import File
from binary_database_files.storage import DatabaseStorage
from binary_database_files.tests.models import Thing
from binary_database_files import utils

DIR = os.path.abspath(os.path.split(__file__)[0])

class DatabaseFilesTestCase(TestCase):

    def setUp(self):
        self.media_dir = os.path.join(DIR, 'media/i/special')
        if os.path.isdir(self.media_dir):
            shutil.rmtree(self.media_dir)
        os.makedirs(self.media_dir)

    def test_adding_file(self):

        # Create default thing storing reference to file
        # in the local media directory.
        test_fqfn = os.path.join(self.media_dir, 'test.txt')
        open(test_fqfn, 'w').write('hello there')
        o1 = o = Thing()
        test_fn = 'i/special/test.txt'
        o.upload = test_fn
        o.save()
        obj_id = o.id

        # Confirm thing was saved.
        Thing.objects.update()
        q = Thing.objects.all()
        self.assertEqual(q.count(), 1)
        self.assertEqual(q[0].upload.name, test_fn)

        # Confirm the file only exists on the file system
        # and hasn't been loaded into the database.
        q = File.objects.all()
        self.assertEqual(q.count(), 0)

        # Verify we can read the contents of thing.
        o = Thing.objects.get(id=obj_id)
        self.assertEqual(o.upload.read(), b"hello there")

        # Verify that by attempting to read the file, we've automatically
        # loaded it into the database.
        File.objects.update()
        q = File.objects.all()
        self.assertEqual(q.count(), 1)
        self.assertEqual(six.BytesIO(q.first().content).getvalue(), b"hello there")

        # Load a dynamically created file outside /media.
        test_file = files.temp.NamedTemporaryFile(
            suffix='.txt',
            # Django>=1.10 no longer allows accessing files outside of MEDIA_ROOT...
            #dir=files.temp.gettempdir()
            dir=os.path.join(settings.PROJECT_DIR, 'media'),
        )
        data0 = b'1234567890'
        test_file.write(data0)
        test_file.seek(0)
        t = Thing.objects.create(
            upload=files.File(test_file),
        )
        self.assertEqual(File.objects.count(), 2)
        t = Thing.objects.get(pk=t.pk)
        self.assertEqual(t.upload.file.size, 10)
        self.assertEqual(t.upload.file.name[-4:], '.txt')
        self.assertEqual(t.upload.file.read(), data0)
        t.upload.delete()
        self.assertEqual(File.objects.count(), 1)

        # Delete file from local filesystem and re-export it from the database.
        self.assertEqual(os.path.isfile(test_fqfn), True)
        os.remove(test_fqfn)
        self.assertEqual(os.path.isfile(test_fqfn), False)
        o1.upload.read() # This forces the re-export to the filesystem.
        self.assertEqual(os.path.isfile(test_fqfn), True)

        # This dumps all files to the filesystem.
        File.dump_files()

        # Confirm when delete a file from the database, we also delete it from
        # the filesystem.
        self.assertEqual(default_storage.exists('i/special/test.txt'), True)
        default_storage.delete('i/special/test.txt')
        self.assertEqual(default_storage.exists('i/special/test.txt'), False)
        self.assertEqual(os.path.isfile(test_fqfn), False)

    def test_adding_extzipfile(self):
        # ZipExtFile advertises seek() but can raise UnsupportedOperation
        with ZipFile(os.path.join(DIR, 'fixtures/test.zip')) as testzip:
            for filename in testzip.namelist():
                with testzip.open(filename) as testfile:
                    o = Thing()
                    o.upload = DjangoFile(testfile)
                    o.save()
                with testzip.open(filename) as testfile:
                    uploaded = File.objects.get(name='i/special/' + filename)
                    self.assertEqual(uploaded.size, testzip.getinfo(filename).file_size)
                    self.assertEqual(six.BytesIO(uploaded.content).read(), testfile.read())

    def test_hash(self):
        verbose = 1

        # Create test file.
        image_content = open(os.path.join(DIR, 'fixtures/test_image.png'), 'rb').read()
        fqfn = os.path.join(self.media_dir, 'image.png')
        open(fqfn, 'wb').write(image_content)

        # Calculate hash from various sources and confirm they all match.
        expected_hash = '35830221efe45ab0dc3d91ca23c29d2d3c20d00c9afeaa096ab256ec322a7a0b3293f07a01377e31060e65b4e5f6f8fdb4c0e56bc586bba5a7ab3e6d6d97a192' # pylint: disable=C0301
        h = utils.get_text_hash(image_content)
        self.assertEqual(h, expected_hash)
        h = utils.get_file_hash(fqfn)
        self.assertEqual(h, expected_hash)
        h = utils.get_text_hash(open(fqfn, 'rb').read())
        self.assertEqual(h, expected_hash)
#        h = utils.get_text_hash(open(fqfn, 'r').read())#not supported in py3
#        self.assertEqual(h, expected_hash)

        # Create test file.
        if six.PY3:
            image_content = six.text_type('aあä')#, encoding='utf-8')
        else:
            image_content = six.text_type('aあä', encoding='utf-8')
        fqfn = os.path.join(self.media_dir, 'test.txt')
        open(fqfn, 'wb').write(image_content.encode('utf-8'))

        expected_hash = '1f40fc92da241694750979ee6cf582f2d5d7d28e18335de05abc54d0560e0f5302860c652bf08d560252aa5e74210546f369fbbbce8c12cfc7957b2652fe9a75' # pylint: disable=C0301
        h = utils.get_text_hash(image_content)
        self.assertEqual(h, expected_hash)
        h = utils.get_file_hash(fqfn)
        self.assertEqual(h, expected_hash)
        h = utils.get_text_hash(open(fqfn, 'rb').read())
        self.assertEqual(h, expected_hash)

    def test_custom_location(self):
        storage = DatabaseStorage(location=os.path.join(DIR, 'media/location'))
        if os.path.isdir(storage.location):
            shutil.rmtree(storage.location)

        class CustomLocationThing(models.Model):
            upload = models.FileField(storage=storage, max_length=500)

            class Meta:
                managed = False
                db_table = Thing()._meta.db_table

        # Create a file in a subdirectory of the custom location and save it
        test_fn = os.path.join('subdirectory', 'test.txt')
        test_fqfn = os.path.join(storage.location, 'subdirectory', 'test.txt')
        os.makedirs(os.path.join(storage.location, 'subdirectory'))
        open(test_fqfn, 'w').write('hello there')
        o1 = o = CustomLocationThing()
        o.upload = test_fn
        o.save()

        # Confirm thing was saved.
        q = CustomLocationThing.objects.all()
        self.assertEqual(q.count(), 1)
        self.assertEqual(q[0].upload.name, test_fn)

        # Confirm the file only exists on the file system
        # and hasn't been loaded into the database.
        q = File.objects.all()
        self.assertEqual(q.count(), 0)

        # Verify we can read the contents of thing.
        o = CustomLocationThing.objects.first()
        self.assertEqual(o.upload.read(), b"hello there")

        # Verify that by attempting to read the file, we've automatically
        # loaded it into the database.
        self.assertEqual(q.count(), 1)
        self.assertEqual(six.BytesIO(q.first().content).getvalue(), b"hello there")

        # Delete file from local filesystem and re-export it from the database.
        self.assertEqual(os.path.isfile(test_fqfn), True)
        os.remove(test_fqfn)
        self.assertEqual(os.path.isfile(test_fqfn), False)
        o1.upload.read()  # This forces the re-export to the filesystem.
        self.assertEqual(os.path.isfile(test_fqfn), True)

    def test_reading_file(self):
        call_command('loaddata', 'test_files.json')
        self.assertEqual(File.objects.count(), 1)
        response = self.client.get('/files/1.txt')
        if hasattr(response, 'streaming_content'):
            content = list(response.streaming_content)[0]
        else:
            content = response.content
        self.assertEqual(content, b'1234567890')
        self.assertEqual(response['content-type'], 'text/plain')
        self.assertEqual(response['content-length'], '10')

    def test_serve_file_from_database(self):
        call_command('loaddata', 'test_files.json')
        self.assertEqual(File.objects.count(), 1)
        test_fqfn = os.path.join(DIR, 'media', '1.txt')
        self.assertEqual(os.path.isfile(test_fqfn), True)
        os.remove(test_fqfn)
        self.assertEqual(os.path.isfile(test_fqfn), False)
        response = self.client.get('/files/1.txt')
        if hasattr(response, 'streaming_content'):
            content = list(response.streaming_content)[0]
        else:
            content = response.content
        self.assertEqual(content, b'1234567890')
        self.assertEqual(response['content-type'], 'text/plain')
        self.assertEqual(response['content-length'], '10')
