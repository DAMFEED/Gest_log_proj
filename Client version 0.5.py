import requests
from inquirer import prompt, List
from inquirer.themes import GreenPassion
import getpass
import json

BASE_URL = 'http://10.78.5.95:5000'

def envoyer_logs(mdp, logs):
    """Envoi des logs au serveur"""
    url = f'{BASE_URL}/upload'
    data = {'logs': logs, 'mdp': mdp}
    response = requests.post(url, json=data)

    if response.status_code == 200:
        print("Envoi effectué avec succès")
    elif response.status_code == 401:
        print("Mot de passe incorrect")
    else:
        print("Erreur inconnue. Veuillez réessayer ultérieurement.")


def recuperer_logs(mdp, ip):
    """Récupération des logs filtrés par IP"""
    url = f'{BASE_URL}/renvoyer'
    data = {'ip': ip, 'mdp': mdp}
    response = requests.post(url, json=data)

    if response.status_code == 200:
        server_response = response.json()
        logs = server_response.get('logs', [])
        print("Logs demandés :")
        for log in logs:
            print(log)
    elif response.status_code == 401:
        print("Mot de passe incorrect")
    else:
        print("Erreur lors de la récupération des logs.")


def recuperer_tout_les_logs(mdpa):
    """Récupération de tous les logs pour les administrateurs"""
    url = f'{BASE_URL}/renvoyer_tout_les_logs'
    data = {'mdp': mdpa}
    response = requests.post(url, json=data)

    if response.status_code == 200:
        server_response = response.json()
        logs = server_response.get('logs', [])
        print("Tous les logs :")
        for log in logs:
            print(log)
    elif response.status_code == 401:
        print("Mot de passe incorrect")
    else:
        print("Erreur lors de la récupération des logs.")


def sous_menu_logs():
    """Menu pour envoyer des logs"""
    questions = [List('Que faire',
                      message="Quel type de logs voulez-vous envoyer ?",
                      choices=['Logs sudo', 'Logs SSH', 'Retour au menu principal'],
                      )]

    exit_menu = False

    while not exit_menu:
        choix = prompt(questions, theme=GreenPassion())['Que faire']

        if choix == 'Logs sudo':
            mdp = getpass.getpass("Mot de passe : ")
            logs = [
                {"IP": "10.78.0.2", "Date": "2025-08-17", "Niveau de sévérité": 4},
                {"IP": "10.79.0.2", "Date": "2025-08-17", "Niveau de sévérité": 4},
                {"IP": "10.78.0.2", "Date": "2025-08-18", "Niveau de sévérité": 3}
            ]
            envoyer_logs(mdp, logs)

        elif choix == 'Logs SSH':
            mdp = getpass.getpass("Mot de passe : ")
            logs = [
                {"IP": "10.78.0.2", "Date": "2025-08-17", "Niveau de sévérité": 4},
                {"IP": "10.79.0.2", "Date": "2025-08-17", "Niveau de sévérité": 4},
                {"IP": "10.78.0.2", "Date": "2025-08-18", "Niveau de sévérité": 3}
            ]
            envoyer_logs(mdp, logs)

        elif choix == 'Retour au menu principal':
            exit_menu = True


def sous_menu_logs2():
    """Menu pour récupérer des logs"""
    questions = [List('Que faire',
                      message="Quel logs voulez-vous voir ?",
                      choices=['Mes logs', 'Tout les logs de tous les postes (Administrateur)', 'Retour au menu principal'],
                      )]

    exit_menu = False

    while not exit_menu:
        choix = prompt(questions, theme=GreenPassion())['Que faire']

        if choix == 'Mes logs':
            mdp = getpass.getpass("Mot de passe : ")
            ip = input("IP du Poste : ")
            recuperer_logs(mdp, ip)

        elif choix == 'Tout les logs de tous les postes (Administrateur)':
            mdpa = getpass.getpass("Mot de passe administrateur : ")
            recuperer_tout_les_logs(mdpa)

        elif choix == 'Retour au menu principal':
            exit_menu = True


def menu():
    """Menu principal pour l'utilisateur"""
    questions = [List('Que faire',
                      message="Que voulez-vous faire ?",
                      choices=['Envoyer logs', 'Récupérer logs', 'Quitter'],
                      )]

    exit_app = False

    while not exit_app:
        reponse = prompt(questions, theme=GreenPassion())['Que faire']

        if reponse == 'Envoyer logs':
            sous_menu_logs()

        if reponse == 'Récupérer logs':
            sous_menu_logs2()

        if reponse == 'Quitter':
            print("Au revoir")
            exit_app = True


if __name__ == '__main__':
    menu()
