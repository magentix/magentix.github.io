Pour bien comprendre la philosophie de **Gemini**, comparons le avec **HTTP**.

### HTTP vs Gemini

#### HTTP

<section markdown="1">

**Requête :**

```
GET /index.html HTTP/1.1
Host: example.com
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate, br
X-What-I-Want: Foo
```

**Réponse :**

```html
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Set-Cookie: PHPSESSID=be071caaf83bf8539310818360720a84
X-What-I-Want: Bar

<!DOCTYPE html>
<html>
    <head>
        <title>Hello World!</title>
    </head>
</html>
<body>
    <h1>Welcome!</h1>
    <p>This is a page</p>
</body>
```
</section>

#### Gemini

<section markdown="1">

**Requête :**
```
gemini://example.com/index.gmi
```

**Réponse :**

```gemtext
20 text/gemini
# Welcome !

This is a page
```
</section>

### Philosophie

Gemini se veut simple, léger, rapide, mais surtout... fermé. Il a pour unique vocation de servir du texte dans un format Markdown simplifié appelé [Gemtext](https://gitlab.com/gemini-specification/gemini-text). La requête et l'en-tête de réponse sont sur une seule ligne, empêchant toute extensibilité. Il est impossible avec le protocole Gemini de créer quelque chose qui s'apparente à un cookie. Pas de session ni de traçage des internautes.

C'est une réponse extrême aux dérives du web. Gemini est parfaitement présenté par [Ploum](http://ploum.net/) dans l'article [Gemini, le protocole du slow web](https://ploum.net/gemini-le-protocole-du-slow-web/).

![Gemini via le navigateur Lagrange]({{ url }}media/blog/articles/gemini-lagrange.png){: width="776" height="488" }

### Retour d'expérience

Nous sommes sur un exemple parfait d'idéologie à des années-lumières de ce qu'est le web et de ce qu'il tend à devenir. C'est un mouvement protestataire, initié par un certain [Solderpunk](https://www.circumlunar.space/~solderpunk/) et relayé par quelques personnalités comme Drew DeVault : [What is this Gemini thing anyway, and why am I excited about it?](https://drewdevault.com/2020/11/01/What-is-Gemini-anyway.html) ou Stéphane Bortzmeyer : [Le protocole Gemini, revenir à du simple et sûr pour distribuer l'information en ligne ?](https://www.bortzmeyer.org/gemini.html). On parle également de Gemini dans quelques débats sur [Hacker News](https://news.ycombinator.com/).

En naviguant sur les capsules (sites Gemini), on découvre le partage de technophiles altruistes, de philosophes, de poètes (beaucoup d'haiku), d'écrivains amateurs, d'artistes ASCII Art, ou encore d'écologistes low-tech. On y trouve quelques fans de [Gopher](https://fr.wikipedia.org/wiki/Gopher), habitués à ces espaces cachés, loin de toute agitation.

Pour partager du contenu via le protocole Gemini, il faut un serveur à disposition et quelques connaissances en administration système. Certains proposent un service d'hébergement ([Flounder](https://flounder.online/), [pollux.casa](https://pollux.casa/)), mais c'est de mon point de vue un peu délicat de poser des fichiers sur un serveur dont on ignore s'il sera encore à disposition le lendemain.

On déplore malheureusement beaucoup de capsules à l'abandon, fermées ou juste là pour le challenge technique. Pour ma part, je me suis trouvé rapidement limité par le Gemtext très simpliste, avec l'impossibilité même d'afficher un texte en gras. Pour la rédaction d'articles techniques ou scientifiques, le format n'est pas adapté. Trop limité et austère. Les capsules manquent finalement d'identité.

Il faut donc accepter de partager simplement une idée, une opinion, un état d'âme ou une histoire, sans échange ni retour. Une bouteille à la mer.

Des demandes ont été formulées pour faire évoluer les [spécifications](https://gitlab.com/gemini-specification/protocol) : ajouter des fonctionnalités comme des formulaires, le partage de fichiers ou de l'échange par message. Cela est sujet à des débats sans fin. Pour Drew DeVault cela n'a pas de sens :

> Gemini is not a protocol for publishing. We use a different protocol for that, like git or rsync. It's not interactive, either, at least not in the same sense as the web is. It is a protocol for consumption: for reading hyperlinked Gemtext documents.

Solderpunk, après plusieurs mois d'absence, a également mis les choses au point. Concernant le Gemtext il annonce :

> Additional capacities in the gemtext format are not necessary. That's not just, like, my opinion, man, that's an empirical fact. Geminispace is there. It's *exactly* the kind of space I originally envisaged.

Gemini restera visiblement ce qu'il est (sauf si **Solderpunk** et **Sean Conner** passe le relais). Il ne convient pas pour ce que je souhaite partager, mais je continue d'y naviguer à mes heures perdues.

Techniquement, le protocole est plutôt intéressant : il permet de mettre en place son propre serveur, le maîtriser de A à Z. Gemini laisse place à la créativité.

### Un serveur Gemini

#### TCP

La lecture des [spécifications](https://gitlab.com/gemini-specification/protocol) ne demande que quelques minutes. Ce pourrait être un parfait sujet de TP dans le cadre d'une formation en réseau et développement : "développer un serveur et un client respectant les spécifications décrites dans ce document". La simplicité a d'ailleurs séduit une multitude de développeurs, on trouve des serveurs et clients Gemini dans tous les langages : Java, Python, Rust, Go, PHP, C, Perl, shell, Kotlin, Ruby, Erlang... Certains ultra légers, d'autres plus complets avec par exemple la gestion d'une authentification TOFU ou l'utilisation de scripts CGI.

Le serveur consiste en l'intégration d'un socket à l'écoute des requêtes envoyées au port 1965, et d'y répondre avec le contenu sollicité. Comme pour HTTP 1 et 2, Gemini utilise TCP comme couche de transport. Un aspect sécurité est bien attendu à prendre en compte, car il ne s'agit pas d'exposer au monde l'intégralité des fichiers d'une machine. Notez qu'avec Gemini, TLS est obligatoire. Il faut générer un certificat (auto-signé ou non) au préalable.

Pour tester rapidement, on installe **nmap** (ou **ncat** directement si disponible) :

```bash
apt install nmap
```

On génère un certificat auto-signé (sans passphrase, avec le FQDN du serveur) :

```bash
openssl req -nodes -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365
```

On ouvre enfin une connexion TCP sur le port 1965 via ncat :

```bash
while true ; do echo -e "20 text/gemini\r\nHello!" | ncat -lvnp 1965 --ssl --ssl-key key.pem --ssl-cert cert.pem ; done
```

 L'accès au serveur via n'importe quel client Gemini (par exemple [Lagrange](https://github.com/skyjake/lagrange) ou [deedum](https://play.google.com/store/apps/details?id=ca.snoe.deedum&hl=fr&gl=US) sur Android) affiche :

```
Hello!
```

On peut également transmettre une requête en ligne de commande avec **ncat** ou **openssl** :

```bash
echo "gemini://127.0.0.1/" | ncat --ssl 127.0.0.1 1965
```

```bash
echo "gemini://127.0.0.1/" | openssl s_client -connect 127.0.0.1:1965 -crlf -quiet -ign_eof 2> /dev/null
```

Dans cet exemple la requête n'a aucune importance, la réponse est toujours la même.

#### Requête

Une requête Gemini est de la forme : `{scheme}://{host}/{path}`

- **scheme** : gemini *(une autre valeur engendre une erreur 53 ou 59)*
- **host** : IP ou domaine *(utile pour gérer plusieurs hosts sur un même serveur)*
- **path** : chemin de la page

Par exemple : `gemini://example.com/index.gmi`

```bash
echo "gemini://magentix.space/index.gmi" | ncat --ssl magentix.space 1965
```

#### En-tête de réponse

Les codes de statut sont sur 2 digits, il y en a 18 au total (le *11 SENSITIVE INPUT* est cependant sur la sellette car non approprié au concept). On retiendra les statuts suivants :

- 20 SUCCESS
- 31 REDIRECT - PERMANENT
- 50 PERMANENT FAILURE
- 51 NOT FOUND
- 53 PROXY REQUEST REFUSED
- 59 BAD REQUEST

Les autres statuts ont un intérêt dans des cas particuliers, je ne m'y attarde pas.

On suffixe systématiquement l'en-tête avec CRLF (\r\n).

#### Corps de la réponse

Le corps de la réponse contient du texte, encodé en UTF-8. Pour le Gemtext on indique le mimetype **text/gemini**.

```gemtext
20 text/gemini
# Hello!

Welcome to my capsule.

=> ./about.gmi Who am I?
```

On pourrait envoyer n'importe quel type de fichier (image/png, audio/mpeg...), avec les données binaires. Mais cela implique que le client puisse les lire ou les proposer au téléchargement. Ce n'est pas le but de Gemini. Peu de clients le font.

#### Un peu de code...

On dispose maintenant de suffisamment d'informations pour coder un serveur Gemini, dans n'importe quel langage. Quelque chose de volontairement assez basique en **PHP 8** ressemble à ceci :

```php
<?php

declare(strict_types=1);

error_reporting(E_ALL & ~E_WARNING & ~E_NOTICE);

const ROOT = __DIR__ . '/';

$resource = stream_context_create(
    [
        'ssl' => [
            'local_cert' => ROOT . 'cert.pem',
            'local_pk' => ROOT . 'key.pem',
            'allow_self_signed' => true,
            'verify_peer' => false,
        ]
    ]
);
$socket = stream_socket_server(address: 'tlsv1.3://0:1965', context: $resource);

while (true) {
    if (!($fSocket = stream_socket_accept($socket, -1))) {
        continue;
    }
    fwrite($fSocket, getContent(parse_url(trim(fread($fSocket, 1024) ?: '')) ?: []));
    fclose($fSocket);
}

/**
 * Retrieve the response content
 *
 * @param string[] $url
 * $url = [
 *     'scheme' => (string) scheme name (gemini)
 *     'host'   => (string) host name (magentix.space)
 *     'path'   => (string) requested page (/about.gmi)
 * ]
 *
 * @return string
 */
function getContent(array $url): string
{
    if (($url['scheme'] ?? '') !== 'gemini') {
        return "59 bad request\r\n";
    }

    $path = $url['path'] ?? '/index.gmi';
    if (!str_ends_with($path, '.gmi')) {
        $path = rtrim($path, '/') . '/index.gmi';
    }
    
    $file = ROOT . 'capsule' . str_replace('../', '', $path);
    if (!file_exists($file)) {
        return "51 Not found\r\n";
    }

    return "20 text/gemini\r\n" . file_get_contents($file);
}
```

<aside>server.php</aside>

Dans le même dossier que le script on génère le certificat (indiquez le FQDN du serveur pour le nom commun) :

```bash
openssl req -nodes -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365
```

```
Country Name (2 letter code) [AU]: US
State or Province Name (full name) [Some-State]: Washington
Locality Name (eg, city) []: Olympia
Organization Name (eg, company) [Internet Widgits Pty Ltd]: MyCompany
Organizational Unit Name (eg, section) []: IT
Common Name (e.g. server FQDN or YOUR name) []: example.com
Email Address []: hello@example.com
```

Le dossier **capsule** contient les fichiers **gemtext**. Le serveur retourne par défaut le contenu du fichier **index.gmi** :

```gemtext
# It works!

Start your new amazing capsule.
```

<aside>capsule/index.gmi</aside>

On démarre enfin le serveur :

```bash
php server.php &
```

[Code source](https://github.com/magentix/leo) sur Github.

### Conclusion

L'idée d'un protocole simple, plus sûre et respectueux de la vie privée a du sens. Mais Gemini est de mon point de vue un peu extrême. Le Gemtext est bien trop limité pour apporter du dynamisme à une lecture, de l'identité à une capsule. Il facilite le développement du client, c'est là le but recherché. Mais proposer un Markdown plus complet aurait été bien plus intéressant.

Travailler sur le protocole est tout de même inspirant. On est au plus bas de la couche application (socket), idéal pour un développement hyper léger, optimisé et maîtrisé. On peut tout imaginer. Un ingénieur logiciel, [Michael Lazar](https://mozz.us/), s'est amusé à écrire une [spécification](https://portal.mozz.us/spartan/spartan.mozz.us/specification.gmi) (The Spartan Protocol) très inspirée de Gemini.

Au-delà de l'aspect technique, je suis curieux de l'avenir du protocole. Il n'évoluera plus, ou très peu. Il semble bien parti pour suivre le même chemin que Gopher : un espace un peu caché, un lieu d'expression (textuel) pour celles et ceux fatigués par la lourdeur du web que l'on connaît.

Pour allez plus loin avec Gemini :

- [Awesome Gemini](https://github.com/kr1sp1n/awesome-gemini)
- [Gemini Quickstart!](https://geminiquickst.art/)
- [Spécification Gemini](https://gitlab.com/gemini-specification)
