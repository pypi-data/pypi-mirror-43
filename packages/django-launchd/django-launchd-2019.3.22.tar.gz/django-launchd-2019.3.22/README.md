<!--
https://pypi.org/project/readme-generator/
-->

[![](https://img.shields.io/pypi/pyversions/django-launchd.svg?longCache=True)](https://pypi.org/project/django-launchd/)

#### Installation
```bash
$ [sudo] pip install django-launchd
```

#### Classes
class|`__doc__`
-|-
`django_launchd.models.Lock` |launchd.plist Lock class. fields: `plist` (ForeignKey), `key`
`django_launchd.models.Plist` |launchd.plist model. fields: `path`

#### Examples
init
```python
import django_launchd
from django_launchd.models import Plist

files = django_launchd.files("~/Library/LaunchAgents")
for f in files:
    Plist.objects.get_or_create(path=f)
Plist.objects.exclude(path__in=files).delete()
```

locks
```python
for agent in filter(lambda a: a.exists, Plist.objects.all()):
    if <condition>:
        agent.lock("key")
    else:
        agent.unlock("key")
```

load/unload
```python
for agent in filter(lambda a: a.exists, Plist.objects.all()):
    if agent.locks:
        agent.unload()
    else:
        agent.load()
```

<p align="center">
    <a href="https://pypi.org/project/readme-generator/">readme-generator</a>
</p>