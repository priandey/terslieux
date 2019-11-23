# Tiers-Lieux
## Définition
Les tiers-lieux fleurissent aujourd'hui en France. Des jardins partagés, des espaces de co-working, 
des cafés associatifs, etc. Tout ces espaces ont en commun une gestion des ouvertures et permanences souvent par
des bénévoles. 

Tiers-Lieux se veut une petite application web facile à prendre en main permettant de référencer 
l'ouverture d'un lieu. Elle permet d'une part de publier l'information auprès du public et d'autre part
aux associations ou entreprises en charge des lieux de garder trace de ces ouvertures.

## Un tour du propriétaire
### Les fonctionalitées implémentées :
#### Référencement d'un lieu
Vous pouvez enregistrer un lieu sur le service en cliquant sur le bouton « + » de votre interface
utilisateur.

![Ajouter une localisation](https://github.com/priandey/tierslieux/blob/dev/tutorial/img/add_location.jpg)

L'utilisateur ayant référencé un lieu devient automatiquement le modérateur de ce dernier. 

**Attention : Pour le moment, un lieu ne peux avoir qu'un seul modérateur, et celui-ci ne peux pas être changé par la suite**

#### Gestion des bénévole
Les bénévoles et les modérateurs sont les seuls utilisateur à pouvoir déclarer un lieu ouvert. 
Pour gérer les bénévole, cliquez sur le Panneau de modération depuis la page du lieu.

![Ouvrir le panneau de modération](https://github.com/priandey/tierslieux/blob/dev/tutorial/img/moderator_pannel.jpg)

S'affiche un récapitulatif des bénévoles liées au lieu, ainsi que des différentes demandes en cours. 

![Détail de la gestion des bénévoles](https://github.com/priandey/tierslieux/blob/dev/tutorial/img/volunteers_pannel.jpg)

En **1** :  Tout les bénévoles actifs du lieu.

En **2** : Une liste des utilisateurs ayant demandé à être bénévoles.

En **3** : Les invitations que vous avez envoyé.

En **4** : Ce formulaire permet d'envoyer une invitation à un bénévole, **si celui-ci n'est pas inscrit sur
le site, vous serez redirigés vers une autre page vous permettant de lui créer un compte.**

#### Ouvrir un lieu
Pour ouvrir un lieu, rien de plus simple, rendez-vous sur la page du lieu (ex: http://tierslieux.priandye.eu/l/mon-lieu)
et cliquez sur **«Ouvrir le lieu»**. Renseignez ensuite un titre pour l'ouverture (ex : "Permanence", 
"Boutures des framboisiers"), une description plus détaillée, puis validez.

#### Fermer un lieu
Une fois qu'un lieu est déclaré ouvert, les bénévoles et le modérateur peuvent le déclarer
fermé en cliquant sur **«Fermer le lieu»**.

#### Obtenir les données d'ouverture d'un lieu
Il est possible pour le modérateur d'obtenir les données d'ouvertures d'un lieu. Pour cela, cliquez
sur l'onglet statistique du panneau de modération d'un lieu. Dans un premier temps, les données sont
accessibles au format de pdf, elles seront très bientôt disponible en CSV.

## Et pour la suite ? 
De nouvelles fonctionnalitées sont en cours de développement.

- Version **1.0** : Ajout d'un service de géolocalisation pour les lieux, prise en charge des images pour la page
personnalisées d'un lieu

- Version **1.5** : Notification mail à l'ouverture d'un lieu en favori, API REST, refonte de l'interface.

- Version **2.0** : Version mobile "Progressive Web App" avec notification push, publication d'un lieu ou non.