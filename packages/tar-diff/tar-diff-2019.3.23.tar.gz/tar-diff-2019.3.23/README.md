<!--
https://pypi.org/project/readme-generator/
-->

#### Installation
```bash
$ [sudo] pip install tar-diff
```

#### Features
file/url arguments supported

#### CLI
```bash
usage: tar-diff archive1 archive2
```

#### Examples
```bash
$ diff="$(tar-diff archive1.tar.gz archive2.tar.gz)"
```

complicated example. bump python project version
```bash
$ dist_dir="$(mktemp -d)"
$ python setup.py sdist --dist-dir="$dist_dir" &> /dev/null
$ sdist="$(find "$dist_dir" -type f)"
$ url="$(python -m pypi_get.urls <name> | grep tar.gz)"
$ diff="$(tar-diff "$sdist" "$url")"
$ [[ -n "$diff" ]] && bumpversion
```

<p align="center">
    <a href="https://pypi.org/project/readme-generator/">readme-generator</a>
</p>