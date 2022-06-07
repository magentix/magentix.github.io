Pour certains sites e-commerce le moteur de recherche n'est pas une priorité. Par exemple si le site ne dispose que de quelques produits, voir même s'il est mono-produit. En imposant **Elasticsearch** il est également plus complexe d'installer Magento, ce n'est pas forcement adapté pour les commerçants avec un faible budget alloué à l'hébergement. Car Magento 2 peut parfaitement fonctionner sur un serveur à faible coût, à condition évidemment de rester sur des fonctionnalités classiques et de disposer d'un catalogue assez peu volumineux.

Se séparer d'**Elasticsearch** est donc adapté dans des cas très particuliers (sinon il serait dommage de s'en priver).

Pour supprimer **Elasticsearch** de Magento, ajoutez au noeud **replace** du fichier **composer.json** les lignes suivantes :

```json
{
    "replace": {
        "magento/module-elasticsearch": "*",
        "magento/module-elasticsearch-6": "*",
        "magento/module-elasticsearch-7": "*",
        "magento/module-inventory-elasticsearch": "*"
    }
}
```

Exécutez ensuite un `composer install`.

Pour les sites **Adobe Commerce**, ajoutez également `magento/module-elasticsearch-catalog-permissions`.

A ce stade vous pouvez faire tourner Magento sans disposer d'Elasticsearch. Le champ recherche apparaît mais une requête provoque une erreur.

### 1. Vous souhaitez conserver un moteur de recherche

Il est possible de revenir au moteur de type **MySQL** développé par Magento dans les versions antérieures.

Le module MySQL Search (Legacy) est mis à disposition par **Swissup** : [Legacy Mysql Search](https://github.com/swissup/module-search-mysql-legacy).

**Swissup** propose 2 manières d'installer le module, la première requiert l'installation de leur marketplace. Privilégiez une installation manuelle en décompressant l'archive de la [dernière release](https://github.com/swissup/module-search-mysql-legacy/tags) dans le dossier `app/code/Swissup/SearchMysqlLegacy`.

Une fois en place exécutez un `php bin/magento setup:upgrade`.

Il ne reste plus qu'à indiquer à Magento le moteur à utiliser. La configuration se situe dans le menu **Stores > Configuration > Catalog > Catalog > Catalog Search**.

Pour l'option **Search Engine**, sélectionnez **Legacy MySQL (deprecated)**.

![Legacy MySQL Magento](<{{ url }}media/blog/articles/legacy-mysql-magento.png>){: width="672" height="73" }

### 2. Vous souhaitez supprimer le moteur de recherche

Si vous n'avez pas besoin d'un moteur de recherche, plusieurs modules sont à désactiver. La fonctionnalité **staging** ne sera plus disponible.

```json
{
    "replace": {
        "magento/module-elasticsearch": "*",
        "magento/module-elasticsearch-6": "*",
        "magento/module-elasticsearch-7": "*",
        "magento/module-inventory-elasticsearch": "*",
        "magento/module-advanced-search": "*",
        "magento/module-catalog-search": "*",
        "magento/module-search": "*",
        "magento/module-inventory-catalog-search": "*",
        "magento/module-search-staging": "*",
        "magento/module-bundle-import-export-staging": "*",
        "magento/module-bundle-staging": "*",
        "magento/module-catalog-import-export-staging": "*",
        "magento/module-catalog-inventory-staging": "*",
        "magento/module-catalog-page-builder-analytics-staging": "*",
        "magento/module-catalog-rule-staging": "*",
        "magento/module-catalog-staging": "*",
        "magento/module-catalog-staging-page-builder": "*",
        "magento/module-catalog-url-rewrite-staging": "*",
        "magento/module-checkout-staging": "*",
        "magento/module-cms-page-builder-analytics-staging": "*",
        "magento/module-cms-staging": "*",
        "magento/module-configurable-product-staging": "*",
        "magento/module-downloadable-staging": "*",
        "magento/module-gift-card-staging": "*",
        "magento/module-gift-message-staging": "*",
        "magento/module-gift-wrapping-staging": "*",
        "magento/module-google-optimizer-staging": "*",
        "magento/module-grouped-product-staging": "*",
        "magento/module-layered-navigation-staging": "*",
        "magento/module-msrp-staging": "*",
        "magento/module-payment-staging": "*",
        "magento/module-product-video-staging": "*",
        "magento/module-review-staging": "*",
        "magento/module-reward-staging": "*",
        "magento/module-rma-staging": "*",
        "magento/module-sales-rule-staging": "*",
        "magento/module-search-staging": "*",
        "magento/module-staging": "*",
        "magento/module-staging-page-builder": "*",
        "magento/module-weee-staging": "*"
    }
}
```

Pour les sites **Adobe Commerce**, prévoyez également de vous séparer de `magento/module-quick-order` (B2B) et de `magento/module-elasticsearch-catalog-permissions`.

Cette fois le champ de recherche natif n'apparaît plus.