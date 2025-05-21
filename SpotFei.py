import os

import os

def limpar_terminal():
    os.system("cls") 


# Arquivos usados para armazenar informações
arquivo_usuarios = "usuarios.txt"
arquivo_musicas = "musicas.txt"
arquivo_historico = "historico.txt"

def inicializar_banco_de_musicas():
    #Cria um arquivo de músicas com uma lista fixa, caso ainda não exista
    if not os.path.exists(arquivo_musicas): #Se existir, Não precisa recirar o aqruivo
        lista_fixa_de_faixas = [
            "Proibida Pra Mim;Charlie Brown Jr.;Transpiração Contínua Prolongada;0;0",
            "Zóio de Lula;Charlie Brown Jr.;Imunidade Musical;0;0",
            "Hoje Eu Acordei Feliz;Charlie Brown Jr.;Transpiração Contínua Prolongada;0;0",
            "Tudo que Ela Gosta;Charlie Brown Jr.;Preço Curto... Prazo Longo;0;0",
            "Céu Azul;Charlie Brown Jr.;Preço Curto... Prazo Longo;0;0",
            "Só os Mortos;Charlie Brown Jr.;Imunidade Musical;0;0",
            "Não Deixe o Mundo Me Derrubar;Charlie Brown Jr.;Transpiração Contínua Prolongada;0;0",
            "Meu Novo Mundo;Charlie Brown Jr.;Nadando com os Tubarões;0;0",
            "Confisco;Charlie Brown Jr.;Imunidade Musical;0;0",
            "Me Encontra;Charlie Brown Jr.;Nadando com os Tubarões;0;0"
        ]
        with open(arquivo_musicas, "w", encoding="utf-8") as arquivo:
            for faixa in lista_fixa_de_faixas: #Escrevei as muscas no arquivo
                arquivo.write(faixa + "\n")

def carregar_musicas():
    #Le as músicas do arquivo e retorna uma lista
    inicializar_banco_de_musicas()
    biblioteca_de_musicas = []
    with open(arquivo_musicas, "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            partes = linha.strip().split(";")
            if len(partes) == 5:
                biblioteca_de_musicas.append({
                    "titulo": partes[0],
                    "artista": partes[1],
                    "album": partes[2],
                    "curtidas": int(partes[3]),
                    "descurtidas": int(partes[4])
                })
    return biblioteca_de_musicas

def buscar_musica(palavra_chave):
    #Busca músicas pelo nome
    return [musica for musica in carregar_musicas() if palavra_chave.lower() in musica["titulo"].lower()]

def atualizar_curtidas(titulo_da_musica, acao):
    #Atualiza a contagem de curtidas e descurtidas de uma música
    lista_de_musicas = carregar_musicas()
    for musica in lista_de_musicas:
        if musica["titulo"].lower() == titulo_da_musica.lower():
            if acao == "curtir":
                musica["curtidas"] += 1
            elif acao == "descurtir":
                musica["descurtidas"] += 1
            salvar_musicas(lista_de_musicas)
            return
    print("Música não encontrada.")

def salvar_musicas(musicas):
    #Grava as músicas atualizadas no arquivo
    with open(arquivo_musicas, "w", encoding="utf-8") as arquivo:
        for musica in musicas:
            arquivo.write(f"{musica['titulo']};{musica['artista']};{musica['album']};{musica['curtidas']};{musica['descurtidas']}\n")

def registrar_historico(usuario, acao, musica):
    #Registra uma ação no histórico do usuário
    with open(arquivo_historico, "a", encoding="utf-8") as arquivo:
        arquivo.write(f"{usuario};{acao};{musica}\n")

def visualizar_historico(usuario):
    """Exibe as ações do usuário registradas no histórico."""
    if not os.path.exists(arquivo_historico):
        print("Nenhum histórico disponível.")
        return
    with open(arquivo_historico, "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            partes = linha.strip().split(";")
            if len(partes) == 3 and partes[0] == usuario:
                print(f"Ação: {partes[1]}, Música: {partes[2]}")

def menu_principal(usuario):
    #Exibe o menu de opções para o usuário
    while True:
        print("\n--- Spotifei ---")
        print("1 - Buscar Música")
        print("2 - Ver Histórico")
        print("3 - Sair")
        escolha = input("> ")

        if escolha == "1":
            termo_busca = input("Digite o nome da música: ")
            resultados = buscar_musica(termo_busca)
            if resultados:
                for indice, musica in enumerate(resultados, 1):
                    print(f"{indice}. {musica['titulo']} - {musica['artista']} ({musica['album']}) | 👍 {musica['curtidas']} 👎 {musica['descurtidas']}")
                escolha_musica = input("Escolha o número da música ou pressione Enter para voltar: ")
                if escolha_musica.isdigit():
                    indice_escolhido = int(escolha_musica) - 1
                    if 0 <= indice_escolhido < len(resultados):
                        musica_selecionada = resultados[indice_escolhido]
                        acao_usuario = input("Digite 'curtir' ou 'descurtir': ")
                        if acao_usuario in ["curtir", "descurtir"]:
                            atualizar_curtidas(musica_selecionada["titulo"], acao_usuario)
                            registrar_historico(usuario, acao_usuario, musica_selecionada["titulo"])
                        else:
                            print("Ação inválida.")
            else:
                print("Nenhuma música encontrada.")
        elif escolha == "2":
            visualizar_historico(usuario)
        elif escolha == "3":
            print("Saindo...")
            break
        else:
            print("Opção inválida.")

# Iniciar o programa
usuario_logado = input("Digite seu nome de usuário: ")
menu_principal(usuario_logado)
