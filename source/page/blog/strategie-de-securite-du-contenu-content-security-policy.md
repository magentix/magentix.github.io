La mise en place d'une stratégie de sécurité du contenu avec CSP est extrêmement efficace. CSP vous permet d'éliminer les moyens de réaliser des attaques XSS en permettant de spécifier les domaines autorisés à fournir des ressources (scripts, images, CSS...) pour la page visitée.

### Configuration

Plusieurs possibilités pour inclure l'en-tête Content-Security-Policy.

#### Configuration Apache

```apache
# Content-Security-Policy
<IfModule mod_headers.c>
    Header set Content-Security-Policy "default-src 'self'"
</IfModule>
# /Content-Security-Policy
```

#### Configuration Nginx

```nginx
add_header Content-Security-Policy "default-src 'self';"
```

#### Fichier .htaccess

```htaccess
# Content-Security-Policy
<IfModule mod_headers.c>
    Header set Content-Security-Policy "default-src 'self'"
</IfModule>
# /Content-Security-Policy
```

#### Header (PHP)

```php
header("Content-Security-Policy: default-src 'self'");
```

#### Meta Tag

```html
<meta http-equiv="Content-Security-Policy" content="default-src 'self'" />
```

### Page d'exemple

Pour notre article, nous utilisons la page suivante :

```html
<!doctype html>
<html lang="fr">
    <head>
        <title>Content Security Policy</title>

        <!-- Content Security Policy -->
        <meta http-equiv="Content-Security-Policy" content="default-src 'self'" />

        <!-- Local resources -->
        <link rel="stylesheet" href="css/style.css" type="text/css" />
        <script type="text/javascript" src="js/script.js"></script>

        <!-- External resources -->
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.15.10/styles/default.min.css" type="text/css" />
        <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.15.10/highlight.min.js"></script>

        <!-- Inline CSS -->
        <style>
            h1 {
                color: #CC0000;
            }
        </style>
    </head>
    <body>
        <h1>CSP Page</h1>

        <!-- Inline CSS -->
        <p style="font-weight: bold">Content Security Policy example page</p>

        <!-- External image -->
        <img src="https://fr.wikipedia.org/static/images/project-logos/frwiki.png" alt="Wikipedia" />

        <!-- Inline Script -->
        <script type="text/javascript">
            console.log('ok');
        </script>
    </body>
</html>
```

### Application

Si vous copiez la page d'exemple dans un fichier html, **la majorité des ressources sont bloquées**. Vous obtenez dans la console du navigateur :

![Blocage des ressources par le navigateur (CSP)]({{ url }}media/blog/articles/browser-csp.png){: width="1068" height="179"}

**Chrome**

Refused to *[apply|load|execute]* the *[stylesheet|script|image|object|media|font]* *[resource]* because it violates the following Content Security Policy directive: (...)
{: .alert .csp }


**Firefox**

Content Security Policy: The page's settings blocked the loading of a resource at *[resource]* (...)
{: .alert .csp }

Content Security Policy: Les paramètres de la page ont empêché le chargement d'une ressource à *[ressource]* (...)
{: .alert .csp }

#### Ressources locales

Considérons la directive CSP suivante :

```
default-src 'self'
```

Nous indiquons ici au navigateur de ne charger que les ressources locales, c'est à dire les fichiers Javascript et CSS herbergés sur notre serveur. Dans notre page d'exemple cela correspond à :

```html
<!-- Local resources -->
<link rel="stylesheet" href="css/style.css" type="text/css" />
<script type="text/javascript" src="js/script.js"></script>
```

