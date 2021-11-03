# StaPy

StaPy is a Static Site Generator. It works with Python without any additional package.

## Requirements

Requires Python 3.4 or newer on any operating system.

## Installation

Create a project directory anywhere and download the last release from the StaPy repository.

```shell
mkdir stapy
cd stapy
wget https://codeberg.org/magentix/stapy/archive/last.tar.gz
tar zxvf last.tar.gz --strip 1
rm last.tar.gz
```

## HTTP server

Run standalone HTTP server:

```shell
python3 server.py
```

On Windows 10 just double-click on the `server.py` file.

Then access the URL `http://localhost:1985`

## Environments

Static files are generated in the `web` directory. This directory contains all the necessary environment directories (devel, prod...).

For the production, add a `prod` directory in the `web` directory. It will contain all pages and files you need to deploy (html, css, js, images...).

After you add a new environment, you must restart the server.

## Route

When a page is open in the browser, the server search a json file in `source/json` directory. The name of the json file is the same as the URL path. Examples:

| URL Path          | Json file                   |
| ----------------- | --------------------------- |
| /                 | index.html.json             |
| /hello.html       | hello.html.json             |
| /hello/world.html | hello/world.html.json       |
| /hello/world/     | hello/world/index.html.json |

If the json file does not exist, a **404 error** is sent.

## Configuration

The json file contains all the data required for generate the page:

```json
{
  "title": "Page title",
  "description": "Page description",
  "template": "template/default.html",
  "content": "page/index.html"
}
```

The **template** key is required.

Set the environment variables with the environment suffix:

```json
{
  "url.local": "http://localhost:1985/",
  "url.prod": "https://www.example.com/"
}
```

**The environment suffix must have the same name as your environment directory.** For local rendering, the suffix is always "local".

A variable can have a default value:

```json
{
  "my_text": "All environments display this text",
  "my_text.local": "Except the local with this"
}
```

A file named **default.json** in the `source/json` directory is used for the default configuration. It will be merged with the page's json file. This is useful for a global configuration.

**default.json**
```json
{
  "title": "Default title",
  "template": "template/default.html"
}
```

**index.html.json**
```json
{
  "title": "Home title",
  "content": "page/index.html"
}
```

**default.json + index.html.json**
```json
{
  "title": "Home title",
  "template": "template/default.html",
  "content": "page/index.html"
}
```

**Note:** the **default.json** file is optional.

## Template

The template file is the skeleton of the page:

```html
<!DOCTYPE html>
<html lang="fr">
    <head>
        <meta charset="utf-8">
        <title>{{ title }}</title>
        <meta name="description" content="{{ description }}" />
        <link rel="stylesheet" href="{{ url }}css/style.css" />
    </head>
    <body>
        {% content %}
    </body>
</html>
```

* All variables in double curly braces {{ }} will be replaced with the text declared in the json file for the var.
* All variables in curly brace percent {% %} will be replaced with the content of the file declared in the json file for the var.

**Tip:** set **false** for the variable in the json file to replace it with empty text.

## Resources

All necessary resources like js, css or images are copied from the `source/web` directory in all environment directories (e.g. `web/prod`).

## Static files

The final static HTML files and resources are added or refreshed when the pages are opened in the browser. When `/hello.html` is open, the `hello.html` file is automatically generated in all environment directories (e.g. `web/prod`).

## Crawler

The website can be regenerated with a crawler. StaPy gives a python crawler script in the `tools` directory.

```
python3 tools/crawler.py {full} {delete} {copy} {crawl}
```

* **delete**: remove content from all environments
* **copy**: copy the `source/web` directory to all the environment directories
* **crawl**: generate all the pages declared in the `json` files
* **full**: delete + copy + crawl

```
python3 crawler.py full

DELETE 200
PUT 200
GET 200 /index.html
GET 200 /hello.html
...
```

## Deployment

If you are using an automated deployment tool like Netlify, Cloudflare Pages, Vercel or Render, configure the tool to deploy the environment directory from the git repository (e.g. `web/prod`).

To deploy with Github Pages, create a `docs` directory with a symlink from `web/prod` to `docs`.

```
ln -s docs web/prod
```

Commit and push the `docs` directory, then configure Github Pages to deploy `docs`.

## Themes

Simple and minimal themes for StaPy:

* [Arctic](https://www.stapy.net/themes/arctic/)
* [Dusk](https://www.stapy.net/themes/dusk/)
* [Breeze](https://www.stapy.net/themes/breeze/)