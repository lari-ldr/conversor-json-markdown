import json
import re
import os
from datetime import datetime


# Função para converter um timestamp do Google para uma data legível
def convert_timestamp(timestamp_usec):
    return datetime.fromtimestamp(int(timestamp_usec) / 1000000).strftime('%Y-%m-%d %H:%M:%S')


# Função para converter URLs do texto para o formato markdown
def convert_links(text):
    # Expressão regular para detectar URLs
    url_pattern = r'(https?://[^\s]+)'
    # Substitui cada URL pelo formato markdown de link
    return re.sub(url_pattern, r'[\g<0>](\g<0>)', text)


# Função para converter uma nota JSON do Google Keep para markdown
def json_to_markdown(note):
    md = ""

    # Título da nota (header em markdown)
    md += f"# {note.get('title', 'Sem Título')}\n\n"  # Usar 'Sem Título' se não houver título

    # Conteúdo da nota, preservando emoticons, quebras de linha e formatando links
    note_text = note.get('textContent', '').replace('\n', '\n\n')  # Substitui \n por quebras de linha
    note_text_with_links = convert_links(note_text)  # Formata links no texto
    md += f"{note_text_with_links}\n\n"

    # Adiciona conteúdo de lista de checkboxes, se presente
    list_content = note.get("listContent")
    if list_content:
        md += "## Checkboxes:\n"
        for item in list_content:
            item_text = item.get("text", "")
            is_checked = item.get("isChecked", False)
            checkbox = "[x]" if is_checked else "[ ]"
            md += f"- {checkbox} {item_text}\n"  # Lista de checkboxes

    # Adiciona labels se existirem
    if 'labels' in note and note['labels']:
        labels = [label['name'] for label in note['labels']]
        md += f"**Labels**: {', '.join(labels)}\n\n"

    # Adiciona informações de arquivamento e fixação (opcionais)
    md += f"**Pinned**: {'Yes' if note.get('isPinned', False) else 'No'}\n"
    md += f"**Archived**: {'Yes' if note.get('isArchived', False) else 'No'}\n\n"

    # Adiciona a data de criação e edição
    md += f"**Created**: {convert_timestamp(note.get('createdTimestampUsec', 0))}\n"
    md += f"**Last Edited**: {convert_timestamp(note.get('userEditedTimestampUsec', 0))}\n\n"

    # Linha divisória entre notas
    md += "---\n\n"

    return md


# Função para ler todos os arquivos JSON de um diretório e escrever em markdown
def convert_all_keep_json_to_markdown(json_dir, md_dir):
    # Certifica-se de que o diretório de saída existe
    os.makedirs(md_dir, exist_ok=True)

    # Itera sobre todos os arquivos no diretório de entrada
    for filename in os.listdir(json_dir):
        if filename.endswith('.json'):
            json_file_path = os.path.join(json_dir, filename)
            md_file_path = os.path.join(md_dir, f"{os.path.splitext(filename)[0]}.md")

            try:
                with open(json_file_path, 'r', encoding='utf-8') as f:
                    note = json.load(f)  # Lê o arquivo como um único objeto

                # Converte o JSON para markdown
                markdown_content = json_to_markdown(note)

                # Escreve o markdown em um arquivo
                with open(md_file_path, 'w', encoding='utf-8') as f:
                    f.write(markdown_content)

                print(f"Conversão concluída: {md_file_path}")

            except FileNotFoundError:
                print(f"Erro: Arquivo não encontrado - {json_file_path}")
            except json.JSONDecodeError:
                print(f"Erro: Falha ao decodificar JSON - {json_file_path}")
            except Exception as e:
                print(f"Erro ao converter o arquivo {json_file_path} para markdown: {e}")


# Caminhos dos diretórios de entrada e saída
json_dir = '/home/larissadantasrequena/Downloads/Google keep - backup mega feito/takeout-20241019T190618Z-001/Takeout/Keep/json'
md_dir = '/home/larissadantasrequena/Downloads/Google keep - backup mega feito/takeout-20241019T190618Z-001/Takeout/Keep/markdown'

# Realiza a conversão
convert_all_keep_json_to_markdown(json_dir, md_dir)
