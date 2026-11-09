#!/usr/bin/env python3
"""Spider - Download images from websites recursively"""

import sys # Para manipular saída e encerrar o programa em caso de erro
import argparse # Para processar argumentos da linha de comando
# from urllib.request import urlopen # Para fazer requisições HTTP
from urllib.error import URLError # Para tratar erros de requisição HTTP
from html.parser import HTMLParser # Para processar HTML
from urllib.request import urlopen, Request  # ← Adicione Request
import time

def parse_arguments():
    """Processa os argumentos da linha de comando"""
    parser = argparse.ArgumentParser()
    
    parser.add_argument('url')
    parser.add_argument('-r', action='store_true')
    parser.add_argument('-p', default='./data/')

    # Pega tudo que não foi processado
    args, unknown = parser.parse_known_args()
    
    # Processa -l manualmente
    args.l = None  # padrão: sem limite
    
    # Valida argumentos desconhecidos (exceto -l que será processado manualmente)
    invalid_args = [arg for arg in unknown if arg != '-l' and not arg.lstrip('-').isdigit()]
    if invalid_args:
        print(f"Error: unrecognized arguments: {' '.join(invalid_args)}")
        sys.exit(1)

    if '-l' in sys.argv:
        # Se não tem -r, erro
        if not args.r:
            print("Error: -l only possible if has -r")
            sys.exit(1)
        
        # Se tem -l, processa o valor
        idx = sys.argv.index('-l')
        if idx + 1 < len(sys.argv) and sys.argv[idx + 1][0] != '-':
            try:
                args.l = int(sys.argv[idx + 1])
            except ValueError:
                args.l = 5
        else:
            args.l = 5

    return args


# def fetch_page(url):
#     """
#     Download a página HTML de uma URL
    
#     Args:
#         url (str): URL para baixar
    
#     Returns:
#         str: Conteúdo HTML da página, ou None se erro
#     """
#     try:
#         # For Rate limiting - pequena pausa para passar o bloqueio de requisicoes muito rapidas
#         time.sleep(1)

#         # Cria uma requisição com User-Agent real e headers adicionais
#         req = Request(
#             url,
#             headers={
#                 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
#                 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#                 'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
#                 'Accept-Encoding': 'gzip, deflate',
#                 'DNT': '1',
#                 'Connection': 'keep-alive',
#                 'Upgrade-Insecure-Requests': '1'
#             }
#         )

#         # Faz a requisição HTTP
#         response = urlopen(url, timeout=5)
        
#         # Lê o conteúdo
#         content = response.read()
        
#         # Tenta diferentes encodings
#         for encoding in ['utf-8', 'iso-8859-1', 'windows-1252', 'latin-1']:
#             try:
#                 html = content.decode(encoding)
#                 return html
#             except (UnicodeDecodeError, AttributeError):
#                 continue
        
#         # Se nenhum encoding funcionou, ignora caracteres inválidos
#         html = content.decode('utf-8', errors='ignore')
#         return html
        
#     except URLError as e:
#         print(f"Erro ao baixar {url}: {e}")
#         return None
#     except Exception as e:
#         print(f"Erro: {e}")
#         return None

import requests
from urllib.error import URLError

def fetch_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    
    try:
        # For Rate limiting - pequena pausa para passar o bloqueio de requisicoes muito rapidas
        time.sleep(1)

        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()  # Levanta erro se HTTP error
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Erro ao baixar {url}: {e}")
        return None

class ImageParser(HTMLParser):
    """Parser para extrair URLs de imagens de HTML"""
    
    def __init__(self):
        super().__init__()
        self.images = []
    
    def handle_starttag(self, tag, attrs):
        """Chamado quando encontra uma tag de abertura"""
        if tag == 'img':
            # attrs é uma lista de tuplas: [('src', 'url'), ('alt', 'texto'), ...]
            for attr, value in attrs:
                if attr == 'src' and value:
                    self.images.append(value)


def extract_images(html):
    """
    Extrai URLs de imagens de um HTML
    
    Args:
        html (str): Conteúdo HTML da página
    
    Returns:
        list: Lista de URLs de imagens encontradas
    """
    parser = ImageParser()
    parser.feed(html)
    return parser.images



def main():

    args = parse_arguments()

    # # Testa args
    print(f"URL: {args.url}")
    print(f"Recursive: {args.r}")
    print(f"Level: {args.l}")
    print(f"Path: {args.p}")
    print()

    # Testa baixar a página
    html = fetch_page(args.url)
    
    # if html:
    #     print(f"✓ Página baixada! Primeiros 200 caracteres:")
    #     print(html[:20000])
    # else:
    #     print("✗ Falha ao baixar página")

    if not html:
        print("✗ Falha ao baixar página")
        sys.exit(1)  # Encerra antes de chamar extract_images()

    images = extract_images(html)
    print(f"Encontradas {len(images)} imagens")
    for img in images:
        print(f"  - {img}")


if __name__ == '__main__':
    main()
