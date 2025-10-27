# chatbot_completo.py
import csv
import difflib
import re
from unidecode import unidecode

def carregar_respostas(arquivo):
    respostas = {}
    
    with open(arquivo, 'r', encoding='utf-8') as n:
        leitor = csv.DictReader(n)
        
        for linha in leitor:
            pergunta = linha['pergunta'].strip().lower() 
            resposta = linha['resposta'].strip()
            respostas[pergunta] = resposta
        print("Base de conhecimento carregada:", respostas)
    return respostas

def detectar_intencao(mensagem):
    """Detecta a intenção da mensagem usando regex"""
    mensagem_limpa = unidecode(mensagem.lower().strip())
    
    # Padrões regex para detectar intenções
    padroes = {
        'saudacao': [
            r'^o+i+!*$',                    # oi, oii, oiii, oi!
            r'^o+l+a+!*$',                  # ola, olaa, ola!
            r'^(e+\s*)?a+e+!*$',           # ae, e ae, e aeee!
            r'^o+p+a+!*$',                  # opa, opaa
            r'^f+a+l+a+!*$',                # fala, falaa
            r'^(hey|hello|hi)+!*$',         # hey, hello, hi
            r'^iai+!*$',                    # iai, iaii
            r'^[bs]om\s*dia!*$',           # bom dia, bom dia!
            r'^[bs]oa\s*tarde!*$',         # boa tarde
            r'^[bs]oa\s*noite!*$'          # boa noite
        ],
        'despedida': [
            r'^t+c+h+a+u+!*$',              # tchau, tchauu
            r'^a+t+[ée]\s*(l[oó]g[o0]|m[aá]is|j[aá])!*$', # ate logo, ate mais, ate ja
            r'^f+l+w+!*$',                  # flw, flww
            r'^(bye|goodbye)+!*$',          # bye, goodbye
            r'^v+a+l+e+u+!*$'               # valeu, valeeu
        ],
        'nome': [
            r'.*[qk]ual\s*[ée]\s*seu\s*nome.*',
            r'.*[ck]omo\s*vo[cc][ea]\s*se\s*chama.*',
            r'.*seu\s*nome.*',
            r'.*nome.*vo[cc][ea].*'
        ],
        'tudo_bem': [
            r'.*tudo\s*[bc]em.*',
            r'.*como\s*vo[cc][ea]\s*esta.*',
            r'.*como\s*vo[cc][ea]\s*t[aá].*',
            r'^[bc]e?le?za+!*$'             # blz, beleza, belezaa
        ]
    }
    
    # Verifica cada categoria
    for intencao, lista_padroes in padroes.items():
        for padrao in lista_padroes:
            if re.search(padrao, mensagem_limpa, re.IGNORECASE):
                return intencao
    
    return "outro"

def responder(mensagem, respostas):
    # Primeiro tenta detectar a intenção com regex
    intencao = detectar_intencao(mensagem)
    
    # Mapeia a intenção para a resposta correspondente
    mapeamento_respostas = {
        'saudacao': respostas.get('oi', 'Olá! Tudo bem?'),
        'despedida': respostas.get('tchau', 'Até logo! Volte sempre!'),
        'nome': respostas.get('qual e o seu nome', 'Eu sou um chatbot feito em Python!'),
        'tudo_bem': respostas.get('tudo bem', 'Que bom! Como posso te ajudar?')
    }
    
    # Se encontrou uma intenção conhecida, retorna a resposta correspondente
    if intencao in mapeamento_respostas:
        return mapeamento_respostas[intencao]
    
    # Se não encontrou por regex, usa o sistema antigo de similaridade
    mensagem_limpa = unidecode(mensagem.lower().strip())
    perguntas = list(respostas.keys())
    
    # Busca exata
    if mensagem_limpa in perguntas:
        return respostas[mensagem_limpa]
    
    # Busca por similaridade
    parecidas = difflib.get_close_matches(mensagem_limpa, perguntas, n=1, cutoff=0.6)
    
    if parecidas:
        return respostas[parecidas[0]]
    else:
        return "Desculpe, não entendi o que você quis dizer."

# Código principal
if __name__ == "__main__":
    # Carrega as respostas do arquivo CSV
    respostas = carregar_respostas("iniciacao.csv")
    
    print("ChatBot: Olá! Digite 'sair' para encerrar.\n")
    
    while True:
        usuario = input("Você: ")
        if usuario.lower() == "sair":
            print("ChatBot: Até mais!")
            break
        print("ChatBot:", responder(usuario, respostas))