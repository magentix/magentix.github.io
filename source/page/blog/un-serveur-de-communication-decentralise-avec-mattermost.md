Sur un serveur dédié (chez un prestataire ou [à la maison]({{ url }}blog/un-serveur-web-a-la-maison.html)), vous pouvez installer le serveur de communication **Mattermost**, l'alternative OpenSource à **Slack**.

Si vous avez l'habitude d'utiliser **Slack**, vous ne serez pas dépaysé, l'interface est très similaire.

![Mattermost desktop application]({{ url }}media/blog/articles/mattermost.png){: width="772" height="465" }

**Mattermost** présente une version **communautaire** (team) et une version **entreprise** sous licence. Cette dernière intègre des fonctionnalités supplémentaires adaptées aux grosses structures (AD/LDAP, Elasticsearch, data retention policy, permissions avancées, analytics, support dédié...). C'est un fonctionnement assez classique pour les applications OpenSource et que j'apprécie particulièrement.

Vous pouvez installer la version **entreprise** ou la version **team**, au choix. Les 2 versions sont strictement identiques, mais la version **team** ne permet pas de débloquer les fonctionnalités **entreprise** si besoin. L'éditeur recommande donc de partir dans tous les cas sur la version entreprise.

**Mattermost** dispose d'une [marketplace](https://mattermost.com/marketplace/) pour l'intégration d'applications tiers. On y trouve la majorité des plateformes utilisées dans le monde du logiciel : Github, Gitlab, Bitbucket, Jira, Confluence, Jenkins... Mais aussi les systèmes de **visio** et de **call**, comme Appear.in, Jitsi, Microsoft teams ou encore Zoom. **Mattermost** démarre une réunion puis dirige l'utilisateur vers la plateforme correspondante (application ou navigateur), ou de façon transparente directement sur l'interface.

L'installation de **Mattermost** ne présente pas de difficultés particulières, il tourne parfaitement sur une petite machine avec simplement Apache et MySQL. C'est un énorme avantage. Pour une petite équipe ou une entreprise qui souhaite garder le contrôle de ses données, c'est l'idéal !

Cet article présente l'installation de **Mattermost** avec **Apache** et **MariaDB** / **MySQL**  sur une distribution **Debian** 10 / 11 ou **Ubuntu** (ou dérivée).
{: .info }

Je n'ai pas indiqué de `sudo` dans les commandes, vous pouvez l'ajouter ou utiliser `su -` / `sudo su -` le temps de l'installation.
{: .info }

### Serveur de base de données

#### Installation

Si cela n'est pas déjà fait, on procède à l'installation de **MariaDB** (ou de MySQL si vous préférez) :

```bash
apt-get install mariadb-server
```

Sécurisez le serveur en utilisant le script **mysql_secure_installation**. Ce script permet de supprimer les utilisateurs anonymes, d'interdire la connexion root à distance et de supprimer la base de données de test :

```bash
mysql_secure_installation
```

#### Base et utilisateur

On ajoute une nouvelle base de données et un nouvel utilisateur :

```bash
mysql -u root -p
```

```mysql
CREATE SCHEMA mattermost;
CREATE USER 'mattermost'@'%';
SET PASSWORD FOR 'mattermost'@'%' = PASSWORD('MyPassword!');
GRANT ALL ON mattermost.* TO 'mattermost'@'%' IDENTIFIED BY 'MyPassword!' WITH GRANT OPTION;
FLUSH PRIVILEGES;
```

### Serveur Mattermost

#### Installation

