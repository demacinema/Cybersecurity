# Spyder - Plano de Desenvolvimento

## Objetivo
Baixar todas as imagens de um website recursivamente.

---

## STEP 1: ✅ Parsing de Argumentos
**Status:** DONE

### O que fazer:
- Processar argumentos da linha de comando
- URL (obrigatório, posicional)
- `-r` (flag, ativa modo recursivo)
- `-l [N]` (nível máximo de profundidade, padrão 5)
- `-p [PATH]` (caminho para salvar imagens, padrão ./data/)

### Funções principais:
- `argparse.ArgumentParser()`
- `.add_argument()`
- `.parse_args()`

---

## STEP 2: ✅ Fetch Page (Baixar HTML)
**Status:** DONE

### O que fazer:
- Fazer requisição HTTP para uma URL
- Retornar conteúdo HTML como string

### Funções principais:
- `urllib.request.urlopen(url, timeout=5)`
- `response.read()` (retorna bytes)
- `content.decode('utf-8')` (converte para string)

---

## STEP 3: 🔄 Extrair URLs de Imagens do HTML
**Status:** TODO

### O que fazer:
- Parsear o HTML da página
- Encontrar todas as tags `<img>`
- Extrair atributo `src` de cada tag
- Retornar lista de URLs de imagens

### Funções principais:
- `html.parser.HTMLParser`
- Subclass com método `handle_starttag()`

---

## STEP 4: 🔄 Validar Extensões de Imagens
**Status:** TODO

### O que fazer:
- Verificar se URL termina em `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`
- Filtrar apenas URLs válidas

---

## STEP 5: 🔄 Converter URLs Relativas em Absolutas
**Status:** TODO

### O que fazer:
- Receber URL relativa
- Receber URL base da página
- Converter para URL absoluta

### Funções principais:
- `urllib.parse.urljoin(base_url, relative_url)`

---

## STEP 6: 🔄 Download de uma Imagem
**Status:** TODO

### O que fazer:
- Fazer requisição HTTP
- Salvar conteúdo em arquivo (modo binário 'wb')

---

## STEP 7: 🔄 Criar Diretório Automaticamente
**Status:** TODO

### O que fazer:
- Verificar se diretório existe
- Se não, criar com `pathlib.Path.mkdir(parents=True, exist_ok=True)`

---

## STEP 8: 🔄 Modo Não-Recursivo
**Status:** TODO

### O que fazer:
- Se `-r` não fornecido: baixar apenas imagens da URL inicial
- Fluxo: Fetch → Extrair → Validar → Converter URLs → Download

---

## STEP 9: 🔄 Modo Recursivo com Depth
**Status:** TODO

### O que fazer:
- Se `-r` fornecido: seguir links recursivamente
- Parar na profundidade máxima (`-l`)
- Evitar URLs duplicadas (visited set)

---

## STEP 10: 🔄 Integrar Tudo (Main)
**Status:** TODO

### O que fazer:
- Chamar tudo na ordem correta
- Mostrar progresso
- Exibir quantas imagens foram baixadas

---