import os
from bs4 import BeautifulSoup

def alterar_href_src_para_static(html_file):
    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
    
    for tag in soup.find_all(['link', 'script', 'img'], src=True):
        src = tag['src']
        if not src.startswith('http'):
            tag['src'] = "{% static '" + src + "' %}"
    
    for tag in soup.find_all('link', href=True):
        href = tag['href']
        if not href.startswith('http'):
            tag['href'] = "{% static '" + href + "' %}"
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write("{% load static %}\n" + str(soup))

def processar_pasta():
    pasta_script = os.path.dirname(os.path.abspath(__file__))
    for file in os.listdir(pasta_script):
        if file.endswith('.html'):
            alterar_href_src_para_static(os.path.join(pasta_script, file))

# Exemplo de uso:
processar_pasta()
