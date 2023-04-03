# ievv_opensource

## Develop
Requires:
- https://github.com/pyenv/pyenv
- Docker (Docker desktop or similar)


### Use conventional commits for GIT commit messages
See https://www.conventionalcommits.org/en/v1.0.0/.
You can use this git commit message format in many different ways, but the easiest is:

- Use commitizen: https://commitizen-tools.github.io/commitizen/commit/
- Use an editor extension, like https://marketplace.visualstudio.com/items?itemName=vivaxy.vscode-conventional-commits for VScode.
- Just learn to write the format by hand (can be error prone to begin with, but it is fairly easy to learn).


### Install hatch and commitizen
NOTE: You only need hatch if you need to build releases, and you
only need commitizen for releases OR to make it easy to follow
conventional commits for your commit messages
(see _Use conventional commits for GIT commit messages_ above).

First install pipx with:
```
$ brew install pipx
$ pipx ensurepath
```

Then install hatch and commitizen:
```
$ pipx install hatch 
$ pipx install commitizen
```

See https://github.com/pypa/pipx, https://hatch.pypa.io/latest/install/
and https://commitizen-tools.github.io/commitizen/ for more install alternatives if
needed, but we really recommend using pipx since that is isolated.


### Install development dependencies

Install a local python version with pyenv:
```
$ pyenv install 3.10
$ pyenv local 3.10
```

Install dependencies in a virtualenv:
```
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install ".[dev,optional]"
```


### Run postgres and redis
```
$ docker-compose up
```

### Run dev server
```
$ source .venv/bin/activate   # enable virtualenv
$ ievv devrun -n docker-compose
```

### Run tests
```
$ source .venv/bin/activate   # enable virtualenv
$ pytest
```


### Destroy postgres and redis
```
$ docker-compose down -v
```


## Documentation
http://ievv-opensource.readthedocs.org/


## How to release ievv_opensource

Release (create changelog, increment version, commit and tag the change) with:
```
$ cz bump
$ git push && git push --tags
```

NOTE:
- ``cz bump`` only works if conventional commits (see section about that above) is used.
- ``cz bump`` can take a specific version etc, but it automatically select the correct version
  if conventional commits has been used correctly. See https://commitizen-tools.github.io/commitizen/.
- The ``cz`` command comes from ``commitizen`` (install documented above).

Release to pypi:
```
$ hatch build -t sdist
$ hatch publish
$ rm dist/*              # optional cleanup
```


