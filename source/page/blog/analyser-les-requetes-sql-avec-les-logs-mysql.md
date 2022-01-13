Sur votre environnement de développement, il est très facile d'activer les logs MySQL. C'est le moyen le plus simple d'obtenir pour une page l'ensemble des requêtes exécutées.

Les logs fournissent la requête exacte et le type de commande (Connect, Prepare, Execute, Query, Close stmt, Quit...). L'analyse de ces logs peut permettre d'alléger le nombre de requête pour une page en les factorisant par exemple.

![Mysql General Log]({{ url }}media/blog/articles/mysql-general-log.png){: width="1000" height="166" }

### Activer les logs

Par le biais d'un utilisateur qui en possède les droits, on active les logs de type TABLE :

```mysql
USE mysql;

SET GLOBAL log_output = 'TABLE';

TRUNCATE general_log;

SET GLOBAL general_log = 'ON';
```

### Consulter une page

Depuis n'importe quel navigateur, consulter la page que vous souhaitez analyser. Ne consultez qu'une seule page préalablement sélectionnée.

### Consulter les logs

```mysql
SET GLOBAL general_log = 'OFF';

SELECT COUNT(*) FROM general_log;

SELECT event_time, user_host, thread_id, server_id, command_type, CONVERT(argument USING utf8) FROM general_log;
```

### Réinitialiser les logs

Avant chaque analyse, il est important de ne pas oublier de vider la table des logs, au risque d'enregistrer les requêtes de plusieurs pages.

```mysql
TRUNCATE general_log;

SET GLOBAL general_log = 'ON';
```

### Exporter les logs

#### Depuis une requête SQL

Uniquement si votre utilisateur dispose du droit **FILE** et que l'option <strong>--secure-file-priv</strong> n'est pas activée.

```mysql
SELECT * FROM general_log INTO OUTFILE '/tmp/general-log.csv' FIELDS TERMINATED BY ';' ENCLOSED BY '"' LINES TERMINATED BY '\n';
```

#### Depuis la console

Le fichier généré peut être ouvert sur un tableur en tant que CSV avec une tabulation comme séparateur de champs, ou sur n'importe quel éditeur de texte.

```bash
mysql -u username -p -h 127.0.0.1 mysql -e "SELECT * FROM general_log" > general_log.csv
```