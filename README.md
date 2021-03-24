# StaPy

StaPy is a real-time static page generator made with Python 3. The code is a file of about 180 lines to modify freely.

## Installation

Create a project directory anywhere and download the last release from the StaPy repository.

```shell
mkdir stapy
cd stapy
wget https://codeberg.org/magentix/stapy/archive/last.tar.gz
tar zxvf last.tar.gz --strip 1
rm last.tar.gz
```

## Website

Static files are generated in the `web` directory. It contains all pages and files you need to deploy (html, css, js, images...).

## HTTP server

Run standalone HTTP server:

```shell
python3 server.py
```

Access to `http://localhost:1985`

**Options:**

| Option              | Description                                 |
| ------------------- | ------------------------------------------- |
| --port PORT         | Server port to bind to (default: 1985)      |
| --hostname HOSTNAME | Server hostname (default: localhost)        |
| --tls-certfile FILE | Server TLS certificate file (default: None) |
| --tls-keyfile FILE  | Server TLS private key file (default: None) |

Example:

```shell
openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365
```

```shell
python3 server.py --port 4443 --hostname localhost.stapy --tls-certfile cert.pem --tls-keyfile key.pem
```

Access to `https://localhost.stapy:4443`

## Route

When a page is open in the browser, the server search a json file in `build/json` directory. The name of the json file is the same as the URL path. Examples:

| URL Path          | Json file                   |
| ----------------- | --------------------------- |
| /                 | index.html.json             |
| /hello.html       | hello.html.json             |
| /hello/world.html | hello/world.html.json       |
| /hello/world/     | hello/world/index.html.json |

If the json file does not exist, a **404 error** is sent.

The json file contains all the data required for generate the page:

```json
{
  "title": "Page title",
  "description": "Page description",
  "template": "build/template/default.html",
  "content": "build/page/index.html"
}
```

**template** and **content** keys are required.

## Template

The template file is the skeleton of the page:

```html
<!DOCTYPE html>
<html lang="fr">
    <head>
        <meta charset="utf-8">
        <title>{{ title }}</title>
        <meta name="description" content="{{ description }}" />
        <link rel="stylesheet" href="/css/style.css" />
    </head>
    <body>
        {% content %}
    </body>
</html>
```

* All variables in double curly braces {{ }} will be replaced with the text declared in the json file for the var.
* All variables in curly brace percent {% %} will be replaced with the content of the file declared in the json file for the var.

The **content** variable will be replaced with the content of the file defined in the json.

## Resources

All necessary resources like js, css or images are copied from the `build/web` directory to the `web` directory.

## Static files

The final static HTML files and resources are added or refreshed when the pages are opened in the browser. When `/hello.html` is open, the `hello.html` file is automatically generated in the `web` directory.

## Crawler

The website can be regenerated with a crawler (for example when the template is updated). StaPy gives a simple cURL crawler. All declared routes (json) will be reached.

```
sh crawler.sh

200 http://localhost:1985/
200 http://localhost:1985/hello.html
...
```

Use specific hostname and port if needed:

```
sh crawler.sh https://localhost.stapy:4443

200 https://localhost.stapy:4443/
200 https://localhost.stapy:4443/hello.html
...
```

Feel free to delete the `web` directory and launch the crawler.

## Netlify

Setup Netlify to deploy the `web` directory of the git repository.
