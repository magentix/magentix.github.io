# Magentix

Magentix website source repository

[www.magentix.fr](https://www.magentix.fr)

The [docs](docs) directory contains the static website hosted by Github Pages.

## Licences

**Blog content** is licensed under a [Creative Commons Attribution-NonCommercial 4.0 International License](https://creativecommons.org/licenses/by-nc/4.0/)

**Static files** are licensed under simplified BSD license (see [LICENSE](LICENCE) for details)

## Installation

1. Download [StaPy](https://codeberg.org/magentix/stapy)
2. Use the **source** and **plugins** directories from the Magentix website repository
3. Run the StaPy server

## Requirements

- Python >= 3.4
- StaPy >= 1.9
- [rcssmin](https://pypi.org/project/rcssmin/)
- [jsmin](https://pypi.org/project/jsmin/)
- [Markdown](https://pypi.org/project/Markdown/)
- [pymdown-extensions](https://pypi.org/project/pymdown-extensions/)

## Github Pages

We need to publish the website in the **docs** directory. A symlink from **web/prod** to **docs** must be created:

```shell
mkdir docs
cd web
rm -rf prod
ln -s ../docs prod
cd ..
python3 tools/crawler.py
```