**Cette stratégie est la plus restrictive et sécurisée qui soit** (après la valeur "none" mais c'est un peu excessif). Par défaut nous n'autorisons que les ressources locales, les scripts et CSS inline sont ignorés.

#### Style inline

Notre page contient des styles en ligne dans le header et dans la page. Avec la directive précedente ils sont ignorés. Nous pouvons autoriser le style inline grâce à la valeur **unsafe-inline** de la directive  **style-src** :

```
default-src 'self'; style-src 'self' 'unsafe-inline'
```

Avec cette stratégie, nos styles en ligne sont maintenant interprétés :

```html
<!-- Inline CSS -->
<style>
    h1 {
        color: #CC0000;
    }
</style>
```

```html
<!-- Inline CSS -->
<p style="font-weight: bold">Content Security Policy example page</p>
```

#### Script inline

Notre page contient un script en ligne ignoré avec notre politique par défaut. Il est cependant possible d'accepter les scripts inline par le biais de la valeur **unsafe-inline** de la directive **script-src** :

```
default-src 'self'; script-src 'self' 'unsafe-inline'
```

Nous autorisons ainsi la portion de code suivante :

```html
<!-- Inline Script -->
<script type="text/javascript">
    console.log('ok');
</script>
```

Dans la pratique il est souvent complexe de ne pas autoriser les scripts en ligne, mais pour une stratégie de sécurité du contenu optimale il faut tendre à les éviter.

#### CSS externe

Nous voulons charger une ressource CSS herbergée sur un serveur distant : `cdnjs.cloudflare.com`. Cette ressource est automatiquement bloquée. Il est nécessaire de l'autoriser. Il faut pour cela indiquer le domaine concerné pour **style-src** :

```
default-src 'self'; style-src 'self' cdnjs.cloudflare.com
```

Cette stratégie nous permet de charger le CSS externe spécifié dans le header :

```html
<!-- External resources -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/.../styles/default.min.css" type="text/css" />
```

#### Script externe

Nous souhaitons charger un script herbergé sur un serveur distant : `cdnjs.cloudflare.com`. Cette ressource est bloquée par défaut. Il nous faut l'autoriser :

```
default-src 'self'; script-src 'self' cdnjs.cloudflare.com
```

Cette stratégie nous permet de charger le Script spécifié dans le header :

```html
<!-- External resources -->
<script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax.../highlight.min.js"></script>
```

#### Image externe

Pour finir, une image externe doit apparaître dans la page. Elle est également bloquée par défaut. Nous l'autorisons via **img-src** :

```
default-src 'self'; img-src 'self' fr.wikipedia.org
```

Nous acceptons ainsi l'affichage des images issues du domaine `fr.wikipedia.org` :

```html
<img src="https://fr.wikipedia.org/static/images/project-logos/frwiki.png" alt="Wikipedia" />
```

### Stratégie de sécurité

Pour afficher complétement notre page d'exemple, nous arrivons finalement à la stratégie de sécurité suivante :

```
default-src 'self'; style-src 'self' 'unsafe-inline' cdnjs.cloudflare.com; script-src 'self' 'unsafe-inline' cdnjs.cloudflare.com; img-src 'self' fr.wikipedia.org
```

La mise en place de CSP sur un site existant peut être extrêmement complexe, une politique moins restrictive (unsafe-inline) sera certainement nécessaire. L'avantage est qu'une fois établie vous maîtrisez les ressources externes et le respect des bonnes pratiques pour les intégrations futures.

Dans tous les cas **n'oubliez jamais de vérifier la console du navigateur** pour adapter si besoin votre stratégie de sécurité du contenu lors de sa mise en place.

### Autres directives

Dans notre page d'exemple nous avons abordés les directives CSP (version 1) suivantes :

- **default-src** : politique par défaut, utilisée partout sauf si surchargée par une directive plus précise
- **style-src** : la politique dédiée aux styles (CSS)
- **script-src** : la politique dédiée aux scripts
- **img-src** : la politique dédiée aux images

CSP présente d'autres directives à utiliser selon vos besoins :

- **object-src** : la politique dédiée aux plugins (éléments object, embed, ou applet)
- **media-src** : la politique dédiée aux medias (éléments video, audio, source, ou track)
- **font-src** : la politique dédiée aux polices de caractères
- **connect-src** : la politique dédiée à l'établissement de connexions depuis un objet XMLHttpRequest ou une WebSocket

Toutes les directive acceptent les valeurs **none**, **self** et une liste de domaine.

Les directives **style-src** et **script-src** acceptent également la valeur **unsafe-inline**. Il est possible d'indiquer **unsafe-eval** avec **script-src** pour autoriser l'utilisation de la méthode **eval()**.

La directive **img-src** accepte **data:** pour les images en base64 (*script-src 'self' data:*)

D'autres directives existent en CSP version 2 et 3 (form-action, child-src...). Retrouvez l'ensemble des directives sur [MDN Web Docs](https://developer.mozilla.org/fr/docs/Web/HTTP/Headers/Content-Security-Policy).

### Google Analytics

Si comme une grande majorité de sites vous implémentez Google Analytics, vous pouvez appliquer la stratégie de base suivante :

```
default-src 'self'; script-src 'self' 'unsafe-inline' www.googletagmanager.com www.google-analytics.com; img-src 'self' www.google-analytics.com
```