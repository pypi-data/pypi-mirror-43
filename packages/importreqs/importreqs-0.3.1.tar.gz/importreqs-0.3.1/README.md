# importreqs

A simple Python lib for extracting reqs.txt from currently imported libs in the context. The lib can be used in the following scenarios:

- Gathering the dependencies for serverless frameworks such as AWS Lambda. If several functions share the same virtualenv, unused dependecies may be introduced via ```pip freeze```. Use importreqs will expose only the reqs imported.
- Remove unused dependencies after refactoring, or on a long time maintained projects.

## Install

```
pip install importreqs
```

## Usage

To use importreqs:

```
import importreqs
importreqs.generate_reqs(replace_version_hash=False,
                         exclude=None)
```

- __replace\_version\_hash__: For editable reqs(with -e when using pip install), remove the commit hash from result.
- __exclude__: Exclude listed packages from the result. For example, importreqs itself.

For example:

```
# import your own projects
# for example "import app"

import importreqs

print(importreqs.generate_reqs(exclude=['importreqs']))
```

Or use importreqs from command line:

```
importreqs -c "import requests"
```