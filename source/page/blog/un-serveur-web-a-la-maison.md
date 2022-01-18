Cet article détaille l'installation complète d'un serveur Web avec **Apache** sous **Debian** derrière une connexion fibrée **Free**. Il peut être adapté avec n'importe quel système (Ubuntu, Fedora, FreeBSD...) et n'importe quel serveur (Nginx, node.js, Tomcat, Lighttpd...).
{: .info }

### Sommaire {: #p0 }

- [Introduction](#p1)
- [Quels sont les risques ?](#p2)
- [Free et la fibre](#p3)
- [Quelle machine ?](#p4)
- [Image d'installation](#p5)
- [Préparer une clé USB bootable](#p6)
- [Installation du système d'exploitation](#p7)
- [Configuration du système](#p8)
- [Installation du serveur Web](#p9)
- [Redirection des ports 80 et 443](#p10)
- [Configuration du vhost](#p11)
- [Enregistrement DNS](#p12)
- [Certificat SSL Let's Encrypt](#p13)

### Introduction {: #p1 }

Pour héberger un site perso, un site statique, un blog, échanger des ressources avec des proches, installer une application, gérer du code, se former, ou juste pour le fun, un serveur web maison est idéal. Pour une agence, c'est aussi un excellent moyen de mettre en place gratuitement et rapidement des instances de recette, proposer des démos aux clients, du bug tracking...

Mais il y a également une question de souplesse et de liberté, vous faites absolument ce que vous souhaitez de la machine. Pas d'engagement, pas de condition, pas de paiement. Personne ne vous facturera 10€ par mois pour l'utilisation d'une version obsolète de PHP (la spécialité chez Ionos). Nos applications sont là, à proximité, et il suffit de débrancher une prise pour les déconnecter. Si vous visitez [magentix.space](https://magentix.space/) (serveur d'expérimentation), vous n'êtes pas dans un data center à Roubaix ou à Francfort, non, vous êtes dans mon entrée, sur un meuble en rotin.

![Freebox Delta]({{ url }}media/blog/articles/freebox.png)

### Quels sont les risques ? {: #p2 }

Au quotidien, nous ne sommes jamais à l'abri d'une coupure de courant ou d'un problème réseau.

Pour les coupures de courant, un onduleur est assez efficace. Il garantit une continuité électrique et permet de se protéger des micros coupures ou des chutes de tension. J'ai acheté il y a quelques années un **Eaton Ellipse ECO 650**, 650VA, batterie 12V, 7Ah, soit au minimum 6h d'autonomie pour une machine de 10 Watts (marge de 20%) :

```
7Ah / ( 10w / 12v ) * 0.8 = 6.72h
```

Pour les longues coupures, liées par exemple aux intempéries, il faudra prendre votre mal en patience. Si vous utilisez le CPL pour communiquer avec des équipements réseaux (comme le boîtier TV), il n'est pas possible de brancher la box sur l'onduleur. Le CPL ne fonctionnera plus.

**Note :** Une **freebox delta** (équipée d'un seul disque dur 2,5") consomme **27,2 Watts**. Avec le **Eaton Ellipse ECO 650** elle continuera de fonctionner environ **2.5h** si elle est branchée seule. Si la panne de courant concerne également le NRO il n'y aura plus la fibre non plus, mais les NRO sont également équipés d'un onduleur...
{: .warning }

Pour les problèmes réseaux entre le terminal optique du logement et les équipements de l'opérateur, cela reste assez rare. En 3 ans cela m'est arrivé à 2 reprises : un mauvais branchement du technicien lors d'une intervention sur la baie. Dans ce cas, la déconnexion peut durer plusieurs jours, le temps que le technicien se déplace pour constater la panne et réparer. Les pannes générales sur les répartiteurs sont souvent traitées rapidement. Les opérateurs ne laissent jamais plusieurs centaines d'abonnées sans connexion.

**De manière générale, c'est à vous de juger l'intérêt d'une installation selon les pannes rencontrées dans votre région et l'utilisation que vous souhaitez faire du serveur.** Si vous déménagez 2 fois par an cela risque d'être également un peu contraignant.

Je pense qu'il faut éviter d'héberger à la maison un site ou une application pour lesquels une déconnexion peut avoir un impact important pour les utilisateurs, la visibilité et l'activité.

### Free et la fibre {: #p3 }

Free est l'un des seules opérateurs en France à proposer depuis toujours l'attribution d'une IP v4 fixe (sur demande). Gratuitement. Pour monter un serveur c'est important. Dans le cadre d'une installation domotique pilotée à distance également. Chez Orange cela est réservé aux professionnels, chez les autres je ne sais pas mais il me semble que c'est impossible. Il faut dans ce cas se tourner vers des solutions DynDNS, mais je n'ai jamais expérimenté.

Par défaut votre IP v4 chez Free est partagé avec 4 clients. L'opérateur réserve simplement une plage de ports différente. Cela permet de pallier (sans doute provisoirement) à la pénurie d'IP v4 que nous rencontrons actuellement. Pour 100000 clients, Free n'a plus besoin de 100000 IPs v4, mais de 25000. Cela convient parfaitement pour un usage traditionnel. Mais pour notre serveur, il faut demander une adresse IP fixe personnelle.

Il est fort probable que nous soyons obligé un jour de basculer complétement vers de l'IP v6. Il est déjà possible de le faire si vos machines le supportent.

Pour le moment nous resterons sur de l'IP v4. Il faut vérifier dans un premier temps que l'attribution d'une adresse IP fixe est possible depuis le compte client : **Ma Freebox > Demander une adresse IP fixe V4 full-stack**.

![Free Adresse IP fixe V4 full-stack]({{ url }}media/blog/articles/freebox-ipv4-fullstack.png)

Si vous n'avez pas l'option, il sera un peu plus compliqué d'accéder à distance à vos applications.

Je recommande donc fortement une connexion fibrée chez Free...

Niveau temps de réponse, c'est très bon, même excellent. Mieux que chez beaucoup d'hébergeurs.

![TTBF Freebox vs Netlify]({{ url }}media/blog/articles/freebox-fibre-vs-netlify.png)

<aside>Freebox FTTH vs Netlify</aside>

Ce graphique met en évidence le temps de latence pour des requêtes vers une **Freebox FTTH** (à gauche), puis **Netlify** (à droite). Les sondes sont situées à Roubaix et Londres. Chez Netlify c'est beaucoup plus cahotique.

### Quelle machine ? {: #p4 }

C'est un vaste sujet... Cela dépend de ce que l'on souhaite héberger sur le serveur. Dans le passé, j'ai toujours eu tendance à prendre des machines surdimensionnées par rapport à l'usage que j'en avais. *"On ne sait jamais, ça peut servir"*. C'est une erreur. De l'argent dépensé inutilement.

Il y a 4 critères à prendre en compte :

- Les applications web que l'on souhaite utiliser (Wordpress, Magento, site statique...)
- Le trafic estimé
- La consommation électrique nécessaire au fonctionnement de la machine
- La place dont vous disposez à proximité de la box

La bonne nouvelle est que de manière générale une machine peu puissante suffi. Un simple Raspberry Pi avec Nginx sert parfaitement un site statique.

Il faut simplement adapter en fonction des recommandations communiquées par les éditeurs. Anticiper si possible le nombre de connexions simultanées.

Si c'est une machine recyclée qui n'avait plus d'utilité, c'est encore mieux.

Ici j'ai souhaité une machine peu encombrante, presque invisible. Cette machine doit remplacer le serveur que j'utilise depuis 3 ans et pour lequel j'ai d'autres projets. La box est située dans l'entrée de la maison, je n'ai pas envie d'y mettre une tour. J'attache également beaucoup d'importance à la consommation électrique, la machine est allumée non stop. Pour finir, je ne souhaite héberger que des sites statiques (jekylls, Hugo...), avec un trafic très faible.

Je suis un lecteur du site [minimachines.net](https://www.minimachines.net). Au moment de mes recherches [Pierre Lecourt](https://twitter.com/PierreLecourt) publiait une offre pour un nouveau mini PC fanless, le [Mele Quieter2](https://www.minimachines.net/actu/mele-quieter2-98885). C'est ce genre de machine qu'il me fallait. Cerise sur le gâteau, le PC est insensible à la poussière.

Mais sur un PC d'une marque chinoise peu connue on ne sait jamais très bien comment une distribution Linux va tourner. C'est un risque modéré car il n'y a généralement rien d'extravagant. Il faut surtout s'inquiéter de la finition générale de l'engin. Il m'est arrivé de me retrouver avec des machines au bruit insupportable ou avec des connecteurs défectueux. Toujours attendre un peu, n'acheter que s'il y a plusieurs retours positifs.

Pour cet article, l'installation a donc été effectuée sur le Mele Quieter2. Il a également l'avantage de consommer **moins de 1.5w** quand il ne se passe rien (sans disque supplémentaire). Cela représente quelques centimes par mois.

Comparatif de la consommation de 3 mini-machines (aucune activité) :

![Consommation électrique]({{ url }}media/blog/articles/consommation-electrique.png)

| Machine                              | OS              | Conso.   |
| ------------------------------------ | --------------- | -------- |
| Raspberry Pi 4 (*Standard*)          | Raspberry Pi OS | **2.5w** |
| ASUS PN60 (*SSD 256Go - 32Go ram*)   | Debian          | **8.5w** |
| Mele Quieter2 (*Standard*)           | Debian          | **1.2w** |

Le **Mele Quieter2** est monté au maximum à **5.1w** avec **283 requêtes HTTP par seconde** sur un site statique.

Héberger un site sur un Mele Quieter2 coûte moins de 2€ par an.

**Note :** ce sont ici des mini-machines avec des composants à très faible consommation. Si vous utilisez une vielle tour qui traîne dans un coin, on pourrait facilement se situer aux alentours des 100w. Il existe de nombreux sites pour estimer la consommation d'un PC, par exemple [Power Supply Calculator](https://outervision.com/power-supply-calculator).
{: .warning }

### Image d'installation {: #p5 }

Pour le système d'exploitation c'est au choix, pour du serveur on peut par exemple trouver :

- Debian
- RHEL
- Ubuntu server
- FreeBSD

Il en existe beaucoup d'autres. J'en ai essayé pas mal, mais j'ai une nette préférence pour Debian. J'y reviens toujours. C'est très personnel.

**J'effectue dans cet article une installation Debian**, mais vous pouvez adapter sans problème selon votre OS préféré.

Je réalise l'installation de l'OS à partir d'une clé USB bootable. On peut utiliser n'importe quelle clé, avec une capacité suffisante pour accueillir l'image d'installation. J'ai une petite clé **SanDisk de 16Go**, ça coûte moins de 10€.

Les systèmes fournissent des images de type **img** ou **iso**. Pour Debian on la télécharge via le lien suivant :

[Télécharger les images de CD de Debian par HTTP ou par FTP](https://www.debian.org/CD/http-ftp/#stable)

Le téléchargement d'une image requiert de connaître le type de processeur. Dans la majorité des cas votre CPU est de type amd64. Pour faire simple, si la machine a moins 20 ans et peut faire tourner Windows c'est de l'amd64. Les choses vont peut-être changer dans le futur avec l'arrivée d'Apple M1 et du Lakefield chez Intel (ARM). Pour un Raspberry Pi 4 c'est de l'arm64, mais Raspberry Pi OS est basé sur Debian, il est préférable d'utiliser cet OS.

Si vous avez la possibilité de relier le PC à la box en ethernet pendant l'installation, partez sur l'image **debian-X.X.X-amd64-netinst.iso**, sinon **debian-X.X.X-amd64-xfce-CD-1.iso**. Il est fréquent que la configuration du wifi requiert des drivers spécifiques, toujours un peu galère pendant la phase d'installation.

De mon côté j'ai la chance d'avoir un D-Link DAP-1360 (environ 30€) configuré en mode Wireless (le bureau est loin de la box), j'y branche simplement la machine en ethernet.

![Dlink DAP 1360]({{ url }}media/blog/articles/dlink-dap-1360.png)

Mais vous pouvez sans problème effectuer l'installation sans Internet à partir de l'image CD complète (**debian-X.X.X-amd64-xfce-CD-1.iso**).

### Préparer une clé USB bootable {: #p6 }

Pour créer une clé USB bootable à partir de l'image téléchargée, 2 solutions.

#### Depuis Windows

<section markdown="1">
Si vous êtes sous Windows, le logiciel [Rufus](https://rufus.ie/fr/) est parfait.

![Logiciel Rufus]({{ url }}media/blog/articles/rufus.png)

Il y a quelques options à paramétrer :

- **Périphérique :** la clé USB
- **Type de démarrage :** l'image d'installation précédemment téléchargée
- **Schéma de partition :** GPT *
- **Système de destination :** UEFI
- **Système de fichiers :** FAT32
- **Taille d’unité d’allocation :** Défaut

\* Je pars du principe que le futur serveur est une machine assez récente (après 2012) avec **firmeware UEFI** et disque avec **partition GPT**. Si vous doutez, il faut visualiser le **setup** de la carte mère. Au démarrage (splash screen) actionnez la touche d'accès au setup (<kbd>Esc</kbd>, <kbd>Suppr</kbd>, <kbd>F2</kbd>, <kbd>F10</kbd>...), généralement la touche est indiquée. Si vous êtes sur de l'UEFI cela est obligatoirement mentionné quelque part.

![Bios Legacy ou UEFI]({{ url }}media/blog/articles/bios-uefi.png)

<aside>UEFI du Asus PN60 (sur de nombreuses cartes mères Asus) et du Mele Quieter2 (Aptio setup utility, un classique)</aside>

Il peut arriver que le boot soit en mode BIOS Legacy. Revenez sur de l'UEFI si cela est le cas (même si le disque est en MBR il sera formaté intégralement).

Après validation, il est possible que Rufus vous demande le mode d'écriture de l'image. Restez sur l'option recommandée (Ecrire en mode image ISO).

![Rufus mode d'écriture de l'image]({{ url }}media/blog/articles/rufus-isohybrid.png)
</section>

#### Depuis un système UNIX

<section markdown="1">
Si vous êtes sous un système UNIX (Ubuntu, Debian, MacOS...), on peut passer par la commande `dd`.

Il faut dans un premier temps identifier le fichier périphérique sur lequel la clé est accessible. J'utilise la commande `dmesg` juste après avoir branché la clé USB.

```bash
sudo dmesg
```

```
[1129003.393918] usb-storage 2-4.3:1.0: USB Mass Storage device detected
[1129003.394285] scsi host1: usb-storage 2-4.3:1.0
[1129004.398960] scsi 1:0:0:0: Direct-Access     SanDisk  Ultra            1.00 PQ: 0 ANSI: 6
[1129004.399389] sd 1:0:0:0: Attached scsi generic sg0 type 0
[1129004.399661] sd 1:0:0:0: [sda] 30464000 512-byte logical blocks: (15.6 GB/14.5 GiB)
[1129004.400584] sd 1:0:0:0: [sda] Write Protect is off
[1129004.400588] sd 1:0:0:0: [sda] Mode Sense: 43 00 00 00
[1129004.400897] sd 1:0:0:0: [sda] Write cache: disabled, read cache: enabled, doesn't support DPO or FUA
[1129004.422517] sda: sda1
[1129004.423849] sd 1:0:0:0: [sda] Attached SCSI removable disk
```

On identifie ici clairement que nous sommes sur `/dev/sda` (ce peut être **sdb**, **sdc**... ou autre), avec une partition (sda1). Ce que l'on peut vérifier avec la commande `df`.

```bash
sudo df
```

```
/dev/sda1    15G    8,0K   15G   1% /media/xxxxxxx/name
```

Ou encore la commande `lsblk`.

```bash
sudo lsblk
```

```
NAME        MAJ:MIN RM   SIZE RO TYPE MOUNTPOINT
sda           8:0    0  14,5G   0 disk
└─ sda1       8:1    0  14,5G   0 part /media/xxxxxxx/name
```

**Note :** si c'est une clé toute neuve ou complétement formatée il n'y a pas forcement de partition (sdaX).

**Pour la suite n'oubliez pas de remplacer le fichier périphérique par celui identifié sur votre système (sda, sdb, sdc...) au risque de perdre toutes les informations contenues sur un disque.**
{: .alert }

Il nous reste, à l'aide de la commande `dd`, à copier l'image sur la clé USB. **Ne pas oublier de démonter la clé au préalable.**

```bash
sudo umount /dev/sda1
```

<aside>Si la partition est montée sur sda1</aside>

```bash
sudo umount /dev/sda
```

<aside>Si la clé USB est montée sur sda</aside>

```bash
sudo dd if=debian-X.X.X-amd64-netinst.iso of=/dev/sda bs=1M
```

<aside>Avec l'image <strong>Debian network install</strong> si la machine dispose d'une connexion Internet</aside>

```bash
sudo dd if=debian-X.X.X-amd64-xfce-CD-1.iso of=/dev/sda bs=1M
```

<aside>Avec l'image <strong>Debian CD</strong> si la machine ne peut être connectée à Internet</aside>

Si tout va bien on obtient après quelques secondes :

```bash
337+0 enregistrements lus
337+0 enregistrements écrits
353370112 bytes (353 MB, 337 MiB) copied, 29,0891 s, 12,1 MB/s
```
</section>

**La clé USB est prête**, on la branche sur le futur serveur.

### Installation du système d'exploitation {: #p7 }

Au démarrage du système, au splash screen, on active rapidement la touche pour l'accès au setup. La touche diffère selon les constructeurs : <kbd>Esc</kbd>, <kbd>Suppr</kbd>, <kbd>F2</kbd>, <kbd>F10</kbd>... En général la touche est indiquée. Pour le **Mele Quieter2** c'est <kbd>Suppr</kbd>.

Une fois sur le **BIOS/UEFI**, on se dirige vers la section `boot`, ou parfois `démarrage` en Français.

![UEFI Aptio Boot]({{ url }}media/blog/articles/uefi-aptio-boot.png)

L'obectif et d'amorcer le démarrage sur la **clé USB** et non sur les autres disques, en lui accordant la priorité. On enregistre et on redémarre.

Le système démarre sur la clé USB et si tout a bien fonctionné, l'écran d'installation du système d'exploitation est affiché.

![Installation du système d'exploitation Debian]({{ url }}media/blog/articles/debian-install-screen.png)

J'effectue l'installation de **Debian**, si vous optez pour un autre système c'est généralement assez similaire.

Par habitude je préfère l'installation classique (Install), je n'utilise jamais l'installation graphique. Mais les étapes sont exactement les mêmes.

<section markdown="1">
- **Language :** French - Français
- **Pays :** France
- **Disposition du clavier :** Français
- **Wifi (optionnel) :** si le réseau n'est pas accessible, Debian tente une connexion wifi qui échoue la plupart du temps en raison des drivers manquants. Passez cette étape puis sélectionnez "Ne pas configurer le réseau maintenant"
- **Nom de la machine :** indiquez ce que vous souhaitez, de préférence un nom qui n'existe pas déjà sur le réseau, ce sera plus simple de l'identifier par la suite
- **Mot de passe root :** mot de passe souhaité
- **Nom complet du nouvel utilisateur :** votre identifiant
- **Forcer l'installation UEFI (optionnel) :** Debian peut détecter un système installé en mode de compatibilité BIOS. On force alors l'UEFI.
- **Partitionner les disques :** sauf pour des cas très particuliers, vous pouvez choisir "Utiliser un disque entier", puis "tous dans une seule partition (recommandé pour les débutants)". On applique enfin les changements sur les disques.

L'installation du système de base commence. Il reste à configurer l'outil de gestion des paquets (sans miroir sur le réseau si vous êtes offline), et enfin la **sélection des logiciels**.

A cette étape **ne sélectionnez que 2 options** :

```
[ ] environnement de bureau Debian
[ ] serveur web
[ ] serveur d'impression
[*] serveur SSH
[*] utilitaires usuels du système
```

- **Serveur SSH** car la connexion au serveur se fera à distance. Une fois l'installation et la configuration terminées on branche la machine sur la box et elle n'en bougera plus.
- **Utilitaires usuels du système** comprend une série d'applications pour gérer le système d'exploitation.

Je ne sélectionne jamais **serveur web**, je préfère une installation manuelle par la suite.
</section>

Le système est installé, on redémarre.

### Configuration du système {: #p8 }

#### Editeur de texte

Pour éditer les fichiers de configuration, utilisez un éditeur que vous appréciez. Par défaut nous n'avons que `vi`. Cela convient aux puristes mais `nano` facilite grandement la tâche.

Si vous êtes en mode offline, utilisez `vi` à l'étape suivante (Adresse IP), vous pourrez installer autre chose par la suite.

```bash
apt-get update
apt-get install nano
```

#### Adresse IP

Nous devons attribuer à la machine une adresse IP fixe en dehors de la plage d'adresses IP réservées par la box pour le DHCP.

Contrôlez cette plage d'adresses dans la configuration de la freebox en vous connectant depuis le navigateur sur [http://mafreebox.freebox.fr](http://mafreebox.freebox.fr).

Dans le menu **Paramètres de la freebox > Réseau local > DHCP**, on visualise le début et la fin de la plage d'adresses :

![Freebox configuration du DHCP]({{ url }}media/blog/articles/freebox-dhcp.png)

Le DHCP est configuré ici pour attribuer des adresses entre **192.168.1.2** et **192.168.1.50**.

Il est également possible dans la configuration de la freebox d'attribuer un bail DHCP statique selon l'adresse mac de la machine, mais par expérience évitez d'utiliser ce système.
{: .warning }

Sur le serveur, connectez vous au compte **root** via la commande `su`, puis éditez le fichier `/etc/network/interfaces`.

```bash
su
nano /etc/network/interfaces
```

Nous devrions trouver **dhcp** pour l'interface réseau. Par exemple :

```bash
iface enp2s0 inet dhcp
```

<aside>L'interface est ici enp2s0, diffère selon les systèmes</aside>

On remplace avec une IP fixe en dehors de la plage d'adresses DHCP de la box. J'ai choisi **192.168.1.60**.

```
# This file describes the network interfaces available on your system
# and how to activate them. For more information, see interfaces(5).

source /etc/network/interfaces.d/*

# The loopback network interface
auto lo
iface lo inet loopback

# The primary network interface
auto enp2s0
allow-hotplug enp2s0
iface enp2s0 inet static
    address 192.168.1.60
    netmask 255.255.255.0
    gateway 192.168.1.254
    broadcast 192.168.1.255
```

<aside>/etc/network/interfaces</aside>

On peut redémarrer :

```bash
/etc/init.d/networking restart
```

On vérifie que l'adresse IP a bien été attribuée avec la commande `ip a` :

```bash
ip a
```

**Nous pouvons maintenant relier définitivement la machine à la box (sans écran ni clavier) et utiliser n'importe quel PC pour s'y connecter à distance.**

Petite vérification au préalable :

```bash
systemctl status ssh
```

Nous avions installer le serveur SSH lors du choix des logiciels à l'installation de Debian. Si vous avez omis cette étape il faut l'installer maintenant : `apt-get install openssh-server`.

Par défaut le serveur SSH n'accepte pas de connexion directe au compte **root**. C'est une configuration que l'on peut modifier en éditant le fichier `/etc/ssh/sshd_config` (**PermitRootLogin**). Mais si vous souhaitez autoriser les connexions SSH depuis l'extérieur je le déconseille fortement. Pensez également dans ce cas à modifier le port de connexion par défaut (22).

Une fois la machine connectée en ethernet à la box, utilisez d'importe quelle machine avec un client ssh pour vous y connecter. Depuis windows 10 vous pouvez utiliser directement la commande `ssh` dans le **command prompt**. Pour les versions antérieures vous pouvez passer par [putty](https://www.putty.org/). Pour les systèmes UNIX c'est la commande `ssh`.

```bash
ssh username@192.168.1.60
```

### Installation du serveur Web {: #p9 }

Apache, Nginx, Node.js... On y met ce que l'on souhaite. Pour mes sites statiques je vais rester sur un traditionnel Apache.

Pour cet article je ne vais pas plus loin, je reste sur l'hébergement d'un site statique. Je n'installe aucun langage (PHP, Python, Java, Ruby...) ni serveur de base de données.

Une fois connecté au serveur via ssh, on installe Apache :

```bash
apt-get install apache2
```

Les commandes de type **a2enmod**, **a2enconf**, **a2enmod**... sont propres à Debian (et donc tous les systèmes basés sur Debian comme Ubuntu). Les opérations que j'effectue via ces commandes sont à réaliser manuellement si vous avez opté pour un système tel que FreeBSD. Le paquet Apache sur les systèmes Debian propose un panel d'outils et une façon particulière de gérer les configurations.
{: .warning }

On active de suite les module classiques :

```bash
a2enmod ssl
a2enmod rewrite
a2enmod expires
a2enmod headers
a2enmod http2
```

```bash
service apache2 restart
```

On peut enfin vérifier qu'Apache communique bien sur les ports 80 et 443 :

```bash
lsof -i -P -n | grep LISTEN
```

A ce stade, depuis n'importe quel PC ou smartphone connecté au réseau, on accéde au serveur depuis le navigateur à l'adresse `http://192.168.1.60` (adaptez selon l'IP que vous avez choisi).

![Page Apache par défaut]({{ url }}media/blog/articles/apache-it-works.png)

J'ajoute une configuration custom pour sécuriser un peu mes applications et activer HTTP/2. A adapter selon vos besoins.

```bash
nano /etc/apache2/conf-available/custom.conf
```

```apache
Timeout 60
FileETag None
ServerTokens Prod
ServerSignature Off
TraceEnable Off

AddDefaultCharset utf-8

<Directory /var/www>
    Options -Indexes
    <LimitExcept GET POST HEAD>
        Require all denied
    </LimitExcept>
</Directory>

<IfModule mod_headers.c>
    Header set Content-Security-Policy "default-src 'self'; style-src 'self' 'unsafe-inline'; base-uri 'self';"
    Header set X-XSS-Protection "1; mode=block"
    Header set X-Content-Type-Options: "nosniff"
    Header set X-Frame-Options: "sameorigin"
</IfModule>

<IfModule mod_ssl.c>
    Protocols h2 http/1.1
</IfModule>
```

<aside>/etc/apache2/conf-available/custom.conf</aside>

```bash
a2enconf custom
service apache2 restart
```

Pour aller plus loin dans la sécuristation d'Apache, je recommande le [guide de renforcement et de sécurité du serveur Web Apache](https://geekflare.com/fr/apache-web-server-hardening-security/) sur geekflare.

Pour la configuration du CSP (Content-Security-Policy), consultez l'article [Utiliser une stratégie de sécurité du contenu (Content Security Policy)]({{ url }}blog/strategie-de-securite-du-contenu-content-security-policy.html)

### Redirection des ports 80 et 443 {: #p10 }

Lorsque qu'un client effectue une requête HTTP sur l'IP assignée par Free, le routeur de la freebox doit être en mesure de rediriger les ports 80 et 443 (SSL) vers le serveur.

Ouvrez la configuration de la freebox depuis le navigateur ([http://mafreebox.freebox.fr](http://mafreebox.freebox.fr)). Accédez ensuite au menu *Paramètres de la freebox > Gestion des ports*.

![Gestion des ports sur la freebox Delta]({{ url }}media/blog/articles/freebox-gestion-des-ports.png)

Ajoutez 2 redirections pour les ports 80 et 443 vers l'IP de votre serveur.

![Freebox redirection du port 80]({{ url }}media/blog/articles/freebox-redirection-port.png)

#### Port 80

- **Ip Destination :** 192.168.1.60 (adaptez selon l'IP que vous avez choisi)
- **Redirection active :** ✓
- **IP source :** Toutes (ou une adresse IP spécifique)
- **Protocole :** TCP
- **Port de début :** 80
- **Port de fin :** 80
- **Port de destination :** 80
- **Commentaire :** Server Web

#### Port 443

- **Ip Destination :** 192.168.1.60 (adaptez selon l'IP que vous avez choisi)
- **Redirection active :** ✓
- **IP source :** Toutes (ou une adresse IP spécifique)
- **Protocole :** TCP
- **Port de début :** 443
- **Port de fin :** 443
- **Port de destination :** 443
- **Commentaire :** Server Web Secure

Cette configuration ne nécessite pas le redémarrage de la box.

**Le serveur est maintenant accessible depuis l'extérieur avec l'IP assignée par free.** Testez la configuration en indiquant l'IP dans le navigateur de votre téléphone depuis une connexion 4G.

### Configuration du vhost {: #p11 }

Je considère que le nom de domaine est `example.com`.

Ajoutons dans un premier temps une page à la racine du futur site `/var/www/example` :

```bash
mkdir /var/www/example
echo "Hello World!" > /var/www/example/index.html
```

On indique un nouvel host dans `/etc/hosts` :

```
127.0.0.1       localhost
127.0.1.1       machine

127.0.0.1       example.com

::1     localhost ip6-localhost ip6-loopback
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
```

<aside>/etc/hosts</aside>

On ajoute ensuite le fichier vhost Apache dans `/etc/apache2/sites-available`. Je nomme le fichier `example.com.conf`.

```apache
<VirtualHost *:80>
    ServerAdmin webmaster@localhost

    DocumentRoot /var/www/example
    ServerName example.com

    <Directory /var/www/example>
        Options Indexes FollowSymLinks MultiViews
        AllowOverride All
        Require all granted
    </Directory>

    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined

    LogLevel warn
</VirtualHost>
```

<aside>/etc/apache2/sites-available/example.com.conf</aside>

Pour finir on active la configuration :

```bash
a2ensite example.com
service apache2 restart
```

### Enregistrement DNS {: #p12 }

Chez le registrar depuis lequel votre domaine est géré (OVH, Ionos, Gandi, GoDaddy, Google domains...), nous allons modifier l'IP pour l'enregistrement DNS de type A (enregistrement d'hôte).

L'accès à la zone DNS du domaine diffère selon les bureaux d'enregistrement. Vous la trouverez certainement en sélectionnant votre nom de domaine, puis sur une action du type *"Modifier la zone DNS"*.

![Zone DNS chez Ionos]({{ url }}media/blog/articles/dns-ionos.png)

<aside>Exemple de configuration de zone DNS chez Ionos</aside>

Les enregistrements qui nous intéressent sont ceux de **type A** (vous trouverez certainement des enregistrements de type AAAA dédiés à l'IPv6 et MX pour le serveur de messagerie).

Il y a autant d'enregistrements de type A qu'il existe de sous domaine. Le nom d'hôte **www** est un sous domaine.

Dans la majorité des cas, on ajoute un enregistrement pour le domaine principal (`example.com`) et le sous domaine www (`www.example.com`). C'est ensuite le serveur (Apache dans notre cas) qui se charge de rediriger l'un vers l'autre selon l'adresse que vous souhaitez exploiter).

L'utilisation du sous domaine **www** est historique. C'est un moyen de faire comprendre immédiatement qu'il s'agit d'un site, si par exemple le domaine apparaît sur une affiche ou une carte de visite. Un domaine peut être utilisé pour une multitude de service. Je recommande généralement l'utilisation du sous domaine **www** avec une redirection du domaine principal (example.com vers www.example.com).
{: .warning }

Pour les hôtes **@** et **www**, modifiez ou ajoutez l'enregistrement de **type A** avec votre IP publique Free. La modification peut prendre plusieurs heures (propagation DNS).

Nous y sommes ! En indiquant l'adresse `http://example.com` nous visualisons notre site !

![Site Internet dans le navigateur]({{ url }}media/blog/articles/site.png)

Si vous souhaitez utiliser `www.example.com` avec redirection de `example.com`, je vous conseille d'ajouter 2 fichiers de configuration vhost :

```apache
# example.com.conf

<VirtualHost *:80>
    ServerName example.com
    Redirect permanent / http://www.example.com
</VirtualHost>
```

<aside>/etc/apache2/sites-available/example.com.conf</aside>

```apache
# www.example.com.conf

<VirtualHost *:80>
    ServerAdmin webmaster@localhost

    DocumentRoot /var/www/example
    ServerName www.example.com

    <Directory /var/www/example>
        Options Indexes FollowSymLinks MultiViews
        AllowOverride All
        Require all granted
    </Directory>

    ErrorLog ${APACHE_LOG_DIR}/error.example.com.log
    CustomLog ${APACHE_LOG_DIR}/access.example.com.log combined

    LogLevel warn
</VirtualHost>
```

<aside>/etc/apache2/sites-available/www.example.com.conf</aside>

### Certificat SSL Let's Encrypt {: #p13 }

Notre site n'est actuellement pas sécurisé. C'est aujourd'hui indispensable.

La génération d'un certificat SSL Let's Encrypt s'effectue très simplement avec **certbot**.

```bash
apt-get install certbot python-certbot-apache
```

La commande `certbot` vous propose l'activation de HTTPS pour les adresses de votre choix :

```bash
certbot

Which names would you like to activate HTTPS for?
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
1: example.com
2: www.example.com
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Select the appropriate numbers separated by commas and/or spaces, or leave input
blank to select all options shown (Enter 'c' to cancel): 1,2
```

La deuxième étape consiste à forcer ou non la redirection de **http** vers **https**. Je vous conseille fortement de l'activer (option 2).

```bash
Please choose whether or not to redirect HTTP traffic to HTTPS, removing HTTP access.
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
1: No redirect - Make no further changes to the webserver configuration.
2: Redirect - Make all requests redirect to secure HTTPS access. Choose this for
new sites, or if you're confident your site works on HTTPS. You can undo this
change by editing your web server's configuration.
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Select the appropriate number [1-2] then [enter] (press 'c' to cancel): 2
```

Certbot se charge automatiquement de l'ajout des vhosts pour le port 443 avec configuration du certificat. Une fois la commande exécutée vous trouverez les nouvelles configurations :

```
-rw-r--r-- 1 root root 659 mai   27 17:01 example.com.conf
-rw-r--r-- 1 root root 847 mai   27 17:17 example.com-le-ssl.conf
-rw-r--r-- 1 root root 268 mai   27 17:02 www.example.com.conf
-rw-r--r-- 1 root root 385 mai   27 17:17 www.example.com-le-ssl.conf
```

<aside>/etc/apache2/sites-available</aside>

Le site est maintenant accessible à l'adresse `https://example.com` (ou `https://www.example.com`).

![Site Internet sécurisé dans le navigateur]({{ url }}media/blog/articles/site-secure.png)

[Sommaire](#p0)
{: .toolbar }