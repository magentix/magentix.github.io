1. [Taille du disque](<#p1>)
2. [Taille des répertoires](<#p2>)
3. [Journaux](<#p3>)
4. [Fichiers des paquets](<#p4>)
5. [Thumbnails](<#p5>)
6. [Fichiers de sauvegarde](<#p6>)
7. [Logs](<#p7>)
8. [Composer](<#p8>)
9. [Flush quotidien avec anacron](<#p9>)

### Taille du disque {: #p1}

Un premier contrôle rapide de la place restante sur les disques s'effectue par la commande `df` (disk free) :

```bash
df -h
```

On identifie assez rapidement la place utilisée sur les disques, par exemple ici sur un SSD :

```
Sys. de fichiers               Taille Utilisé Dispo Uti% Monté sur
/dev/nvme0n1p2                   938G     84G  807G  10% /
```

### Taille des répertoires {: #p2}

La commande `du` est très pratique pour contrôler la taille des dossiers.

On utilise l'option `h` pour obtenir des tailles plus lisibles, et l'option `s` pour ne pas afficher le détail des fichiers et sous dossiers.

Quelques exemples sur des répertoires souvent très volumineux :

```bash
sudo du -sh /var/log
```

```bash
sudo du -sh /tmp
```

```bash
sudo du -sh ~/.cache/*/
```

Pour contrôler la taille des sous-dossiers du dossier courant :

```bash
sudo du -sh ./*/
```

### Journaux {: #p3}

L'affichage de la taille des journaux du système s'effectue par le biais de la commande suivante :

```bash
journalctl --disk-usage
```

Les logs sont stockés sous forme de fichiers persistants dans le dossier **var/log/journal** s'il existe. Les journaux ont souvent tendance à se remplir très rapidement.

Pour nettoyer ces journaux :

```bash
journalctl --vacuum-time=1d > /dev/null 2>&1
```

Dans cet exemple on supprime tous les logs de plus de 24 heures.

### Fichiers des paquets {: #p4}

Un nettoyage des fichiers temporaires et des fichiers d'installation peut s'effectuer rapidement.

Supprimer le cache des paquets périmés :

```bash
sudo apt-get autoclean
```

Supprimer tout le cache :

```bash
sudo apt-get clean
```

Supprimer les paquets installés comme dépendances et devenus inutiles :

```bash
sudo apt-get autoremove
```

### Thumbnails {: #p5}

Les miniatures des images de l'interface sont stockées dans les dossiers **~/.thumbnails**, **~/.cache/thumbnails**.

Pour nettoyer les images, on supprime sans crainte les miniatures générées depuis plus de 7 jours :

```bash
find ~/.thumbnails -type f -ctime +7 -delete
```

```bash
find ~/.cache/thumbnails -type f -ctime +7 -delete
```

### Fichiers de sauvegarde {: #p6}

Les fichiers avec un **~** à la fin de leur nom sont des copies de sauvegarde créées automatiquement pour les documents ouverts par certaines applications (gedit, LibreOffice...). On peut les supprimer sans problème.

```bash
find ~/ -name '*~' -exec rm {} \;
```

### Logs {: #p7}

Les logs sont stockées dans le dossier **/var/log**. Le **logrotate** par défaut (apache, php, dpkg...) est souvent important (12 mois) et il fastidieux de les modifier manuellement.

Sauf dans des cas bien spécifiques, il est très rare d'aller fouiller dans des archives de log de plusieurs mois.

La façon la plus radicale et efficace de nettoyer ces logs est de supprimer toutes les archives :

```bash
sudo find /var/log/ -type f -regex '.*\.[0-9]+\.gz$' -delete
```

### Composer {: #p8}

Si vous développez et utilisez quotidiennement **composer**, pensez à supprimer son cache de temps en temps.

Le cache de **composer** peut grossir rapidement, pour s'en rendre compte :

```bash
sudo du -sh ~/.cache/composer
```

```bash
sudo du -sh ~/.composer/cache
```

Pour supprimer le cache :

```bash
composer clearcache
```

```bash
rm -rf ~/.cache/composer
```

```bash
rm -rf ~/.composer/cache
```

### Flush quotidien avec anacron {: #p9}

J'ai pour habitude d'effectuer quotidiennement des nettoyages des fichiers et dossiers les plus volumineux via **anacron**. Cela permet d'éviter un encombrement inutile.

```bash
nano /etc/anacrontab
```

```
1       10      log.flush       find /var/log/ -type f -regex '.*\.[0-9]+\.gz$' -delete
1       20      journal.flush   journalctl --vacuum-time=1d > /dev/null 2>&1
1       30      thumb.flush     find ~/.thumbnails -type f -ctime +7 -delete
```