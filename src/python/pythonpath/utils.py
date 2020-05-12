import os
import pyuno


IMPLEMENTATION_NAME = "com.rdt.comp.Utils"


def path_to_url(path):
    if not path.startswith('file://'):
        return pyuno.systemPathToFileUrl(os.path.realpath(path))


def get_package_path(file_to_find):
    """
    Returns the path for template or image, using the constant
     TEMPLATE_NAME or LOGO_URL, which does not start with a "/".
    """
    working_dir = os.path.join(os.path.dirname(__file__), file_to_find)
    path = os.path.normpath(working_dir)
    if path.startswith('file:'):
        path = path.split(':')[1]
    assert os.path.isfile(path)
    return path_to_url(path)


def get_package_location(ctx):
    srv = ctx.getByName(
        "/singletons/com.sun.star.deployment.PackageInformationProvider")
    return srv.getPackageLocation(IMPLEMENTATION_NAME)
