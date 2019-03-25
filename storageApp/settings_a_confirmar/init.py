from .base import *
# you need to set "myproject = 'prod'" as an environment variable
# in your OS (on which your website is hosted)
if os.environ['STORAGE_APP'] == 'prod':
    from .prod import *
else:
    from .dev import *

