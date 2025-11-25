from __future__ import annotations
import requests
from http import HTTPStatus
from rich.table import Table
from rich.console import Console 
from rich import print as p_print


console = Console()

tabela = Table(title="Menu de Opções", title_style="red", show_lines=True)

tabela.add_column("Código", style="cyan", justify="center")
tabela.add_column("Descrição da Opção", style="blue")

tabela.add_row("1", "Informações de perfil")
tabela.add_row("2", "Informações de atividade")


def get_github_user_info():
    while True:
        username = str(input('Digite seu usuario github:'))

        url = f"https://api.github.com/users/{username}/events"

        response = requests.get(url)

        if response.status_code == HTTPStatus.OK:
            events = response.json()
            
            p_print(tabela)
            console.file.flush() 
            
            info = int(input('Qual tipo de informação você deseja buscar?(Digite o número da opreção desejada): '))

            if info == 1:
                get_perfil_user_information(username)

            elif info == 2:
                for event in events:
                    if event['type'] == 'IssueCommentEvent':
                        p_print(f":fire: comentarios em issue: {event['payload']['issue']['number']}")
                    elif event['type'] == 'PushEvent':
                        p_print(f":fire: push para: {event['repo']['name']}")
                    elif event['type'] == 'IssuesEvent':
                        p_print(f':fire: issue criadas: {event["payload"]["issue"]["number"]}')
                    elif event['type'] == 'WatchEvent':
                        p_print(f':fire: Repositorio favoritos: {event["repo"]["name"]}')
                    elif event['type'] == 'PullRequestEvent':
                        p_print(f':fire: Pullrequest criadas: {event["payload"]["pull_request"]["number"]}')
                    elif event['type'] == 'PullRequestReviewEvent':
                        p_print(f':fire: solicitações de Pullrequest: {event["payload"]["pull_request"]["number"]}')
                    elif event['type'] == 'PullRequestReviewCommentEvent':
                        p_print(f':fire: comentarios em Pullrequest: {event["payload"]["pull_request"]["number"]}')
                    elif event['type'] == 'CreateEvent':
                        p_print(f':fire: criação de eventos {event["payload"]["ref_type"]} {event["payload"]["ref"]}')
                

                resposta = str(input('Deseja buscar outro usuário? s/n: ')).upper()

                if resposta != 'S':
                    break 
                    
        else:
            p_print(f'[bold red]❌ Erro[/bold red]: eventos não encontrados no usuário [bold magenta]{username}[/bold magenta]: [bold yellow]{response.status_code}[/bold yellow]')
            
            
def get_perfil_user_information(username):
    url = f'https://api.github.com/users/{username}'

    response = requests.get(url)

    if response.status_code == HTTPStatus.OK:
        user = response.json()

        p_print(f":bust_in_silhouette: Nome: {user.get('name')}")
        p_print(f":id: ID: {user.get('id')}")
        p_print(f":computer: Login: {user.get('login')}")
        p_print(f":earth_americas: Localização: {user.get('location')}")
        p_print(f":bookmark_tabs: Bio: {user.get('bio')}")
        p_print(f":smiley: Followers: {user.get('followers')}")
        p_print(f":star: Public Repos: {user.get('public_repos')}")
    else:
        p_print(":warning: Não foi possível carregar as informações de perfil")


if __name__ ==  '__main__':
    get_github_user_info()