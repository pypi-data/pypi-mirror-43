# Mucho DSL

Mucho is a Python library that provides a domain specific language (DSL) to define
rules with the form:

```
rule_name: description
conditions
=> match|mismatch|unknown
```

For example:

```
like_a_duck: it must be a duck
walks.like_a_duck and
quacks.like_a_duck and
looks.like_a_duck
=> match
```

It comes with:

- a compiler that transforms the rules into a Python object representation
- a virtual machine that evaluates the compiled rules and returns the first
satisfied one

[![Documentation Status](https://readthedocs.org/projects/mucho/badge/?version=latest)](https://mucho.readthedocs.io/en/latest/?badge=latest)

## Configure Python environment

```
pipenv install --dev
```

## Run tests

```
make test-coverage
```

## Generate docs

```
cd docs
pipenv run make html
```

## Documentation

See https://mucho.readthedocs.io .
