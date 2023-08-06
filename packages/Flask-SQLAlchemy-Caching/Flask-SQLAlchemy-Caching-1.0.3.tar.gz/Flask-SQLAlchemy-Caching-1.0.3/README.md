Flask-SQLAlchemy-Caching
========================

This is a fork of [iurisilvio's Flask-SQLAlchemy-Cache](https://github.com/iurisilvio/Flask-SQLAlchemy-Cache)

A CachingQuery implementation to Flask using Flask-SQLAlchemy and Flask-Caching.

To start using caching queries, you just have to replace Flask-SQLAlchemy `Model.query_class`.

```python
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy_caching import CachingQuery
from flask_caching import Cache

db = SQLAlchemy(app, query_class=CachingQuery)

cache = Cache(app)
```

After that, you can just make queries to a model `YourModel`:

```python
from flask_sqlalchemy_caching import FromCache

# cache is a Flask-Caching instance imported for your app init
YourModel.query.options(FromCache(cache)).get()
```

You also have `RelationshipCache` to enable lazy loading relationships from
cache.

```python
from sqlalchemy.orm import lazyload
from flask_sqlalchemy_caching import RelationshipCache

rc = RelationshipCache(YourModel.some_relationship, cache)
obj = YourModel.query.options(lazyload(YourModel.some_relationship), rc).get()

# make the query and cache the results for future queries
print(obj.some_relationship)
```

If there is a column in your table that is much more dynamic and you want to exclude it from
being cached, try using a deferred query like:
```python
YourModel.query.options(defer('crazy_column')).options(FromCache(cache)).get()
```

Take a look at [Dogpile Caching example][] to more details about how
`CachingQuery` works. Most changes to their were made just to integrate it
with Flask, Flask-SQLAlchemy and Flask-Caching instead of Dogpile.

[Dogpile Caching example]: http://docs.sqlalchemy.org/en/latest/orm/examples.html?highlight=dogpile#module-examples.dogpile_caching
