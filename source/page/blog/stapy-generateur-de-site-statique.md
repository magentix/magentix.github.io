[StaPy](<https://www.stapy.net>) est le générateur de site statique que j'utilise depuis plusieurs mois. Le développement a été motivé par la refonte de Magentix. Le site est devenu un micro-blog, sans interaction (pas de formulaire, pas de commentaire). Un SSG (Static Site Generator) est parfaitement adapté.

Il existe des centaines de générateurs de site statique. Je voulais quelque chose de très simple. StaPy est un **mini SSG** qui s'enrichit au fur et à mesure des releases. J'aimais aussi l'idée de concevoir l'outil avec lequel j'allais travailler.

À l'heure où j'écris ce billet la version **1.7.0** vient juste de paraître. Je pense le SSG assez mature pour en parler plus largement et exposer ici les choix de conception.

- [Site officiel StaPy](<https://www.stapy.net>)
- [Magentix sur Codeberg](<https://codeberg.org/magentix>)

### Python

Il y a un énorme avantage à Python : il est disponible partout et lorsque ce n'est pas le cas il est très facile de l'installer.

Sous Windows par exemple, il peut s'installer directement depuis le Microsoft Store. Le SSG devient sur ce système un simple executable capable de lancer un serveur et de générer le site sans passer par la ligne de commande.

![Python sur le Microsoft Store]({{ url }}media/blog/articles/stapy-python-microsoft-store.jpg){: width="550" height="276"}

Sous unix il y a de fortes chances que Python soit déjà disponible sur le système car préinstallé.

### Portabilité

StaPy présente un seul script et aucune dépendance. Dans l'esprit de simplicité, je me suis imposé d'utiliser ce que permet nativement Python, sans paquet supplémentaire.

Il suffit de partager le script et les sources du site pour que n'importe quel système disposant de Python puisse générer un site, sans disposer d'une connexion Internet. Même sur Android via Termux.

![Portabilité de StaPy]({{ url }}media/blog/articles/stapy-portability.png){: width="361" height="284"}

### Compatibilité

StaPy fonctionne à partir de la version 3.4 de Python, dont la date de release est le 16 mars 2014. Il restera compatible pour cette version le plus longtemps possible. Je m'efforce de plus en plus d'intégrer la notion d'obsolescence logicielle dans mes conceptions, facilitée ici par un programme local sans dépendance dont le seul objectif est d'assembler un site.

### JSON

Le format JSON pour stocker les données est très adapté. Une solution efficace pour assurer l'interopérabilité entre les systèmes. Je peux imaginer générer les JSON de différentes manières, par exemple les récupérer depuis l'API d'une solution comme graphCMS (SAAS) ou Strapi (FOSS), et les copier sans effort. Ou tout simplement les écrire à la main.

Dans StaPy le nom du fichier correspond au chemin de l'URL, et les données qu'il contient alimentent la page (metas, titre, date, chemins des blocs et page de contenu, etc...)

```
/                 : index.html.json
/hello.html       : hello.html.json
/hello/world.html : hello/world.html.json
/hello/world/     : hello/world/index.html.json
```

```json
{
    "template": "template/default.html",
    "content":  "page/blog/post.html",

    "meta_title":       "Welcome to this new post!",
    "meta_description": "Check out a great post.",
    "title":            "This is a new post!",
    "intro":            "This post is great.",
    "author":           "Matthieu",
    "date":             "01/01/2021",

    "tags": ["post", "sitemap"]
}
```

<aside>Exemple de fichier JSON du site Magentix</aside>

La seule clé obligatoire est **template**, le reste est totalement libre.

Le format JSON permet aussi de ne pas dépendre d'un paquet supplémentaire. Cela aurait été le cas avec du YAML ou du TOML. Je le trouve également plus lisible que le XML.

### Multi environnement

Certaines données de la page comme le domaine ou les scripts analytics sont propres à l'environnement : production, développement, recette...

Il est possible de définir des variables spécifiques pour un environnement, et de générer plusieurs versions du site.

![Environnements StaPy]({{ url }}media/blog/articles/stapy-environments.png){: width="720" height="205"}

### Temps réel

La page statique est générée pour tous les environnements à chaque requête de type GET (ressources incluses). Lorsqu'une page est ajoutée ou modifiée et que je visualise le rendu dans un navigateur, la version statique est mise à jour, il n'est pas nécessaire de re-générer tout le site.

![Génération des pages en temps réel]({{ url }}media/blog/articles/stapy-realtime.png){: width="550" height="205"}

### Modularité

Une fois le serveur lancé, d'autres scripts indépendants peuvent interagir avec l'API HTTP, par exemple pour générer un sitemap ou un flux RSS.

![Serveur StaPy]({{ url }}media/blog/articles/stapy-server.png){: width="330" height="276"}

- **GET** : récupérer la liste de toutes les pages, les données d'une page ou encore la liste des environnements (JSON)
- **HEAD** : effectuer une simple requête pour générer la version statique de la page
- **PUT** : copier toutes les ressources (images, CSS, JS...) vers les environnements
- **POST** : ajouter un fichier aux environnements

Un script (en n'importe quel language) peut ainsi récupérer la liste de toutes les pages au format JSON (GET), générer un fichier `rss.xml` puis le copier sur l'environnement souhaité (POST).

### Templating

Le moteur de template est simplifié à l'extrême. Pas de condition, pas de boucle. Il effectue uniquement du remplacement.

```html
{{ name }} <-- Variable -->
{% content %} <-- Template simple (bloc) -->
{% link + hello.html %} <-- Template avec données d'une page spécifique -->
{% post ~ tags:post %} <-- Template avec boucle sur une liste de pages -->
```

L'affichage d'un bloc ou d'une variable est conditionné par les données de la page ou de l'environnement. Il est donc possible de se passer de l'instruction **if** :

```json
{
    "analytics": "",
    "analytics.prod": "template/bloc/analytics.html"
}
```

<aside>source/json/default/html.json</aside>

```html
{% analytics %}
```

<aside>template/default.html</aside>

Le bloc **analytics** est ici affiché uniquement sur l'environnement **prod**.

### Contenus

Markdown est très pratique, je me suis longuement intérrogé sur son implémentation. Il est un véritable atout pour la portabilité, l'interopérabilité et la pérennité des contenus.

L'idée est pour ce point de laisser la liberté d'implémenter Markdown sous forme de plugin externe sur le moteur de template, **prévu dans la version 1.9**.

### Légèreté

Le script pèse environ 16ko pour 450 lignes. Le challenge est d'implémenter tout ce que je souhaite le plus efficacement possible (sans dépendance).

StaPy peut être forké, modifié et partagé très facilement.

### Roadmap

- **1.7**
    - ~~Système de JSON query~~
    - ~~Enrichissement de l'API (récupération des contenus)~~

- **1.8**
    - ~~Blank thème responsive ultra léger sans javascript pour le blogging~~

- **1.9**
    - ~~Template plugin (Markdown)~~

---

- [Site officiel StaPy](<https://www.stapy.net>)
- [Magentix sur Codeberg](<https://codeberg.org/magentix>)