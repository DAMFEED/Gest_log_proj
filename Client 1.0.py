import requests
from inquirer import prompt, List
from inquirer.themes import GreenPassion
import getpass
import json

BASE_URL = 'http://10.78.5.95:5000'  # URL de base pour les requêtes API

def envoyer_logs(mdp, logs):
    """Envoi des logs au serveur"""
    url = f'{BASE_URL}/upload/{mdp}/{json.dumps(logs)}'  # Passer le mot de passe directement dans l'URL
    response = requests.get(url)  # Envoi de la requête GET avec les logs au serveur

    if response.status_code == 200:
        print("Envoi effectué avec succès")  # Si la requête réussit, affichage du message de succès

    elif response.status_code == 401:
        print("Mot de passe incorrect")  # Si le mot de passe est incorrect, affichage du message d'erreur

    else:
        print("Erreur inconnue. Veuillez réessayer ultérieurement.")  # Autres erreurs inconnues


def recuperer_logs(mdp, ip):
    """Récupération des logs filtrés par IP"""
    url = f'{BASE_URL}/renvoyer/{mdp}/{ip}'  # Passer le mot de passe et l'IP dans l'URL
    response = requests.get(url)  # Envoi de la requête GET pour récupérer les logs de l'IP donnée

    if response.status_code == 200:
        server_response = response.json()  # Conversion de la réponse en JSON
        logs = server_response.get('logs', [])  # Récupération des logs
        print("Logs demandés :")
        for log in logs:
            print(log)  # Affichage des logs récupérés

    elif response.status_code == 401:
        print("Mot de passe incorrect")  # Si le mot de passe est incorrect

    else:
        print("Erreur lors de la récupération des logs.")  # Si une autre erreur survient


def recuperer_tout_les_logs(mdpa):
    """Récupération de tous les logs pour les administrateurs"""
    url = f'{BASE_URL}/renvoyer_tout_les_logs/{mdpa}'  # Passer le mot de passe administrateur dans l'URL
    response = requests.get(url)  # Envoi de la requête GET pour récupérer tous les logs

    if response.status_code == 200:
        server_response = response.json()  # Conversion de la réponse en JSON
        logs = server_response.get('logs', [])  # Récupération des logs
        print("Tous les logs :")
        for log in logs:
            print(log)  # Affichage des logs récupérés

    elif response.status_code == 401:
        print("Mot de passe incorrect")  # Si le mot de passe est incorrect

    else:
        print("Erreur lors de la récupération des logs.")  # Si une autre erreur survient


def sous_menu_logs():
    """Menu pour envoyer des logs"""
    questions = [List('Que faire',
                      message="Quel type de logs voulez-vous envoyer ?",
                      choices=['Logs sudo', 'Logs SSH', 'Retour au menu principal'],
                      )]

    exit_menu = False

    while not exit_menu:
        choix = prompt(questions, theme=GreenPassion())['Que faire']  # Affichage du menu et choix de l'utilisateur

        if choix == 'Logs sudo':
            mdp = getpass.getpass("Mot de passe : ")  # Demander le mot de passe
            logs = [
                {"IP": "10.78.0.2", "Date": "2025-08-17", "Niveau de sévérité": 4},
                {"IP": "10.79.0.2", "Date": "2025-08-17", "Niveau de sévérité": 4},
                {"IP": "10.78.0.2", "Date": "2025-08-18", "Niveau de sévérité": 3}
            ]
            envoyer_logs(mdp, logs)  # Envoi des logs via la fonction envoyer_logs

        elif choix == 'Logs SSH':
            mdp = getpass.getpass("Mot de passe : ")  # Demander le mot de passe
            logs = [
                {"IP": "10.78.0.2", "Date": "2025-08-17", "Niveau de sévérité": 4},
                {"IP": "10.79.0.2", "Date": "2025-08-17", "Niveau de sévérité": 4},
                {"IP": "10.78.0.2", "Date": "2025-08-18", "Niveau de sévérité": 3}
            ]
            envoyer_logs(mdp, logs)  # Envoi des logs via la fonction envoyer_logs

        elif choix == 'Retour au menu principal':
            exit_menu = True  # Quitter le sous-menu et revenir au menu principal


def sous_menu_logs2():
    """Menu pour récupérer des logs"""
    questions = [List('Que faire',
                      message="Quel logs voulez-vous voir ?",
                      choices=['Mes logs', 'Tout les logs de tous les postes (Administrateur)', 'Retour au menu principal'],
                      )]

    exit_menu = False

    while not exit_menu:
        choix = prompt(questions, theme=GreenPassion())['Que faire']  # Affichage du menu et choix de l'utilisateur

        if choix == 'Mes logs':
            mdp = getpass.getpass("Mot de passe : ")  # Demander le mot de passe
            ip = input("IP du Poste : ")  # Demander l'IP du poste
            recuperer_logs(mdp, ip)  # Récupérer les logs via la fonction recuperer_logs

        elif choix == 'Tout les logs de tous les postes (Administrateur)':
            mdpa = getpass.getpass("Mot de passe administrateur : ")  # Demander le mot de passe administrateur
            recuperer_tout_les_logs(mdpa)  # Récupérer tous les logs via la fonction recuperer_tout_les_logs

        elif choix == 'Retour au menu principal':
            exit_menu = True  # Quitter le sous-menu et revenir au menu principal


def menu():
    """Menu principal pour l'utilisateur"""
    questions = [List('Que faire',
                      message="Que voulez-vous faire ?",
                      choices=['Envoyer logs', 'Récupérer logs', 'Quitter'],
                      )]

    exit_app = False

    while not exit_app:
        reponse = prompt(questions, theme=GreenPassion())['Que faire']  # Affichage du menu principal et choix de l'utilisateur

        if reponse == 'Envoyer logs':
            sous_menu_logs()  # Lancer le sous-menu pour envoyer des logs

        if reponse == 'Récupérer logs':
            sous_menu_logs2()  # Lancer le sous-menu pour récupérer des logs

        if reponse == 'Quitter':
            print("Au revoir")  # Quitter l'application
            exit_app = True


if __name__ == '__main__':
    menu()  # Lancer le menu principal