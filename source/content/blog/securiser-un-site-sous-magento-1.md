**Magento 1** restera dans l'histoire comme une solution e-commerce exceptionnelle : une communauté Française et internationale très active et dynamique (conférences, blogs, forums...), un panel de fonctionnalités natives impressionnant, des milliers de modules développés et mis à disposition par des développeurs du monde entier. Magento a déchaîné les passions pendant plus de 10 ans.

Tout le monde en parle depuis plusieurs années, cette date fatidique où Magento 1 deviendra un **produit EOL** (End Of Life). On se sert souvent de cette date pour mettre une certaine pression sur les commerçants, j'ai pu lire de tout et de n'importe quoi sur les réseaux, dans des communiqués ou des blogs.

L'argument n°1 avancé est la **sécurité** : des failles de sécurité énormes vont apparaître, des vols de carte et de données personnelles... L'argument n°2 est l'**obsolescence des technologies** utilisées par la solution (framework, Zend, PHP).

Ces 2 arguments sont légitimes, mais NON, Magento 1 n'explosera pas en **juin 2020** et continuera de tourner correctement.

Tout d'abord, en suivant certaines règles, il est aisé de **sécuriser Magento 1**, et cela pour plusieurs années. Et comme 95% des commerçants de taille moyenne, le paiement est effectué sur une plateforme externe (le client est redirigé).

Pour les technologies elles ne sont certes pas modernes, mais resteront pérennes. Le seul frein restera certainement PHP (sauf si vous optez pour la version Magento 1 LTS OpenMage ou que vous avez à disposition une équipe de développeur). Notez que rendre compatible Magento 1.9.4 avec PHP 7.4 ne prend que quelques heures (hors extensions tierces) et garantie la sécurité de PHP jusqu'au 28 novembre 2022. Reste également l'option headless permettant d'isoler complètement le front (si vous vous sentez prêt à adopter cette techno).

Ce qui est cependant inévitable, c'est le **sentiment de solitude**. Les développeurs Magento 1 sont passés pour beaucoup à autre chose. Les blogs, ressources et forums disparaissent les uns après les autres (on a connu la fermeture de Magento Connect, des forums officiels, puis de Fragento). Plus aucun module n'est développé ni mis à jour depuis déjà quelques années. Si vous souhaitez rester sur Magento 1 ou reporter une migration, il est indispensable de conserver un développeur Magento 1 confirmé, car pour du e-commerce, il y a toujours des milliers de choses à expérimenter.

Voici donc **plusieurs astuces pour sécuriser** votre plateforme. Cela ne couvre pas les risques à 100%, des développements spécifiques et des modules externes peuvent toujours être à l'origine de failles.

L'idée principale est de **cacher un maximum aux bots** que votre site est sous Magento 1. Car au delà de sécuriser la plateforme, des **centaines de bots** parcourent le web à la recherche de CMS connus (wordpress, Prestashop, Magento...) afin d'en **exploiter les failles**.

