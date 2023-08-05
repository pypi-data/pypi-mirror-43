## Munchkin API

<img src="media/logo.png" height=100 width=100 />

Munchkin server side part of Munchkin plate game.

#### Commands

| Command              | Description
|----------------------|-----------------------------------------------------
| `make bootstrap`     | Setup package and install dependencies
| `make clean`         | Remove all generated files by other commands
| `make deploy`        | Deploy `api` on azure
| `make dist`          | Create distribuable `.tar.gz` of `API` under `dist/`
| `make doc`           | Build package documentation (`html` by default)
| `make lint`          | Run linter on all `src/` dir
| `make test`          | Run unit test (and code coverage)

##### Clean command

You can pass some extra argument to `clean` command:

```sh
make KEEP_VENV=true clean
```

to only keep `venv/` directory when cleaning `api` package.

##### Dist command

You can pass some extra argument to `dist` command:

```sh
make UPLOAD=true dist
```

to upload new `api` package to [pypi](https://pypi.org/project/munchkinapi).

##### Documentation command

You can pass some extra argument to `doc` command:

```sh
make FORMAT="html" doc
```

to build html documentation and place it under `docs/_build/html`.

Possible value for `FORMAT` are available
[here](https://www.sphinx-doc.org/en/master/man/sphinx-build.html#options).

#### Licence

Except mentionned part, this project is place under
[GNU/GPL](https://www.gnu.org/licenses/gpl.html) licences.

#### Credits

See [CONTRIBUTORS](../../CONTRIBUTORS.md), `backend` team.
