import logging
import uno
import unohelper
from com.sun.star.task import XJobExecutor

# debug
from IPython.core.debugger import Pdb
ipdb = Pdb()
from utils import mri


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('tcm')


class TimeCodeCorrector(unohelper.Base, XJobExecutor):

    def __init__(self, ctx):
        self.ctx = ctx

    def trigger(self, args):
        logger.debug("Logger says Launcher's been called.")
        desktop = self.ctx.ServiceManager.createInstanceWithContext(
            "com.sun.star.frame.Desktop", self.ctx )

        doc = desktop.getCurrentComponent()

        try:
            search = doc.createSearchDescriptor()
            search.SearchRegularExpression = True
            search.SearchString = "orking"

            found = doc.findFirst( search )
            while found:
                found.String = found.String.replace( "o", u"\xa0" )
                logger.debug('something has been done.')
                found = doc.findNext( found.End, search)
        except:
            logger.debug('Something has not been done!!!')


g_ImplementationHelper = unohelper.ImplementationHelper()
g_ImplementationHelper.addImplementation(
        TimeCodeCorrector,
        "com.rdt.openoffice.TimeCodeCorrector",
        ("com.sun.star.task.Job",),)


# if __name__ == "__main__":
#     import os
#
#     # os.environ.update({'PYPYSCRIPT_LOG_LEVEL':'ERROR',
#     #                    'PYSCRIPT_LOG_STDOUT': '1',
#     #                    'PYUNO_LOGLEVEL': 'ARGS'})
#
#     # Start OpenOffice.org, listen for connections and open testing document}
#     os.system( "/usr/bin/libreoffice '--accept=socket,host=localhost,port=2002;urp;' --writer /home/bastien/Bureau/tc_test.odt &" )
#
#     # Get local context info
#     localContext = uno.getComponentContext()
#     resolver = localContext.ServiceManager.createInstanceWithContext(
#         "com.sun.star.bridge.UnoUrlResolver", localContext )
#
#     ctx = None
#
#     # Wait until the OO.o starts and connection is established
#     while ctx == None:
#         try:
#             ctx = resolver.resolve(
#                 "uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext" )
#         except:
#             pass
#
#     # trigger our job
#     tcm = TimeCodeCorrector( ctx )
#     tcm.trigger( () )
