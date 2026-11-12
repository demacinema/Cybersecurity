# Scorpion - Plano de Desenvolvimento

## Objetivo
Ler arquivos de imagem e extrair metadados (EXIF e outros), exibindo no terminal.

---

## STEP 1: 🔄 Parsing de Argumentos
**Status:** TODO

### O que fazer:
- Processar argumentos da linha de comando
- Receber um ou mais arquivos de imagem (posicionais)
- Validar se pelo menos 1 arquivo foi informado

### Funções principais:
- `argparse.ArgumentParser()`
- `.add_argument()`
- `.parse_args()`

---

## STEP 2: 🔄 Validar Arquivos de Entrada
**Status:** TODO

### O que fazer:
- Verificar se cada caminho existe
- Verificar se é arquivo (não diretório)
- Tratar erro de permissão/leitura

### Funções principais:
- `pathlib.Path.exists()`
- `pathlib.Path.is_file()`
- `pathlib.Path.suffix`

---

## STEP 3: 🔄 Validar Extensões Suportadas
**Status:** TODO

### O que fazer:
- Aceitar apenas:
  - `.jpg` / `.jpeg`
  - `.png`
  - `.gif`
  - `.bmp`
- Ignorar ou reportar arquivos inválidos

---

## STEP 4: 🔄 Abrir Imagem com Segurança
**Status:** TODO

### O que fazer:
- Abrir cada imagem sem quebrar o programa inteiro
- Tratar imagens corrompidas
- Continuar processamento dos próximos arquivos

### Funções principais:
- `PIL.Image.open()`
- `try/except`

---

## STEP 5: 🔄 Extrair Metadados EXIF
**Status:** TODO

### O que fazer:
- Ler EXIF quando disponível
- Converter IDs EXIF para nomes legíveis
- Organizar pares chave/valor

### Funções principais:
- `image.getexif()`
- `PIL.ExifTags.TAGS`

---

## STEP 6: 🔄 Extrair Metadados Básicos do Arquivo
**Status:** TODO

### O que fazer:
- Coletar dados básicos:
  - nome do arquivo
  - caminho
  - tamanho em bytes
  - data de criação/modificação (se disponível)
  - formato da imagem
  - dimensões (width x height)
- Exibir mesmo quando não houver EXIF

### Funções principais:
- `pathlib.Path.stat()`
- `image.format`
- `image.size`

---

## STEP 7: 🔄 Formatar Saída no Terminal
**Status:** TODO

### O que fazer:
- Exibir resultados por arquivo de forma clara
- Separar “Metadados básicos” e “EXIF”
- Indicar quando EXIF não existir

---

## STEP 8: 🔄 Modo Multi-Arquivo
**Status:** TODO

### O que fazer:
- Processar `FILE1 [FILE2 ...]`
- Garantir que erro em um arquivo não interrompa os demais
- Exibir resumo final (processados, com erro, sem EXIF)

---

## STEP 9: 🔄 Tratamento de Erros e Códigos de Saída
**Status:** TODO

### O que fazer:
- Mensagens claras para:
  - arquivo inexistente
  - extensão não suportada
  - leitura inválida/corrompida
- Definir código de saída apropriado (`0` sucesso, `1` erro)

---

## STEP 10: 🔄 Integrar Tudo (Main)
**Status:** TODO

### O que fazer:
- Conectar todas as etapas no fluxo principal
- Estruturar em funções pequenas e reutilizáveis
- Preparar base para bônus (edição/remoção de metadados)