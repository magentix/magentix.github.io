Sur un serveur accessible à distance, les scans de port et les tentatives de connexion SSH sont légions. La solution la plus radicale est de tout bloquer, sauf les ports dont le serveur a besoin pour le ou les services qu'il propose.

**Attention :** il est indispensable pour un serveur distant (serveur dédié par exemple) d'autoriser l'accès SSH (port 22 par défaut) à plusieurs IPs fixes : la votre et des IPs de secours. **Si vous ne disposez pas d'IP fixe ne bloquez pas l'accès à SSH et proposez le service sur un autre port que 22.**

### Configuration

On vérifie dans un premier temps qu'iptables est bien en place sur le serveur, si ce n'est pas le cas, on procède à l'installation :

```bash
sudo apt-get install iptables
```

Pour contrôler les règles en place, on utilise la commande suivante :

```bash
sudo iptables -L
```

Par défaut, le pare-feu accepte toutes les connexions.

- **Chain INPUT :** les paquets entrants, de l'extérieur vers le serveur
- **Chain FORWARD :** les paquets redirigés
- **Chain OUTPUT :** les paquets sortants, du serveur vers l'extérieur

**Note :** nous appliquons dans cet article uniquement des règles sur le traffic entrant (INPUT).

### Règles du pare-feu

Le plus simple est d'écrire les règles souhaitées dans un fichier spécifique :

```bash
sudo nano /etc/iptables.custom.rules
```

Afin de bloquer le traffic sur l'ensemble des ports exceptés les 80, 443 et 22, nous utilisons les règles suivantes :

```
*filter

# Allow unlimited traffic on loopback
-A INPUT -i lo -j ACCEPT

# Allow ESTABLISHED and RELATED packets
-A INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT

# Allow traffic on specified ports (ex: web server)
-A INPUT -p tcp -m tcp --dport 80 -j ACCEPT
-A INPUT -p tcp -m tcp --dport 443 -j ACCEPT
-A INPUT -p tcp -m tcp --dport 22 -j ACCEPT # Comment for reject SSH connection

# Allow all for specified IPs (whitelist)
-A INPUT -s 123.123.123.123 -j ACCEPT
-A INPUT -s 456.456.456.456 -j ACCEPT

# Reject traffic other than for the rules mentioned above
-A INPUT -j DROP

COMMIT
```

N'oubliez pas de remplacer la whitelist par vos IPs.

```
# Allow all for specified IPs
-A INPUT -s 123.123.123.123 -j ACCEPT # Votre IP Fixe 1
-A INPUT -s 456.456.456.456 -j ACCEPT # Votre IP Fixe 2
# ...
```

### Application

Une fois les règles écrites, il ne reste plus qu'à les appliquer :

```bash
sudo iptables-restore > /etc/iptables.custom.rules
```

On vérifie que les règles sont bien appliquées :

```bash
sudo iptables -L
```

### Explications

#### Loopback

```
-A INPUT -i lo -j ACCEPT
```

Cette règle correspond au trafic loopback qui permet aux services de la machine de communiquer entre elles.

#### State

```
-A INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT
```

On autorise ici les connexions déjà établies.

#### Ports autorisés

```
-A INPUT -p tcp -m tcp --dport 80 -j ACCEPT
-A INPUT -p tcp -m tcp --dport 443 -j ACCEPT
-A INPUT -p tcp -m tcp --dport 22 -j ACCEPT
```

On établie la liste de tous les ports pour lesquels on autorise le traffic. Vous pouvez adapter cette liste selon le type de service proposé par le serveur.

#### Whitelist

```
-A INPUT -s 123.123.123.123 -j ACCEPT
-A INPUT -s 456.456.456.456 -j ACCEPT
```

Liste des IPs depuis lesquels l'accès à l'ensemble du serveur est autorisé. Si vous souhaitez bloquer l'accès SSH, assurez vous que cette liste d'IPs soit valide, au risque de ne plus pouvoir accéder au serveur.

#### Drop

```
-A INPUT -j DROP
```

On rejette tout le reste.

### Réinitialisation

Si vous souhaitez restaurer les règles par défaut (ACCEPT), utilisez la commande suivante :

```bash
sudo iptables -F
```