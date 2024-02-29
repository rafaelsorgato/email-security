import os
from bs4 import BeautifulSoup

def alterar_href_src_para_static(html_file):
    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    # Verifica se já existe '{% load static %}' no arquivo
    load_static_exists = False
    for line in soup.prettify().split('\n'):
        if '{% load static %}' in line:
            load_static_exists = True
            break

    if not load_static_exists:
        # Adiciona '{% load static %}' no início do arquivo
        soup.insert(0, "{% load static %}")

    for tag in soup.find_all(['link', 'script', 'img'], src=True):
        src = tag['src']
        if not src.startswith('http'):
            if not tag.get('static_added'):
                tag['src'] = "{% static '" + src + "' %}"
                tag['static_added'] = True
    
    for tag in soup.find_all('link', href=True):
        href = tag['href']
        if not href.startswith('http'):
            if not tag.get('static_added'):
                tag['href'] = "{% static '" + href + "' %}"
                tag['static_added'] = True
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(str(soup))

def processar_pasta():
    pasta_script = os.path.dirname(os.path.abspath(__file__))
    for file in os.listdir(pasta_script):
        if file.endswith('.html'):
            alterar_href_src_para_static(os.path.join(pasta_script, file))

# Exemplo de uso:
processar_pasta()
