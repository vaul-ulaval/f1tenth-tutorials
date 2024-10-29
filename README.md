# Tutoriels F1tenth

## Introduction

Le but du repo suivant sera de vous initier à la robotique avec le projet F1tenth. Il s'agit essentiellement d'une feuille de route afin de vous guider dans votre apprentissage.

### Pré-requis

- Git
- Python 3.10


## Projet F1tenth

F1tenth est une plateforme open-source dédiée à la recherche et à l'éducation sur les systèmes autonomes. Des étudiants et des chercheurs du monde entier l'utilisent pour apprendre et expérimenter dans les domaines de la perception, de la planification et du contrôle en construisant une voiture radiocommandée à l'échelle 1/10e d'une voiture de Formule 1. La F1tenth Foundation organise régulièrement des Grands Prix F1tenth lors de conférences internationales sur la robotique, où des équipes s'affrontent sur la piste pour déterminer qui a la voiture la plus rapide, mais surtout, les meilleurs algorithmes.


## Base de la robotique

Afin d'être à l'aise avec la terminologie de la robotique et d'avoir un survol de chaque discipline (perception, planning, contrôle), les séminaires suivants sont un très bon point de départ: https://github.com/vaul-ulaval/vaul-wiki/wiki/S%C3%A9minaires-de-robotique-mobile


## Simulateur F1tenth AutoDRIVE