On télécharge la dernière version de **Mattermost**. La liste des versions est disponible dans la documentation : [Version Archive](https://docs.mattermost.com/upgrade/version-archive.html#mattermost-team-edition). Récupérez le lien correspondant à la version souhaitée, ici **entreprise 6.3.0** :

```bash
wget https://releases.mattermost.com/6.3.0/mattermost-6.3.0-linux-amd64.tar.gz
```

On extrait le contenu de l'archive dans le dossier **/opt** :

```bash
tar xvzf mattermost-6.3.0-linux-amd64.tar.gz -C /opt/
```

On ajoute un dossier **data**. C'est dans ce dossier que les fichiers envoyés et échangés par les utilisateurs sont stockés :

```bash
mkdir /opt/mattermost/data
```

**Note :** C'est ici le chemin par défaut, vous pouvez définir un autre emplacement, par exemple sur un disque ou une partition spécifique (voir **configuration**).
{: .info }

On ajoute un nouveau groupe et un nouvel utilisateur, auquels on attribut les droits sur les fichiers :

```bash
useradd --system --user-group mattermost
chown -R mattermost:mattermost /opt/mattermost
chmod -R g+w /opt/mattermost
```

Pour mettre à jour **Matermost**, réitérez ces opérations en prenant soin de conserver les données ! Les dossiers suivants ne doivent jamais être supprimés : **config**, **logs**, **plugins**, **client/plugins** et **data**. Voir la documentation officielle : [Upgrading Mattermost Server](https://docs.mattermost.com/upgrade/upgrading-mattermost-server.html).
{: .warning }

#### Configuration

On édite le fichier de configuration de **Mattermost** :

```bash
nano /opt/mattermost/config/config.json
```

Adaptez les clés suivantes :

```json
{
    "ServiceSettings": {
        "SiteURL": "https://mattermost.example.com",
        ...
    },
    ...
    "SqlSettings": {
        "DriverName": "mysql",
        "DataSource": "mattermost:MyPaword!@tcp(localhost:3306)/mattermost?charset=utf8mb4,utf8&readTimeout=30s&writeTimeout=30s",
        ...
    },
    ...
    "FileSettings": {
        "Directory": "./data/",
        ...
    },
    ...
    "PluginSettings": {
        "Directory": "/opt/mattermost/plugins",
        "ClientDirectory": "/opt/mettermost/client/plugins",
        ...
    },
    ...
}
```

- **ServiceSettings**
  - **SiteURL** : URL de votre application. Vous pouvez utiliser l'IP du serveur si vous ne disposez pas de domaine.

- **SqlSettings**
  - **DriverName** : nous utilisons le driver mysql
  - **DataSource** : information de connexion à la base de données. Adaptez le nom de l'utilisateur et le mot de passe

- **FileSettings**
  - **Directory** : adaptez si vous utilisez un emplacement spécifique pour le stockage des fichiers, sinon laisser la valeur par défaut.

- **PluginSettings**
  - **Directory** : chemin des plugins, la valeur par défaut provoque chez moi des erreurs au démarrage du serveur, il semble préférable d'indiquer le chemin absolu.
  - **ClientDirectory** : chemin des plugins client, la valeur par défaut provoque chez moi des erreurs au démarrage du serveur, il semble préférable d'indiquer le chemin absolu.

#### Service

On ajoute un nouveau service avec **systemd** :

```bash
nano /lib/systemd/system/mattermost.service
```

Copiez dans le fichier le contenu suivant :

```
[Unit]
Description=Mattermost
After=network.target
After=mysql.service
Requires=mysql.service

[Service]
Type=notify
User=mattermost
Group=mattermost
ExecStart=/opt/mattermost/bin/mattermost
TimeoutStartSec=3600
Restart=always
RestartSec=10
WorkingDirectory=/opt/mattermost
LimitNOFILE=49152

[Install]
WantedBy=mariadb.service
```

On recharge le processus **systemd** :

```bash
systemctl daemon-reload
```

On active ensuite le service pour qu'il soit pris en compte par le système et lancé à chaque démarrage :

```bash
systemctl enable mattermost
```

On démarre **Mattermost** :

```bash
systemctl start mattermost
```

On vérifie enfin que **Mattermost** est bien démarré :

```bash
systemctl status mattermost.service
```

Vous devez obtenir :

```bash
mattermost.service - Mattermost
   Loaded: loaded (/lib/systemd/system/mattermost.service; enabled; vendor preset: enabled)
   Active: active (running) since Mon 2022-01-17 10:02:28 CET; 24min ago
 Main PID: 704 (mattermost)
    Tasks: 15 (limit: 4915)
   Memory: 123.9M
   CGroup: /system.slice/mattermost.service
           └─704 /opt/mattermost/bin/mattermost
```

### Serveur Apache

#### Installation

Si votre système ne dispose pas encore d'Apache, on effectue l'installation :

```bash
apt-get install apache2
```

**Note :** vous pouvez également choisir d'utilisez **nginx**. La configuration est disponible dans la documentation officielle : [Configuring NGINX as a proxy for Mattermost Server](https://docs.mattermost.com/install/config-proxy-nginx.html)
{: .info }

On active les modules suivants :

```bash
a2enmod ssl
a2enmod rewrite
a2enmod expires
a2enmod headers
a2enmod http2
a2enmod proxy
a2enmod proxy_http
a2enmod proxy_wstunnel
```

#### Nouveau Vhost

Apache est utilisé comme proxy vers le serveur **Mattermost**. Il facilite l'accès au service. Je considère que le domaine est **example.com** et que l'on souhaite contacter le service via le sous domaine **mattermost.example.com**.

On ajoute le nouveau **VirtualHost** :

```bash
nano /etc/apache2/sites-available/mattermost.example.com.conf
```

```apache
<VirtualHost *:80>
ServerAdmin webmaster@localhost
ServerName mattermost.example.com

ProxyPreserveHost On

RewriteEngine On
RewriteCond %{REQUEST_URI} /api/v[0-9]+/(users/)?websocket [NC]
RewriteCond %{HTTP:UPGRADE} ^WebSocket$ [NC]
RewriteCond %{HTTP:CONNECTION} \bUpgrade\b [NC]
RewriteRule .* ws://127.0.0.1:8065%{REQUEST_URI} [P,QSA,L]

<Location />
Require all granted
ProxyPass http://127.0.0.1:8065/
ProxyPassReverse http://127.0.0.1:8065/
ProxyPassReverseCookieDomain 127.0.0.1 mattermost.example.com
</Location>

RewriteCond %{SERVER_NAME} =mattermost.example.com
RewriteRule ^ https://%{SERVER_NAME}%{REQUEST_URI} [END,NE,R=permanent]
</VirtualHost>
```

Remplacez les 3 entrées **mattermost.example.com** avec votre domaine.

On active le site :

```bash
a2ensite mattermost.example.com
```

```
systemctl reload apache2
```

On édite ensuite la **zone DNS** du domaine en ajoutant une entrée de type A (IP v4) pour le sous domaine (ici **mattermost**).

Pour finir, on active **SSL**. Installez **Let's Encrypt** si nécessaire :

```bash
apt-get install certbot python-certbot-apache
```

Puis exécutez la commande `certbot`.

Vous pouvez maintenant accéder facilement à la messagerie via le **navigateur**, l'application **desktop** ou **mobile**.

### Data Retention Policy

La configuration de la durée de préservation des messages est une feature **entreprise**. Si vous ne souhaitez pas alourdir la base de données avec des échanges obsolètes, vous pouvez faire le ménage facilement :

```mysql
DELETE FROM Posts WHERE CreateAt > DATE_FORMAT(NOW() - INTERVAL 30 DAY, "%Y-%m-%d 00:00:00");
```

Cette requête supprime l'intégralité des messages de plus de **30 jours**. À automatiser si besoin.