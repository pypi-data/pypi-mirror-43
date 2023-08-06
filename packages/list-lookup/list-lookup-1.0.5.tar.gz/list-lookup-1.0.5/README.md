# ListLookup
Wrapper for faster lookups in a list of objects/dictionaries.
**ATTENTION** Do not modify list once index are created!

```
from listlookup import ListLookup
cities = ListLookup([
  {"id": 1, "country": "us", name: "Atlanta"},
  {"id": 2, "country": "us", name: "Miami"},
  {"id": 3, "country": "uk", name: "Britain"},
  {"id": 4, "country": "ca", "name": "Barrie"},
])

cities.index("id", lambda d: d['id'], True)
cities.index("country", lambda d: d['country'])

list(cities.lookup(id=1))
>>> [{"id": 1, "country": "us", name: "Atlanta"}]

list(cities.lookup(country="us", preserve_order=True))
>>> [{"id": 1, "country": "us", name: "Atlanta"}, {"id": 2, "country": "us", name: "Miami"}]

list(cities.lookup(id=2, country="uk"))
>>> []

cities.index('name', lambda d: d['name'])
list(cities.lookup(name=lambda val: val.startswith('B'))
>>> [{"id": 3, "country": "uk", name: "Britain"}, {"id": 4, "country": "ca", "name": "Barrie"}]
```

## Case insensitive index
This is not supported out of the box. You need to use same case for index and lookup values. E.g. use `.lower()`
```
from listlookup import ListLookup
cities = ListLookup([
  {"id": 1, "country": "us", name: "Atlanta"},
  {"id": 2, "country": "us", name: "Miami"},
  {"id": 3, "country": "uk", name: "Britain"},
  {"id": 4, "country": "ca", "name": "Barrie"},
])

cities.index("country_ci", lambda d: d['country'].lower())

list(cities.lookup(country_ci="UK".lower()))
>>> [{"id": 3, "country": "uk", name: "Britain"}]
```