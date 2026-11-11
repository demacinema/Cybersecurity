#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Spider - Download images from websites recursively"""

import sys  # Para manipular saída e encerrar o programa em caso de erro
import argparse  # Para processar argumentos da linha de comando
import time  # Para fazer pausas entre requisições HTTP
from html.parser import HTMLParser  # Para processar HTML
from urllib.request import urlopen, Request  # Adicione Request
from urllib.error import URLError  # Para tratar erros de requisição HTTP
from urllib.parse import urlparse, urljoin  # Para manipular URLs
from pathlib import Path  # Para manipular caminhos de arquivos

VALID_IMG_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}


def parse_arguments():
    """Processa os argumentos da linha de comando"""

    parser = argparse.ArgumentParser()

    parser.add_argument('url')
    parser.add_argument('-r', action='store_true', dest='rec')
    parser.add_argument('-p', default='./data/', dest='path')

    # Pega tudo que não foi processado
    args, unknown = parser.parse_known_args()

    # Processa -l manualmente
    args.level = None  # padrão: sem limite

    # Valida argumentos desconhecidos (exceto -l)
    invalid_args = [
        arg for arg in unknown
        if arg != '-l' and not arg.lstrip('-').isdigit()]
    if invalid_args:
        print(f"Error: unrecognized arguments: {' '.join(invalid_args)}")
        sys.exit(1)

    # processa -l manualmente
    if '-l' in sys.argv:
        # Se não tem -r, erro
        if not args.rec:
            print("Error: -l only possible if has -r")
            sys.exit(1)

        # Se tem -l, processa o valor
        idx = sys.argv.index('-l')
        if idx + 1 < len(sys.argv) and sys.argv[idx + 1][0] != '-':
            try:
                args.level = int(sys.argv[idx + 1])
            except ValueError:
                args.level = 5
        else:
            args.level = 5

    return args


def fetch_page(url):
    try:
        time.sleep(1)

        req = Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0",
                "Accept":
                "text/html,application/xhtml+xml, \
                application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
            },
        )

        response = urlopen(req, timeout=5)  # use req, not url
        content = response.read()

        for enc in ("utf-8", "iso-8859-1", "windows-1252", "latin-1"):
            try:
                return content.decode(enc)
            except UnicodeDecodeError:
                pass

        return content.decode("utf-8", errors="ignore")

    except URLError as e:
        print(f"Erro ao baixar {url}: {e}")
        return None
    except Exception as e:
        print(f"Erro: {e}")
        return None


class ImageParser(HTMLParser):
    """Parser para extrair URLs de imagens de HTML"""

    def __init__(self):
        """Inicializa o parser e a lista de imagens"""
        super().__init__()
        self.images = []

    def handle_starttag(self, tag, attrs):
        """Chamado quando encontra uma tag de abertura"""
        # print(f"[DEBUG] start tag: {tag} | attrs: {attrs}")  # debug
        if tag == 'img':
            # attrs é uma lista de tuplas:
            # [('src', 'url'), ('alt', 'texto'), ...]
            for attr, value in attrs:
                if attr == 'src' and value:
                    # print(f"-->[DEBUG] img src encontrado: {value}")  # debug
                    self.images.append(value)


def extract_images(html):
    """Extrai URLs de imagens de um HTML
    Args: html (str): Conteúdo HTML da página
    Returns: list: Lista de URLs de imagens encontradas"""

    parser = ImageParser()
    parser.feed(html)
    parser.close()
    # print(f"****[DEBUG] LISTA FINAL: {parser.images}")  # debug
    return parser.images


def is_valid_image_url(image_url):
    """Return True if valid image extension."""

    if not image_url:
        return False
    if image_url.startswith('data:'):
        return False  # ignore base64 inline images for now

    path = urlparse(image_url).path.lower()
    return any(path.endswith(ext) for ext in VALID_IMG_EXTENSIONS)
    # return True if any extension matches ->

    # for ext in VALID_IMG_EXTENSIONS:
    # if path.endswith(ext):
    #     return True
    # return False


def filter_valid_image_urls(image_urls):
    """Keep only image URLs with validd extensions."""
    return [url for url in image_urls if is_valid_image_url(url)]
    # [ EXPRESSION for ITEM in ITERABLE if CONDITION ]
    # if is True, is included on the returned list ->

    # valid_urls = []
    # for url in image_urls:
    #     if is_valid_image_url(url):
    #         valid_urls.append(url)
    # return valid_urls


def convert_to_absolute_urls(base_url, image_urls):
    """Convert relative image URLs to absolute URLs."""

    absolute_urls = []
    for image_url in image_urls:
        if not image_url:
            continue
        absolute_urls.append(urljoin(base_url, image_url.strip()))
    return absolute_urls


def download_image(image_url, output_dir):
    """Download one image and save. Return saved path or None."""

    try:
        req = Request(
            image_url,
            headers={
                "User-Agent": "Mozilla/5.0",
                "Accept": "image/*,*/*;q=0.8",
            },
        )

        with urlopen(req, timeout=10) as response:
            content = response.read()

        filename = Path(urlparse(image_url).path).name
        if not filename:
            filename = f"image_{int(time.time() * 1000)}.bin"

        output_path = Path(output_dir) / filename

        with open(output_path, 'wb') as f:
            f.write(content)

        print(f"Downloaded: {image_url} -> {output_path}")
        return str(output_path)

    except URLError as e:
        print(f"Error downloading {image_url}: {e}")
        return None
    except Exception as e:
        print(f"Error saving {image_url}: {e}")
        return None


def main():
    """Função principal"""
    args = parse_arguments()

    # Testa args
    print(f"URL: {args.url}")
    print(f"Recursive: {args.rec}")
    print(f"Level: {args.level}")
    print(f"Path: {args.path}")
    print()

    # Testa baixar a página
    html = fetch_page(args.url)

    if not html:
        print("✗ Falha ao baixar página")
        sys.exit(1)  # Encerra antes de chamar extract_images()

    # print("[DEBUG] Página baixada! Primeiros 200 caracteres:\n")
    # print(html[:200]). # debug

    # Testa extrair imagens
    images = extract_images(html)
    valid_images = filter_valid_image_urls(images)
    absolute_images = convert_to_absolute_urls(args.url, valid_images)

    print(f"Encontradas {len(images)} imagem(s)\n")
    print(f"Validas: {len(valid_images)}\n")
    print(f"Absolutas: {len(absolute_images)}\n")

    # for img in images:
    # for img in valid_images:
    for img in absolute_images:
        print(f"  - {img}\n")

    downloaded = 0
    for img in absolute_images:
        print(".", end="", flush=True)  # heartbeat: shows progress
        if download_image(img, args.path):
            downloaded += 1

    print(f"Baixadas: {downloaded}\n")


if __name__ == '__main__':
    main()
