'''Функции приложения'''
import uuid
import os.path


def image_upload_path(instance, filename):
    """ Функция определения папки для изображения """
    return 'images/{0}/{1}/{2}'.format(
        instance._meta.db_table,
        instance.parent_pk(),
        generate_uuid4_filename(filename)
    )


def generate_uuid4_filename(filename):
    """ Функция генерации имени файла """
    _, ext = os.path.splitext(filename)
    basename = str(uuid.uuid4()).replace("-", "")
    return u'{0}{1}'.format(basename, ext)
