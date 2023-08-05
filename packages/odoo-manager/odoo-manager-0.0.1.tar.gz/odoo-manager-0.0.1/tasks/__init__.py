"""
Initialization of the Invoke command line tool for om.

For reference to how the pyinvoke library works, see http://www.pyinvoke.org

This handles the configuration of invoke tasks and invoke namespaces. All
invoke tasks configured by this file are either defined in their own namespace
or in the global namespace.

1. Global namespace tasks:
==========================

All tasks in the global namespace will be defined in the general.py file and
this file will automatically load the tasks from that file into the namespace
by iterating over the __dict__ attribute for the general.py module.

```
invoke run
invoke stop
invoke build
```

2. Define namespace tasks:
==========================

Each namespace must be explicitly loaded via `add_collection` and from
`from_module($module, $namespace_name)`.

```

# curl namespace...
invoke curl.authenticate
invoke curl.json

# make namespace...
invoke make.model
invoke make.view
```

"""

import inspect
import invoke
from invoke import Collection, task

from . import curl
from . import db
from . import formatter
from . import general
from . import make
from . import run
from . import scaffold
from . import setups
from . import test
from . import wiki
from .lib import configs

configs.init()
namespace = Collection()

# Configure each collection in the global namespace...
namespace.add_collection(Collection.from_module(curl, 'curl'))
namespace.add_collection(Collection.from_module(db, 'db'))
namespace.add_collection(Collection.from_module(formatter, 'format'))
namespace.add_collection(Collection.from_module(make, 'make'))
namespace.add_collection(Collection.from_module(run, 'run'))
namespace.add_collection(Collection.from_module(scaffold, 'scaffold'))
namespace.add_collection(Collection.from_module(setups, 'setup'))
namespace.add_collection(Collection.from_module(test, 'test'))
namespace.add_collection(Collection.from_module(wiki, 'wiki'))

for attribute in general.__dict__.values():
    if isinstance(attribute, invoke.tasks.Task) and inspect.getmodule(attribute.body) == general:
        namespace.add_task(attribute)
