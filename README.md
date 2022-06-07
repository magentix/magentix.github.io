# Magentix

Magentix website source repository

[www.magentix.fr](https://www.magentix.fr)

The [docs](docs) directory contains the static website hosted by Github Pages.

## Licences

[Blog content](source/page/blog) is licensed under a [Creative Commons Attribution-NonCommercial 4.0 International License](https://creativecommons.org/licenses/by-nc/4.0/)

Other files are licensed under simplified BSD license (see [LICENSE](LICENCE) for details)

## Installation

1. Download [StaPy](https://codeberg.org/magentix/stapy)
2. Use the **source** and **plugins** directories from the Magentix website repository
3. Run the StaPy server

## Requirements

- Python >= 3.5
- StaPy >= 1.10.0
- [rcssmin](https://pypi.org/project/rcssmin/)
- [jsmin](https://pypi.org/project/jsmin/)
- [pytidylib](https://pypi.org/project/pytidylib/)
- [Markdown](https://pypi.org/project/Markdown/)
- [pymdown-extensions](https://pypi.org/project/pymdown-extensions/)

```
pip install rcssmin jsmin pytidylib Markdown pymdown-extensions
```

## Github Pages

We need to publish the website in the **docs** directory. A symlink from **web/prod** to **docs** must be created.

### Unix

Start a terminal and navigate to the root of the project. Then:

```shell
mkdir docs
cd web
rm -rf prod
ln -s ../docs prod
cd ..
python tools/crawler.py
```

### Windows

Start a command prompt as administrator and navigate to the root of the project. Then:

```msdos
md docs
cd web
rmdir prod
mklink /d prod ..\docs
cd ..
python tools/crawler.py
```

