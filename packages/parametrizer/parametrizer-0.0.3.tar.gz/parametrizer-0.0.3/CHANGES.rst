Changelog
=========

0.0.3 (2019-03-19)
------------------

- Provide a different mechanism in parametrize: variable substitution (mapping)
  and jinja context (context)

0.0.2 (2019-03-14)
------------------

- Adopt Jinja2 as template engine. You can use ``$name`` and ``${name}`` as usual, now
  custom expressions ``{! name.upper() !}`` or any other Jinja2 constructs are supported
  too

0.0.1 (2019-01-16)
------------------

- First release
