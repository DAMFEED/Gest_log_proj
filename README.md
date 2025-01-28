## **Comment mettre ses scripts sur GitHub**

### **Prérequis :**
* **Un compte GitHub:** Inscris-toi sur [https://github.com/](https://github.com/) si tu n'en as pas encore.
* **Git installé:** Télécharge et installe Git depuis [https://git-scm.com/](https://git-scm.com/).

### **Les étapes :**

1. **Créer un dépôt GitHub:**
   * Connecte-toi à ton compte GitHub.
   * Clique sur le bouton "New repository".
   * Donne un nom à ton dépôt, ajoute une description (optionnel) et choisis si tu veux qu'il soit public ou privé.
   * Clique sur "Create repository".

2. **Cloner le dépôt:**
   * Ouvre ton terminal ou invite de commandes.
   * Navigue jusqu'au répertoire où tu veux placer ton projet.
   * Exécute la commande suivante en remplaçant `<url_du_depot>` par l'URL de ton dépôt :
     ```bash
     git clone <url_du_depot>
     ```

3. **Ajouter tes scripts:**
   * Copie tes scripts dans le dossier que tu viens de cloner.

4. **Suivre les modifications:**
   * Dans ton terminal, à l'intérieur du dossier de ton projet :
     ```bash
     git add .
     ```
     Cela ajoute tous les nouveaux fichiers ou modifications à la liste des fichiers qui seront inclus dans ton prochain commit.

5. **Créer un commit:**
   * Enregistre tes modifications avec un message expliquant ce que tu as fait :
     ```bash
     git commit -m "Ton message ici"
     ```
     Par exemple :
     ```bash
     git commit -m "Ajout des scripts Python"
     ```

6. **Envoyer les modifications sur GitHub:**
   * Pour envoyer tes changements sur GitHub :
     ```bash
     git push -u origin main
     ```
     Remplace `main` par le nom de ta branche si elle est différente.

### **Mettre à jour ton dépôt local:**
* Pour récupérer les dernières modifications depuis GitHub :
  ```bash
  git pull origin main
  ```

### **Créer une nouvelle branche:**
* Pour travailler sur une nouvelle fonctionnalité sans affecter la branche principale :
  ```bash
  git checkout -b nom_de_ta_branche
  ```
* Pour revenir à la branche principale et fusionner tes changements :
  ```bash
  git checkout main
  git merge nom_de_ta_branche
  ```

### **Résoudre les conflits:**
* Si des modifications ont été faites en parallèle sur GitHub, tu pourrais rencontrer des conflits lors de la fusion.
  * Utilise `git status` pour identifier les fichiers en conflit.
  * Résous les conflits manuellement dans les fichiers concernés.
  * Ajoute les fichiers résolus : `git add .`
  * Fais un nouveau commit : `git commit -m "Résolution des conflits"`

### **Résumé des commandes:**
| Commande        | Description                                        |
|----------------|----------------------------------------------------|
| `git clone`     | Cloner un dépôt existant                             |
| `git add`       | Ajouter des fichiers au prochain commit             |
| `git commit`    | Créer un commit avec un message explicatif          |
| `git push`      | Envoyer les modifications sur GitHub                 |
| `git pull`      | Récupérer les dernières modifications depuis GitHub  |
| `git checkout`  | Changer de branche                                 |
| `git merge`     | Fusionner une branche avec une autre                 |
| `git status`     | Vérifier l'état de ton dépôt local                    |

**Avec ces étapes, tu peux facilement partager tes projets sur GitHub et collaborer avec d'autres développeurs !**

**Pour aller plus loin:**

* **GitHub Actions:** Automatiser des tâches comme la construction, les tests et le déploiement.
* **GitHub Pages:** Héberger des sites web statiques directement depuis ton dépôt.
* **GitHub Issues:** Suivre les problèmes et les demandes de fonctionnalités.

**Tu as d'autres questions ? N'hésite pas à demander !**

**[Image illustrative de GitHub avec les commandes]**

**Note:** Tu peux personnaliser ce Markdown en ajoutant des images, des liens vers la documentation officielle de GitHub, ou en créant des sections plus détaillées pour les concepts que tu souhaites approfondir. 

**Pour créer une image illustrative, tu peux utiliser des outils en ligne comme Draw.io ou des logiciels de création d'images comme Canva. Puis, tu peux l'héberger sur une plateforme comme Imgur et ajouter le lien à ton fichier Markdown en utilisant la syntaxe suivante :**

```markdown
![Image de GitHub](https://i.imgur.com/exemple.png)
```

**N'oublie pas d'adapter le lien de l'image à l'image que tu auras choisie.**

peut me 