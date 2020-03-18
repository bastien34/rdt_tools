import uno
from com.sun.star.uno import RuntimeException


def createUnoService(service, ctx=None, args=None):
    if not ctx:
        ctx = uno.getComponentContext()
    smgr = ctx.getServiceManager()
    if ctx and args:
        return smgr.createInstanceWithArgumentsAndContext(service, args, ctx)
    elif args:
        return smgr.createInstanceWithArguments(service, args)
    elif ctx:
        return smgr.createInstanceWithContext(service, ctx)
    else:
        return smgr.createInstance(service)


def mri(target):
    """Macro to instantiate Mri introspection tool from hanya."""
    try:
        mri = createUnoService("mytools.Mri")
        mri.inspect(target)
    except (RuntimeException, AttributeError):
        print('Fail loading MRI')