Avant de commencer à travailler sur un vrai robot, nous allons commencer par installer le simulateur F1tenth [AutoDRIVE](https://autodrive-ecosystem.github.io/). Ce simulateur est basé sur Unity et est rapide à mettre en place afin de commencer à expérimenter.

### Installation du simulateur

1. Télécharger le simulateur pour votre système d'exploitation: https://github.com/Tinker-Twins/AutoDRIVE/tree/AutoDRIVE-Simulator
2. Une fois téléchargé, vous devriez avoir un fichier exécutable. Simplement à le double-cliquer pour lancer le simulateur. (Si vous êtes sous Linux, vous allez devoir ajouter la permission d'exécution)

*Si vous avez une erreur concernant Microsoft Visual C++ en ouvrant le simulateur, télécharger [ceci](https://visualstudio.microsoft.com/visual-cpp-build-tools/.)*

Une fois ouvert, je vous recommande de jouer un peu avec le simulateur pour explorer les différents menus/options disponibles. Ce sera pratique pour le développement plus tard

### Utilisation du devkit

Afin de pouvoir écrire des algorithmes pour contrôler le véhicule, on devra utiliser le devkit afin de pouvoir lancer un serveur qui recevra les données du simulateur et qui enverra les commandes autonomes à effectuer.

1. Ouvrir le répertoire suivant en ligne de commande et faire:
```bash
cd labs
```
2. Installer les dépendences Python
```bash
pip3 install -r requirements.txt
```
3. Exécuter le script python afin de lancer le serveur de commandes:
```bash
python example.py # Le script devrait s'exécuter sans erreurs
```

### Exécution d'un premier algorithme

Ouvrir le code du script [example.py](./labs/example.py) et analyser un peu ce qui se passe. On remarque que vers la fin du script, on envoie une commande de `throttle` et de `steering` de `1.0`, ce qui signifie de tourner le volant à gauche au max et de donner toute la puissance moteur disponible. Testons ces hypothèses avec le simulateur!

1. Démarrer le simulateur (Le fichier exécutable démarrer précédemment)
2. Démarrer le serveur de commandes [example.py](./labs/example.py)
```bash
python example.py
```
3. Dans l'interface du simulateur, cliquer sur le bouton `Connect` afin de se connecter au serveur de commande. Normalement l'interface devrait afficher `Connected`
4. Ensuite, changer le mode de conduite de `Manual` à `Autonomous`.
5. Si tout est bien connecté, normalement le véhicule devrait exécuter les commandes autonomes mentionnés plus tôt

Bravo! Vous avez exécuté votre premier algorithme de contrôle en simulation! Maintenant il est temps de programmer des algorithmes plus intéressants.


## Laboratoires F1tenth

Les différents [laboratoires F1tenth](https://www.youtube.com/watch?v=v6w_zVHL8WQ&list=PL7rtKJAz_mPdFDJtufKmqfWRNu55s_LMc) explorent bien les bases de la conduite autonome. Dans les différentes vidéos/solutions, on discute de ROS, mais il est possible de réaliser tous ces laboratoires sans ROS avec le simulateur installé précédemment.

Pour réaliser ces laboratoires, vous pouvez dupliquer le fichier [example.py](./labs/example.py) et programmer dedans. Ensuite, vous pourrez simplement suivre les mêmes étapes qu'auparavant pour exécuter votre code, simplement à changer le nom du fichier python à exécuter.

Pour avoir accès aux informations provenant des capteurs du f1tenth, regardez le code dans [autodrive.py](./labs/autodrive.py). On peut y voir toutes les informations qui sont disponibles. Par exemple, `lidar_range_array` correspond au scan de lidar.

Certaines solutions des laboratoires sont fournis, cependant, on vous recommande fortement de faire les exercices sans regarder la solution d'abord.

### 1er laboratoire: Système de frein d'urgence

Apprentissages importants:
- Développer un algorithme avec le simulateur
- Qu'est-ce qu'un lidar?
- Récupérer un scan Lidar à un angle donné
- Envoyer des commandes de contrôle au robot

[Vidéo explicative](https://www.youtube.com/watch?v=k4FQ-dZ0Lp8&list=PL7rtKJAz_mPdFDJtufKmqfWRNu55s_LMc&index=3)

[Instructions](https://github.com/f1tenth/f1tenth_lab2_template)

[Solution](./solutions-labs/emergency_braking.py)

### 2ème laboratoire: Suivi de murs

Apprentissages importants:
- Contrôle PID
- Objectif de contrôle (Suivre le mur à une distance de `d` mètres)

[Vidéo explicative](https://www.youtube.com/watch?v=qIpiqhO3ITY&list=PL7rtKJAz_mPdFDJtufKmqfWRNu55s_LMc&index=6)

[Instructions](https://github.com/f1tenth/f1tenth_lab3_template)

[Solution](./solutions-labs/wall_follow.py)

### 3ème laboratoire: Suivi de trou

Apprentissages importants:
- Algorithme réactif
- Évitement d'obstacle de base

[Vidéo explicative](https://www.youtube.com/watch?v=5asfD-_Z9x8&list=PL7rtKJAz_mPdFDJtufKmqfWRNu55s_LMc&index=7)

[Instructions](https://github.com/f1tenth/f1tenth_lab4_template)

[Solution (Avec ROS)](https://github.com/vaul-ulaval/gap_following/blob/dev/scripts/gap_following_node.py)

## Introduction à Robot Operating System (ROS)

Avant de développer des algorithmes plus complexes, il sera nécessaire d'apprendre les bases de ROS. ROS est un middleware s'installant sur Ubuntu permettant de distribuer un système robotique en plusieurs parties. Celui-ci fourni également plusieurs outils indispensable pour le déboguage comme Rviz ou l'enregistrement de rosbags.

**ROS est très important à apprendre puisque c'est ce qui est utilisé sur chacun de nos robots**

### Séminaire d'introduction

Pour s'introduire à ROS, si ce n'est pas déjà fait, vous pouvez consulter le [séminaire d'introduction](https://www.youtube.com/watch?v=vAb5SnaJbF0&list=PL125ARjD2GAQM5pfGsJEozWxafsucLw1G&index=4).

### Installation de ROS dans une machine virtuelle

Avec la connaissance de base de ROS, passons maintenant à l'action. Afin de comprendre comment installer ROS et l'utiliser, on vous suggère de vous créer une machine virtuelle avec Ubuntu 22:

1. Télécharger [VirtualBox](https://www.virtualbox.org/)
2. Télécharger le fichier .ISO d'[Ubuntu 22 desktop](https://releases.ubuntu.com/jammy/)
3. Suivre les [étapes suivantes](https://ubuntu.com/tutorials/how-to-run-ubuntu-desktop-on-a-virtual-machine-using-virtualbox#1-overview) pour installer votre machine virtuelle

Une fois la machine virtuelle fonctionnelle, installer ROS2 humble sur celle-ci en suivant la [page d'installation](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html)

### Tutoriels ROS

Afin d'avoir une expérience hands-on, on vous suggère maintenant de suivre les [tutoriels officiels suivants](https://docs.ros.org/en/humble/Tutorials.html) afin de jouer avec cette nouvelle installation de ROS.