1. [Nettoyer les fichiers et dossiers à la racine](<#p1>)
2. [Un accès au backoffice sécurisé](<#p2>)
3. [Effectuer une montée en version](<#p3>)
4. [Empêcher la navigation dans les dossiers](<#p4>)
5. [Désactiver les modules inutiles](<#p5>)
6. [Ajouter aux entêtes HTTP un Content Security Policy](<#p6>)
7. [Bloquer les détecteurs de CMS](<#p7>)
8. [Bloquer l'accès à certains fichiers natifs](<#p8>)
9. [Protéger les variables dynamiques dans les templates](<#p9>)
10. [Modifier le nom des routes](<#p10>)
11. [Modifier le nom du cookie frontend](<#p11>)
12. [Déplacer les dossiers js, skin et media dans un sous dossier](<#p12>)
13. [Déplacer les variables Javascript](<#p13>)
14. [Sécuriser les cookies](<#p14>)

### 1. Nettoyer les fichiers et dossiers à la racine {: #p1 }

On supprime sans aucun risque les dossiers et fichiers suivants :

- downloader
- dev
- .htaccess.sample
- LICENSE.html
- LICENSE.txt
- LICENSE_AFL.txt
- README.md
- RELEASE_NOTES.txt
- index.php.sample
- php.ini.sample

### 2. Un accès au backoffice sécurisé {: #p2 }

Si cela n'est pas déjà fait, on met à jour le chemin de l'admin dans le fichier **app/etc/local.xml**.

```xml
<admin>
    <routers>
        <adminhtml>
            <args>
                <frontName><![CDATA[cheminAdminSecure]]></frontName>
            </args>
        </adminhtml>
    </routers>
</admin>
```

Le chemin d'accès à l'admin doit être tout sauf **admin** ou **manager**.

Dans le fichier **.htaccess** à la racine de Magento (après la ligne **RewriteEngine on**), on autorise uniquement l'accès à des IPs définies :

```apache
RewriteCond %{REQUEST_URI} ^/(index.php/)?cheminAdminSecure(.*) [NC]
RewriteCond %{REMOTE_ADDR} !^1.1.1.1
RewriteCond %{REMOTE_ADDR} !^2.2.2.2
RewriteRule .* - [F,L]
```

Remplacez **1.1.1.1**, **2.2.2.2** etc... par vos IPs.

Si vous n'avez pas d'IP fixe l'idéal est un VPN. On peut obtenir une adresse IP v4 fixe facilement via un VPN sécurisé comme [myip.io](<https://www.myip.io>) (le meilleur que j'ai trouvé, fiable, sécurisé et compatible avec n'importe quelle plateforme via OpenVPN, choisir **Dedicated-VPN - France**).

### 3. Effectuer une montée en version {: #p3 }

Si ce n'est pas déjà fait, une migration vers la toute dernière release de Magento est recommandée (actuellement **1.9.4.5**).

**Note :** Magento a introduit dans sa version **1.9.4.3** le cryptage des mots de passe avec **bcrypt**, ce qui est une très bonne chose. Cette évolution a disparu de Magento **1.9.4.5** (pour SHA256) car il est impossible de migrer les mots de passe des clients en **bcrypt** vers Magento 2.
{: .info }

- [Télécharger SUPEE-11346 - Dernier patch de sécurité (22/06/2020)](<{{ url }}media/blog/download/supee-11346_ce_1.5.0.0_-_1.9.4.5_-2020-06-22-03-13-11.zip>)
- [Télécharger Magento 1.9.4.5 (29/04/2020)](<{{ url }}media/blog/download/magento-1.9.4.5-2020-04-29-01-29-17.tar.gz>)
- [Télécharger Magento 1.9.4.4 (28/01/2020)](<{{ url }}media/blog/download/magento-1.9.4.4-2020-01-28-04-53-25.tar.gz>)
- [Télécharger Magento 1.9.4.3 (08/10/2019)](<{{ url }}media/blog/download/magento-1.9.4.3-2019-10-08-05-28-41.tar.gz>)

### 4. Empêcher la navigation dans les dossiers {: #p4 }

Dans le fichier **.htaccess** à la racine de Magento, on ajoute tout en haut la ligne suivante :

```
Options -Indexes
```

Les hébergeurs activent généralement cette option par défaut, mais on ne sait jamais.

### 5. Désactiver les modules inutiles {: #p5 }

Moins il y en a, mieux c'est. Voici une liste de module natifs que vous pouvez désactiver sans problème si vous n'en avez pas l'utilité :

- Mage_AdminNotification
- Mage_Compiler
- Mage_ConfigurableSwatches
- Mage_Usa
- Mage_Paygate
- Mage_Paypal
- Mage_PaypalUk
- Mage_GoogleCheckout
- Mage_Poll
- Mage_Tag
- Mage_Reports
- Mage_Newsletter
- Mage_Sendfriend
- Mage_Rss
- Mage_ProductAlert
- Mage_Api
- Mage_Api2
- Mage_Authorizenet
- Mage_Downloadable
- Mage_ImportExport
- Mage_Oauth
- Mage_XmlConnect
- Phoenix_Moneybookers

### 6. Ajouter aux entêtes HTTP un Content Security Policy {: #p6 }

Les CSP permettent d'éviter l'exploitation de failles XSS en contrôlant les ressources externes et internes que vous utilisez. Par exemple :

```apache
<IfModule mod_headers.c>
Header set Content-Security-Policy "default-src 'self' www.youtube.com fonts.gstatic.com; style-src 'self' 'unsafe-inline' fonts.googleapis.com; script-src 'self' 'unsafe-inline' 'unsafe-eval' www.googletagmanager.com www.google-analytics.com maps.googleapis.com; img-src 'self' www.google-analytics.com maps.gstatic.com maps.googleapis.com data:; base-uri 'self'"
</IfModule>
```

Cet exemple n'autorise aux navigateurs que les resources externes en provenance de **Google analytics**, **Google Fonts**, **Youtube** et **Google Maps**. Il convient évidemment de l'adapter à vos besoins. N'hésitez pas à vous documenter sur les CSP : [Utiliser une stratégie de sécurité du contenu (Content Security Policy)](<{{ url }}blog/strategie-de-securite-du-contenu-content-security-policy.html>).

### 7. Bloquer les détecteurs de CMS {: #p7 }

Il existe de nombreux détecteurs de CMS, il est possible d'en identifier certains. Pour bloquer l'analyse des 2 plus populaires, il faut ajouter les lignes suivantes au fichier **.htaccess** (après la ligne **RewriteEngine on**) :

```apache
RewriteCond %{HTTP_USER_AGENT} (WhatCMS|Wappalyzer) [NC]
RewriteRule .* - [F,L]
```

### 8. Bloquer l'accès à certains fichiers natifs {: #p8 }

Via le fichier **.htaccess** à la racine de Magento, on interdit l'exécution de certains fichiers depuis l'extérieur :

```apache
<Files .gitignore>
    order allow,deny
    deny from all
</Files>

<Files install.php>
    order allow,deny
    deny from all
</Files>

<Files api.php>
    order allow,deny
    deny from all
</Files>

<Files cron.sh>
    order allow,deny
    deny from all
</Files>

<Files cron.php>
    order allow,deny
    deny from all
</Files>

<Files mage>
    order allow,deny
    deny from all
</Files>
```

### 9. Protéger les variables dynamiques dans les templates {: #p9 }

Pour éviter les failles XSS, il conviendra de vérifier dans tous vos templates que les variables dynamiques passent bien par un **escapeHtml** :

```php+HTML
<?php echo $this->escapeHtml($variable) ?>
```

### 10. Modifier le nom des routes {: #p10 }

Les bots viennent scanner l'existence des routes natives (**/contacts**, **/customer/account/login**...).

Les modifier est très rapide mais il faudra **contrôler tous les liens de votre site**, surtout ceux saisis en dur (pages CMS, blocs...).

Depuis le fichier **config.xml** d'un module dédié, ajoutez les noeuds suivants (surcharge des frontName natifs) :

```xml
<?xml version="1.0"?>
<config>
    ...
    <frontend>
        ...
        <routers>
            <customer>
                <use>standard</use>
                <args>
                    <module>Mage_Customer</module>
                    <frontName>ctm</frontName> <!-- /customer/* >> /ctm/* -->
                </args>
            </customer>
            <checkout>
                <use>standard</use>
                <args>
                    <module>Mage_Checkout</module>
                    <frontName>ckt</frontName> <!-- /checkout/* >> /ckt/* -->
                </args>
            </checkout>
            <contacts>
                <use>standard</use>
                <args>
                    <module>Mage_Contacts</module>
                    <frontName>cts</frontName> <!-- /contacts/* >> /cts/* -->
                </args>
            </contacts>
        </routers>
    </frontend>
</config>
```

Adaptez avec le nom de chemins avec ce que vous souhaitez. Les anciennes routes deviendront des **pages 404**.

### 11. Modifier le nom du cookie frontend {: #p11 }

Magento génère un cookie nommé **frontend**. Certains bots contrôlent l'existence de ce cookie dans l'en-tête HTTP pour s'assurer que le site est bien sur Magento.

Pour changer le nom du cookie, copiez le fichier :

- app/code/**core**/Mage/Core/Controller/Varien/Action.php
  {: .file }

Dans :

- app/code/**local**/Mage/Core/Controller/Varien/Action.php
  {: .file }

Modifiez le nom du namespace par celui de votre choix :

```php
/**
 * Session namespace to refer in other places
 */
const SESSION_NAMESPACE = 'frontend'; // Par exemple : navigation
```

**Note :** Cette technique de surcharge "directe" dans local a toujours été déconseillée, mais Magento 1 ne connaîtra plus aucune mise à jour...
{: .info }

### 12. Déplacer les dossiers js, skin et media dans un sous dossier {: #p12 }

Les bots scannent très souvent les dossiers **skin**, **media** et **js** à la recherche de fichiers connus pour leur vulnérabilité. Les déplacer réglera immédiatement le problème.

Dans le fichier **app/etc/config.xml**, modifiez les chemins suivants :

```xml
<media>{{root_dir}}/media</media>
<upload>{{root_dir}}/media/upload</upload>
<skin>{{root_dir}}/skin</skin>
```

Avec le dossier de votre choix (ici **pub**) :

```xml
<media>{{root_dir}}/pub/media</media>
<upload>{{root_dir}}/pub/media/upload</upload>
<skin>{{root_dir}}/pub/skin</skin>
```

Copiez le fichier :

- app/code/**core**/Mage/Core/Model/Config/Options.php
  {: .file }

Dans :

- app/code/**local**/Mage/Core/Model/Config/Options.php
  {: .file }

Ajoutez en bas de la méthode `_construct()` :

```php
$this->_data['media_dir'] = $this->_data['base_dir'] . DS . 'pub/media';
$this->_data['skin_dir'] = $this->_data['base_dir'] . DS . 'pub/skin';
```

Copiez ensuite le fichier :

- app/code/**core**/Mage/Page/Block/Html/Head.php
  {: .file }

Dans :

- app/code/**local**/Mage/Page/Block/Html/Head.php
  {: .file }

Pour la méthode `&_prepareStaticAndSkinElements`, remplacez la ligne suivante :

```php
$items[$params][] = $mergeCallback ? Mage::getBaseDir() . DS . 'js' . DS . $name : $baseJsUrl . $name;
```

Par :

```php
$items[$params][] = $mergeCallback ? Mage::getBaseDir() . DS . 'pub/js' . DS . $name : $baseJsUrl . $name;
```

Modifiez en backoffice, en base de données ou via le setup d'un module les chemins pour **skin**, **media** et **js** :

```php
<?php

/** @var $installer Mage_Core_Model_Resource_Setup */
$installer = $this;

$installer->setConfigData('web/unsecure/base_skin_url', '{{unsecure_base_url}}pub/skin/');
$installer->setConfigData('web/unsecure/base_media_url', '{{unsecure_base_url}}pub/media/');
$installer->setConfigData('web/unsecure/base_js_url', '{{unsecure_base_url}}pub/js/');
$installer->setConfigData('web/secure/base_skin_url', '{{secure_base_url}}pub/skin/');
$installer->setConfigData('web/secure/base_media_url', '{{secure_base_url}}pub/media/');
$installer->setConfigData('web/secure/base_js_url', '{{secure_base_url}}pub/js/');
```

Pour finir, dans le fichier **.htaccess** à la racine de Magento, modifiez la ligne suivante :

```apache
RewriteCond %{REQUEST_URI} !^/(media|skin|js)/
```

Avec :

```apache
RewriteCond %{REQUEST_URI} !^/(media|skin|js|pub)/
```

Il ne reste plus qu'à déplacer les dossiers **skin**, **media** et **js** dans un nouveau dossier **pub** à la racine :

![Arborescence Magento]({{ url }}media/blog/articles/magento-pub.png){: width="265" height="351" }

### 13. Déplacer les variables Javascript {: #p13 }

Les bots analysent parfois le contenu de la page à la recherche de code connu. Les variables JS (Mage.Cookies.path, optionalZipCountries, Translator) trahissent Magento.

L'idée est de déplacer ces variables JS dans un fichier script "dynamique" :

```html
<script type="text/javascript" src="https://.../dynamic/script.js"></script>
```

J'entends par **dynamique** que le fichier est composé de blocs ne contenant que du JS et généré via l'action d'un contrôleur, le téléchargement du fichier est forcé (pas de cache navigateur). Nous pourrions également utiliser le cache navigateur mais avec un système de versionning lors de mises à jour (script.js?v=1.0).

```php
public function indexAction()
{
    /** @var Mage_Core_Model_Date $date */
    $date = Mage::getModel('core/date');
    /** @var string $gmtDate */
    $gmtDate = $date->date("D, d M Y H:i:s") . ' GMT';

    $this->getResponse()->setHeader('Content-Type', 'application/javascript');
    $this->getResponse()->setHeader('Last-Modified', $gmtDate, true);
    $this->getResponse()->setHeader('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0', true);
    $this->getResponse()->setHeader('Pragma', 'no-cache', true);
    $this->getResponse()->setHeader('Expires', 'Sat, 26 Jul 1997 05:00:00 GMT', true);

    $this->loadLayout(false);
    $this->renderLayout();
}
```

Vous pouvez récupérer le module complet via le lien suivant : [Magentix_DynamicJs](<{{ url }}media/blog/download/Magentix_DynamicJs.tar.gz>)

![Fichier Script Magento]({{ url }}media/blog/articles/magento-dynamic-script.png){: width="604" height="116" }

### 14. Sécuriser les cookies {: #p14 }

Par défault, les cookies frontend sont servis avec l'attribut **Secure** à *false* et l'attribut **sameSite** à *None*.

Il est propable que ces cookies soient un jour refusés par les navigateurs. Firefox dans les dernières versions affiche par exemple le message suivant :

> Le cookie "frontend" sera bientôt rejeté car son attribut "sameSite" est défini sur "none" ou une valeur invalide, et sans attribut "secure"

![Cookie]({{ url }}media/blog/articles/cookie.png){: width="350" height="200" }

Une simple surcharge de la classe **Mage_Core_Model_Cookie** permet de corriger ce problème :

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config>
    <modules>
        <Magentix_SecureCookie>
            <version>1.0.0</version>
        </Magentix_SecureCookie>
    </modules>
    <global>
        <models>
            <core>
                <rewrite>
                    <cookie>Magentix_SecureCookie_Model_Cookie</cookie>
                </rewrite>
            </core>
        </models>
    </global>
</config>
```

Nous indiquons que le cookie doit être sécurisé et ajoutons la valeur **strict** pour l'attribut **sameSite**.

**Note :** si le client est redirigé vers une plateforme bancaire pour le paiement, utilisez plutôt la valeur **lax**.

```php
<?php

class Magentix_SecureCookie_Model_Cookie extends Mage_Core_Model_Cookie
{
    /**
     * Is https secure request
     * {override} use secure cookie on frontend
     *
     * @return bool
     * @throws Mage_Core_Model_Store_Exception
     */
    public function isSecure()
    {
        return $this->_getRequest()->isSecure();
    }

    /**
     * Retrieve Path for cookie
     * {override} Force strict for samesite
     *
     * @return string
     */
    public function getPath()
    {
        $path = parent::getPath();

        return $path . '; samesite=strict';
    }
}
```