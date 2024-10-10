# Tutoriels F1tenth

## Introduction

Le but du repo suivant sera de vous initier à la robotique avec le projet F1tenth. Il s'agit essentiellement d'une feuille de route afin de vous guider dans votre apprentissage.

### Pré-requis

- Git
- Python >=3.8


## Projet F1tenth

F1tenth est une plateforme open-source dédiée à la recherche et à l'éducation sur les systèmes autonomes. Des étudiants et des chercheurs du monde entier l'utilisent pour apprendre et expérimenter dans les domaines de la perception, de la planification et du contrôle en construisant une voiture radiocommandée à l'échelle 1/10e d'une voiture de Formule 1. La F1tenth Foundation organise régulièrement des Grands Prix F1tenth lors de conférences internationales sur la robotique, où des équipes s'affrontent sur la piste pour déterminer qui a la voiture la plus rapide, mais surtout, les meilleurs algorithmes.


## Base de la robotique

Afin d'être à l'aise avec la terminologie de la robotique et d'avoir un survol de chaque discipline (perception, planning, contrôle), les séminaires suivants sont un très bon point de départ: https://github.com/vaul-ulaval/vaul-wiki/wiki/S%C3%A9minaires-de-robotique-mobile


## Simulateur F1tenth AutoDRIVE

Avant de commencer à travailler sur un vrai robot, nous allons commencer par installer le simulateur F1tenth [AutoDRIVE](https://autodrive-ecosystem.github.io/). Ce simulateur est basé sur Unity et est rapide à mettre en place afin de commencer à expérimenter.

### Installation du simulateur

1. Télécharger le simulateur pour votre système d'exploitation: https://github.com/Tinker-Twins/AutoDRIVE/tree/AutoDRIVE-Simulator
2. Une fois téléchargé, vous devriez avoir un fichier exécutable. Simplement à le double-cliquer pour lancer le simulateur

Une fois ouvert, je vous recommande de jouer un peu avec le simulateur pour explorer les différents menus/options disponibles. Ce sera pratique pour le développement plus tard

### Installation du devkit

Afin de pouvoir écrire des algorithmes pour contrôler le véhicule, on devra télécharger le devkit afin de pouvoir lancer un serveur qui recevra les données du simulateur et qui enverra les commandes autonomes à effectuer.

1. Cloner le répertoire suivant avec la commande suivante:
```bash
git clone --single-branch --branch AutoDRIVE-Devkit https://github.com/Tinker-Twins/AutoDRIVE.git
```
2. Le répertoire contient différents exemples pour plusieurs languages de programmation, nous allons utiliser Python.
```bash
cd 'AutoDRIVE/ADSS Toolkit/autodrive_py'
```
3. Installer les dépendences Python en fonction de votre version de Python
```bash
pip3 install -r requirements_python_3.10.txt # Remplacer 3.10 par votre version de Python
```
4. Exécuter le script python afin de lancer le serveur de commandes:
```bash
python example_f1tenth.py # Le script devrait s'exécuter sans erreurs
```

### Exécution d'un premier algorithme

Ouvrir le code du script `example_f1tenth.py` et analyser un peu ce qui se passe. On remarque que vers la fin du script, on envoie une commande de `throttle` et de `steering` de `1`, ce qui signifie de tourner le volant à gauche au max et de donner toute la puissance moteur disponible. Testons ces hypothèses avec le simulateur!

1. Démarrer le simulateur
2. Démarrer le serveur de commandes `example_f1tenth.py`
```bash
python example_f1tenth.py
```
3. Dans l'interface du simulateur, cliquer sur le bouton `Connect` afin de se connecter au serveur de commande. Normalement l'interface devrait afficher `Connected`
4. Ensuite, changer le mode de conduite de `Manual` à `Autonomous`.
5. Si tout est bien connecté, normalement le véhicule devrait exécuter les commandes autonomes mentionnés plus tôt

Bravo! Vous avez exécuté votre premier algorithme de contrôle en simulation! Maintenant il est temps de programmer des algorithmes plus intéressants.


## Laboratoires F1tenth

Les différents laboratoires F1tenth explore bien les bases de la conduite autonome. Dans les différentes vidéos/solutions, on discute de ROS, mais il est possible de réaliser tous ces laboratoires sans ROS avec le simulateur installé précédemment.

Les solutions des laboratoires sont en ROS, mais vous pouvez quand même analyser le code et avoir une idée de quoi faire

### 1er laboratoire: Système de frein d'urgence

Apprentissages importants:
- Développer un algorithme avec le simulateur
- Qu'est-ce qu'un lidar?
- Récupérer un scan Lidar à un angle donné
- Envoyer des commandes de contrôle au robot

Voir: https://www.youtube.com/watch?v=k4FQ-dZ0Lp8

Instructions: https://github.com/f1tenth/f1tenth_lab2_template

Solution (en ROS avec Python): https://github.com/vaul-ulaval/emergency_braking_node/blob/dev/ttc-speed-projection/scripts/safety_node.py

### 2ème laboratoire: Suivi de murs

Apprentissages importants:
- Contrôle PID
- Objectif de contrôle (Suivre le mur à une distance de `d` mètres)

Voir: https://www.youtube.com/watch?v=qIpiqhO3ITY

Instructions: https://github.com/f1tenth/f1tenth_lab3_template

Solution (en ROS avec C++): https://github.com/vaul-ulaval/wall_following_node/blob/main/src/wall_follow_node.cpp 