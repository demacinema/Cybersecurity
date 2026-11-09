#!/usr/bin/env python3
"""Spider - Download images from websites recursively"""

import sys # Para manipular saída e encerrar o programa em caso de erro
import argparse # Para processar argumentos da linha de comando
from urllib.request import urlopen # Para fazer requisições HTTP
from urllib.error import URLError # Para tratar erros de requisição HTTP

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


def fetch_page(url):
    """
    Download a página HTML de uma URL
    
    Args:
        url (str): URL para baixar
    
    Returns:
        str: Conteúdo HTML da página, ou None se erro
    """
    try:
        # Faz a requisição HTTP
        response = urlopen(url, timeout=5)
        
        # Lê o conteúdo
        content = response.read()
        
        # Converte de bytes para texto
        html = content.decode('utf-8')
        
        return html
        
    except URLError as e:
        print(f"Erro ao baixar {url}: {e}")
        return None
    except Exception as e:
        print(f"Erro: {e}")
        return None

def main():

    args = parse_arguments()
    print(f"URL: {args.url}")
    print(f"Recursive: {args.r}")
    print(f"Level: {args.l}")
    print(f"Path: {args.p}")

    # Testa baixar a página
    html = fetch_page(args.url)
    
    if html:
        print(f"✓ Página baixada! Primeiros 200 caracteres:")
        print(html[:20000])
    else:
        print("✗ Falha ao baixar página")


if __name__ == '__main__':
    main()

