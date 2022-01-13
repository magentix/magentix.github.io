Pour le profiling rapide d'un projet, **XHProf** est une excellente extension. Elle permet en quelques secondes de détecter les fuites de mémoire, avec un impact sur les temps d'exécution de l'application extrêmement faible.

Cet article explique comment implémenter **XHProf** pour votre application PHP.

![Xhprof Callgraph]({{ url }}media/blog/articles/xhprof-graph.png){: width="1000" height="200" }

### Installer l'extension PHP

Nous installons l'extension pour PHP 7 maintenue par **Tideways**.

```bash
git clone "https://github.com/tideways/php-xhprof-extension.git"
cd php-xhprof-extension
phpize
./configure
make
sudo make install
```

On active ensuite l'extension, à adapter selon la version de PHP en place (ici php 7.2).

```bash
echo "extension=tideways_xhprof.so" | sudo tee -a /etc/php/7.2/mods-available/xhprof.ini
```

PHP standard :

```bash
sudo phpenmod -v 7.2 xhprof
sudo service apache2 restart
```

PHP FPM :

```bash
sudo phpenmod -v 7.2 -s fpm xhprof
sudo service php7.2-fpm restart
sudo service apache2 restart
```

### Installer une interface web

Le rapport fournit par **XHProf** doit être analysé via une interface web. Cette interface permet la navigation dans l'arbre et la génération de graphs.

```bash
sudo mkdir /var/www/xhprof
cd /var/www/hxprof
git clone https://github.com/sters/xhprof-html .
```

```bash
sudo nano /etc/hosts
```

On ajoute au fichier une nouvelle entrée :

```
127.0.0.1 localhost.xhprof
```

On génère ensuite un nouveau vhost :

```bash
sudo nano /etc/apache2/sites-available/xhprof.conf
```

On utilise la configuration basique suivante :

```apache
<VirtualHost *:80>
    ServerAdmin webmaster@localhost

    DocumentRoot /var/www/xhprof
    ServerName localhost.xhprof

    <Directory /var/www/xhprof>
        Options Indexes FollowSymLinks MultiViews
        AllowOverride All
        Order allow,deny
        allow from all
    </Directory>
</VirtualHost>
```

Il ne reste plus qu'à activer le site :

```bash
sudo a2ensite xhprof.conf
sudo service apache2 restart
```

Depuis le navigateur, accédez à l'URL *http://localhost.xhprof/?dir=/tmp*. Le paramètre **dir** dans l'URL indique que les runs sont stockés dans le dossier **/tmp** de la machine (à adapter si besoin). Vous obtenez le message suivant :

```
No XHProf runs specified in the URL.
Existing runs:
```

### Installation de GraphViz

**GraphViz** est la solution retenue pour la génération des graphiques (callgraphs). C'est un ensemble d'outils OpenSource dédiés à la génération de graphs. Ils seront générés via l'interface Web.

```bash
sudo apt-get install graphviz
```

### Profiler une application PHP

Pour exécuter un run **XHProf**, il faut simplement ajouter dans le code de l'application les lignes suivantes :

```php
tideways_xhprof_enable();

// Code à profiler

$data = tideways_xhprof_disable();
$namespace = 'myapp';
file_put_contents(
    sys_get_temp_dir() . "/" . uniqid() . "." . $namespace . ".xhprof", // /tmp/xxxxxxxxxxxxx.myapp.xhprof
    serialize($data)
);
```

Pour profiler entièrement l'application, on place généralement ces lignes dans le fichier **index.php**.

Le fichier généré dans **tmp** est de la forme **xxxxxxxxxxxxx.myapp.xhprof**. Ce fichier contient l'ensemble des données enregistrées par **XHProf**. Il peut maintenant être analysé via l'interface Web.

### Analyse des résultats

En ouvrant de nouveau *http://localhost.xhprof/?dir=/tmp*, vous disposez maintenant du run :

![Xhprof Runs]({{ url }}media/blog/articles/xhprof-runs.png){: width="439" height="104" }

Sélectionnez le run correspondant, l'analyse peut alors débuter...