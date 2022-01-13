![Datacenter]({{ url }}media/blog/articles/datacenter.jpg){: width="800" height="250" }

Il n'est pas rare avec les solutions de déploiement automatisé de sites statiques de trouver des offres gratuites. Ce sont souvent des offres d'appel, limitées, pour vendre ensuite une solution plus complète.

Mais dans de nombreux cas ces offres suffisent largement. Les sites de votre plombier, de votre ostéopathe ou du restaurant japonais au bas de la rue pourraient bien souvent être hébergés gratuitement s'ils étaient statiques (on trouve très souvent du Wordpress). Sans parler de l'impact écologique.

Un thread sur twitter de Arnaud Ligny (créateur du SSG [Cecil](<https://cecil.app/>)) résume parfaitement la situation :

> Je vois beaucoup de sites Web dont le contenu change très rarement, servi par un backend qui est potentiellement appelé à chaque visite : quel gâchis de ressources ! (...) L'autre intérêt d'un site statique c'est sa capacité à être migré en cas de soucis d'hébergement : n'importe serveur Web fera l'affaire si vous maîtrisez le nom de domaine. Sans parler de la monter en charge : sans BDD il devient très facile de déployer un site sur un réseau CDN.

<aside><a href="https://twitter.com/ArnaudLigny/status/1447146996960215041">Lire le thread complet</a></aside>

Je me suis intéressé aux offres gratuites des solutions d'hébergement sur un CDN.

## Sélection des solutions

Je n'ai pas utilisé les services de build des solutions de déploiement. Je génère le site statique localement et pousse le résultat sur Github. Il ne reste plus qu'à trouver un espace sur le web pour partager les fichiers.

J'ai retenu **6 solutions** : Github Pages, Gitlab Pages, Netlify, Vercel, Render et Cloudflare Pages.

Pour les tests j'ai utilisé le site Magentix (celui que vous lisez actuellement) que j'ai hébergé (temporairement) sur 6 sous-domaines :

- [**Github Pages**](<#github>) : github.magentix.fr
- [**Gitlab Pages**](<#gitlab>) : gitlab.magentix.fr
- [**Netlify**](<#netlify>) : netlify.magentix.fr
- [**Vercel**](<#vercel>) : vercel.magentix.fr
- [**Render**](<#render>) : render.magentix.fr
- [**Cloudflare Pages**](<#cloudflare>) : cloudflare.magentix.fr

Ces 6 solutions proposent toutes gratuitement les fonctionnalités qui m'intéressent :

- Publication automatique d'une branche du dépôt
- Nom de domaine personnalisé via l'ajout d'un enregistrement CNAME sur la zone DNS
- Génération automatique du certificat SSL
- Page d'erreur 404 personnalisable
- Cache local des ressources
- HTTP 2

Les bandes passantes sont souvent limitées à 100GB. Cela correspond à 1.000.000 de pages vues par mois pour des pages de 100ko. Cette bande passante est partagée par **tous les sites** de votre compte.

Petite exception avec **Cloudflare Pages** qui propose une bande passante illimitée dans son offre gratuite.

Les tests vont s'attarder sur les points suivants :

- Facilité de configuration
- En-têtes HTTP personnalisables
- Stockage
- Temps de latence

Le temps de latence est un critère primordial : le site est dans le cloud, AWS, cloudflare, Digital Ocean, Azure... Si le serveur est à l'autre bout de la planète c'est un peu moins intéressant pour moi. Je trouve un peu dommage d'attendre 400ms juste pour récupérer un fichier statique de 5ko.

Il est important de se rapprocher au maximum des utilisateurs, mais n'oublions pas que nous sommes sur des offres gratuites, plus limitées.

J'effectue les tests de TTFB (Time To First Byte) depuis chez moi avec des requêtes toutes les 30 secondes sur les 6 sous-domaines.

**Note :** je publie des fichiers statiques avec les offes **gratuites** des solutions de déploiement automatisés. Ce comparatif ne s'attarde pas sur les outils de build ni sur les avantages des offres payantes. **La conclusion serait alors complétement différente**.
{: .info }

## Analyses

### Github Pages {: #github }

Pour utiliser **Github Pages** gratuitement, il faut accepter que son site soit déposé sur un repository public. C'est le gros point noir de l'offre gratuite.

Il n'est pas possible de customiser les en-têtes HTTP, pour ajouter par exemple une [directive CSP](<{{ url }}blog/strategie-de-securite-du-contenu-content-security-policy.html>) ou X-Frame-Options.

Pour le reste c'est assez fluide, il m'a fallu environ 10 minutes pour mettre le site en ligne. Pas besoin d'un outil supplémentaire qui viendrait cloner le dépôt.

Les fichiers statiques sont disponibles sur le dépôt (username.github.io) et on ajoute l'entrée CNAME sur la zone DNS.

Le site ne doit pas excéder les 1GB. Les temps de réponse sont très bons et réguliers, avec une moyenne de **59ms** sur 7 jours.

------

+ Temps de réponse excellent
  {: .compare .positive }
+ Mise en ligne très simple
  {: .compare .positive }
+ Pas d'outil supplémentaire
  {: .compare .positive }
- Dépôt public
  {: .compare .negative }
- En-têtes HTTP non personnalisables
  {: .compare .negative }

------

### Gitlab Pages {: #gitlab }

Contrairement à son concurrent Github, Gitlab permet de publier un site sur un dépôt privé. On peut donc gérer le site et le déployer sur la même plateforme, le tout gratuitement.

La mise en ligne n'a pas posé de problèmes particuliers mais je suis plutôt habitué à utiliser Gitlab. J'ai cependant toujours trouvé l'interface moins ergonomique que celle de Github. La configuration du site statique reste plus complexe qu'avec les autres solutions, moins facile d'accès.

Il n'est pas possible de customiser les en-têtes HTTP. Celles-ci sont par contre peu nombreuses (8 contre une vingtaine pour Github). Notez que Gitlab ajoute de base la directive `permissions-policy: interest-cohort=()` pour la désactivation de l'algorithme Google FLoC.

Gitlab accuse un temps de réponse très élevé, avec depuis la France un TTFB moyen de **387ms** sur 7 jours. Avec une sonde depuis les US ce n'est pas beaucoup mieux, le TTFB moyen obtenu est de **317ms**.

La compression des ressources (gzip) n'est pas effectuée par défaut, il faut l'ajouter au script de déploiement :

```
pages:
  # Other directives
  script:
  - find public -type f -regex '.*\.\(html\|js\|css\)$' -exec gzip -f -k {} \;
```

<aside>.gitlab-ci.yml</aside>

------

+ Pas d'outil supplémentaire
  {: .compare .positive }
+ Dépôt privé
  {: .compare .positive }
- Temps de réponse très élevé
  {: .compare .negative }
- Configuration complexe
  {: .compare .negative }
- En-têtes HTTP non personnalisables
  {: .compare .negative }

------

### Netlify {: #netlify }

Netlify est le CDN que j'ai choisi il y a quelques mois pour héberger Magentix. je n'avais pas vraiment réalisé de comparatif. En quelques minutes le site était en ligne et c'était très satisfaisant (clone du dépôt Github et modification du CNAME). L'expérience utilisateur de l'outil est excellente.

Mais j'ai constaté sur Netlify des changements de serveur et de localisation : parfois aux US avec un TTFB d'environ 200ms, parfois en Allemagne avec TTFB de 130ms. Parfois sur un cloud AWS, parfois sur un cloud Digital Ocean. Il en résulte des inégalités dans la délivrabilité des pages. En moyenne sur 7 jours j'obtiens un TTFB de **147ms**.

Il est possible de customiser les en-têtes HTTP avec un simple fichier `_headers` à la racine du site.

```
/*
  X-Frame-Options: DENY
```

------

+ Mise en ligne très simple
  {: .compare .positive }
+ En-têtes HTTP personnalisables
  {: .compare .positive }
- Temps de réponse élevé et irrégulier
  {: .compare .negative }

------

### Render {: #render }

Render présente une offre gratuite dans la moyenne. Les temps de réponse sont acceptables : 50ms et 300ms toutes les 5 minutes, pour une moyenne de **105ms** sur 7 jours.

L'installation du site est facile (environ 10 minutes : clone du dépôt et ajout du CNAME), il est possible de customiser les headers directement sur l'interface, ce qui est plutôt pratique.

Il est tout de même obligatoire d'enregistrer une carte bancaire pour continuer d'utiliser le service, même si vous n'utilisez que l'offre gratuite. C'est un frein pour beaucoup.

------

+ Mise en ligne très simple
  {: .compare .positive }
+ En-têtes HTTP personnalisables
  {: .compare .positive }
- CB obligatoire même pour l'offre gratuite
  {: .compare .negative }
- Temps de réponse moyen
  {: .compare .negative }

------

### Vercel {: #vercel }

Vercel présente un très bon TTFB. Les réponses sont constantes, avec une moyenne de **69ms** sur 7 jours. C'est la seule solution de ce comparatif à répondre depuis un serveur Français (AWS Paris), depuis chez moi.

L'interface est épurée, la configuration du site très facile (clone du dépôt, ajout du CNAME).

Il est tout à fait possible de modifier les en-têtes HTTP via un fichier `vercel.json` à la racine du projet (nécessite un déploiement avec vercel CLI).

```json
{
  "headers": [
    {
      "source": "/(.*)",
      "headers" : [
        {
          "key" : "X-Frame-Options",
          "value" : "DENY"
        }
      ]
    }
}
```

------

+ Temps de réponse très bon
  {: .compare .positive }
+ Mise en ligne très simple
  {: .compare .positive }
+ En-têtes HTTP personnalisables
  {: .compare .positive }

------

### Cloudflare Pages {: #cloudflare }

La solution de déploiement **Cloudflare Pages** a été lancée en avril 2021. Cloudflare est le spécialiste du CDN et dispose de sa propre infrastructure, c'est un énorme avantage.

En 15 minutes le site était en ligne, l'interface est sobre et va à l'essentiel. On peut simplement noter un temps de build supérieur aux concurrents. Il faut compter environ 3 minutes pour déployer le site (soit 3 minutes entre un commit et la publication des modifications).

J'ai obtenu un TTFB moyen depuis la France de **80ms**, ce qui représente un très bon résultat.

Cloudflare propose la customisation des en-têtes HTTP depuis un simple fichier `_headers` à la racine du site.

```
/*
  X-Frame-Options: DENY
```

------

+ Temps de réponse très bon
  {: .compare .positive }
+ Mise en ligne très simple
  {: .compare .positive }
+ En-têtes HTTP personnalisables
  {: .compare .positive }

------

## Conclusion

Mon premier choix pour l'hébergement gratuit d'un site statique est **Vercel**. Un très bon temps de réponse et une interface au top.

Suivi de très près par **Cloudflare Pages** avec un temps de réponse légèrement supérieur.

**Github Pages** vient en troisième position mais c'est une excellente alternative dans le cas où le dépôt public ne serait pas une contrainte. Il est tout de même dommage de ne pas pouvoir modifier les headers.

Je place **Netlify** en quatrième position, pénalisé par un temps de réponse depuis la France assez médiocre par rapport aux concurrents.

Pour finir **Gitlab Pages** avec un temps de réponse très mauvais, suivi de **Render** avec un temps de réponse moyen et l'obligation de renseigner une carte bancaire.

![Temps de réponse moyen hébergement]({{ url }}media/blog/articles/static-website-tools-ttfb.jpg){: width="850" height="600" }

Il est possible que les offres ne restent pas gratuites indéfiniment ou que les solutions disparaissent un jour. Ce fût par exemple le cas de **fast.io**, qui a tout simplement mis fin à son service de déploiement de sites statiques. Si cela devait arriver, il serait tout de même très facile et rapide de changer de solution.