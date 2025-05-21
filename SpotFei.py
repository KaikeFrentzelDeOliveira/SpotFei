import os

ARQ_USUARIOS = "usuarios.txt"
ARQ_MUSICAS = "musicas.txt"

def limpa():
    os.system()

# ======================= USUÁRIOS =======================
def lerUsuarios():
    users = {}
    if os.path.exists(ARQ_USUARIOS):
        with open(ARQ_USUARIOS, "r", encoding="utf-8") as f:
            for l in f:
                l = l.strip()
                if l:
                    p = l.split(";")
                    if len(p) >= 2:
                        users[p[0]] = p[1]
    return users

def gravarUsuarios(users):
    with open(ARQ_USUARIOS, "w", encoding="utf-8") as f:
        for u, s in users.items():
            f.write(f"{u};{s}\n")

def cadastro():
    limpa()
    users = lerUsuarios()
    print("----- Cadastro -----")
    nome = input("Usuário: ").strip()
    if nome in users:
        print("Usuário já existe!")
        input("ENTER para voltar...")
        return
    senha = input("Senha: ").strip()
    users[nome] = senha
    gravarUsuarios(users)
    print("Cadastro feito!")
    input("ENTER para continuar...")

def login():
    limpa()
    users = lerUsuarios()
    print("----- Login -----")
    nome = input("Usuário: ").strip()
    senha = input("Senha: ").strip()
    if nome in users and users[nome] == senha:
        print(f"Bem-vindo, {nome}!")
        input("ENTER...")
        return nome
    print("Dados incorretos!")
    input("ENTER...")
    return None

# ======================= MÚSICAS (Charlie Brown Jr.) =======================
def iniciaMusicas():
    if not os.path.exists(ARQ_MUSICAS):
        faixas = [
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
        with open(ARQ_MUSICAS, "w", encoding="utf-8") as f:
            for faixa in faixas:
                f.write(faixa+"\n")

def lerMusicas():
    iniciaMusicas()
    lista = []
    with open(ARQ_MUSICAS, "r", encoding="utf-8") as f:
        for l in f:
            l = l.strip()
            if l:
                p = l.split(";")
                if len(p) == 5:
                    lista.append({
                        "nome": p[0],
                        "artista": p[1],
                        "album": p[2],
                        "curtidas": int(p[3]),
                        "descurtidas": int(p[4])
                    })
    return lista

def gravarMusicas(musicas):
    with open(ARQ_MUSICAS, "w", encoding="utf-8") as f:
        for m in musicas:
            f.write(f"{m['nome']};{m['artista']};{m['album']};{m['curtidas']};{m['descurtidas']}\n")

def buscaMusica(termo):
    return [m for m in lerMusicas() if termo.lower() in m["nome"].lower()]

def atualizaContagem(faixa, acao):
    mus = lerMusicas()
    achou = False
    for m in mus:
        if m["nome"].lower() == faixa.lower():
            if acao == "curtir":
                m["curtidas"] += 1
            elif acao == "descurtir":
                m["descurtidas"] += 1
            achou = True
            break
    if achou:
        gravarMusicas(mus)
    else:
        print("Música não encontrada.")

# ======================= HISTÓRICO =======================
def lerHistorico(user):
    arq = f"historico_{user}.txt"
    hist = {"curtidas": [], "descurtidas": []}
    if os.path.exists(arq):
        with open(arq, "r", encoding="utf-8") as f:
            for l in f:
                l = l.strip()
                if l.startswith("curtidas:"):
                    c = l.replace("curtidas:", "").strip()
                    if c:
                        hist["curtidas"] = c.split(",")
                elif l.startswith("descurtidas:"):
                    c = l.replace("descurtidas:", "").strip()
                    if c:
                        hist["descurtidas"] = c.split(",")
    return hist

def gravarHistorico(user, hist):
    arq = f"historico_{user}.txt"
    with open(arq, "w", encoding="utf-8") as f:
        f.write("curtidas: " + ",".join(hist["curtidas"]) + "\n")
        f.write("descurtidas: " + ",".join(hist["descurtidas"]) + "\n")

def atualizaHist(user, faixa, acao):
    hist = lerHistorico(user)
    if acao == "curtir" and faixa not in hist["curtidas"]:
        hist["curtidas"].append(faixa)
    elif acao == "descurtir" and faixa not in hist["descurtidas"]:
        hist["descurtidas"].append(faixa)
    gravarHistorico(user, hist)

def mostraHistorico(user):
    hist = lerHistorico(user)
    limpa()
    print("----- Histórico -----")
    if not hist["curtidas"] and not hist["descurtidas"]:
        print("Nenhuma ação registrada.")
    else:
        print("Curtidas:")
        for m in hist["curtidas"]:
            print(" -", m)
        print("\nDescurtidas:")
        for m in hist["descurtidas"]:
            print(" -", m)
    input("\nENTER para voltar...")

# ======================= PLAYLISTS =======================
def lerPlaylists(user):
    arq = f"playlists_{user}.txt"
    listas = {}
    if os.path.exists(arq):
        with open(arq, "r", encoding="utf-8") as f:
            for l in f:
                l = l.strip()
                if l:
                    p = l.split(";")
                    if len(p) == 2:
                        listas[p[0]] = p[1].split(",") if p[1] else []
    return listas

def gravarPlaylists(user, listas):
    arq = f"playlists_{user}.txt"
    with open(arq, "w", encoding="utf-8") as f:
        for n, faixas in listas.items():
            f.write(f"{n};{','.join(faixas)}\n")

def criaPlaylist(user):
    listas = lerPlaylists(user)
    nome = input("Nome da nova playlist: ").strip()
    if nome in listas:
        print("Playlist já existe!")
    else:
        listas[nome] = []
        gravarPlaylists(user, listas)
        print("Playlist criada!")
    input("ENTER para continuar...")

def addPlaylist(user):
    listas = lerPlaylists(user)
    if not listas:
        print("Nenhuma playlist. Crie uma.")
        input("ENTER...")
        return
    print("Playlists:")
    for p in listas:
        print(" -", p)
    nomePl = input("Nome da playlist: ").strip()
    if nomePl not in listas:
        print("Playlist não encontrada!")
    else:
        faixa = input("Digite o nome exato da música a adicionar: ").strip()
        if faixa in listas[nomePl]:
            print("Música já na playlist!")
        else:
            listas[nomePl].append(faixa)
            gravarPlaylists(user, listas)
            print("Música adicionada!")
    input("ENTER para continuar...")

def remPlaylist(user):
    listas = lerPlaylists(user)
    if not listas:
        print("Nenhuma playlist.")
        input("ENTER...")
        return
    print("Playlists:")
    for p in listas:
        print(" -", p)
    nomePl = input("Nome da playlist: ").strip()
    if nomePl not in listas:
        print("Playlist não encontrada!")
    else:
        faixa = input("Digite o nome exato da música a remover: ").strip()
        if faixa in listas[nomePl]:
            listas[nomePl].remove(faixa)
            gravarPlaylists(user, listas)
            print("Música removida!")
        else:
            print("Música não encontrada na playlist!")
    input("ENTER para continuar...")

def mostraPlaylists(user):
    listas = lerPlaylists(user)
    limpa()
    print("----- Suas Playlists -----")
    if not listas:
        print("Nenhuma playlist encontrada.")
    else:
        for n, faixas in listas.items():
            print("Playlist:", n)
            if faixas:
                for f in faixas:
                    print(" -", f)
            else:
                print("  (vazia)")
            print()
    input("ENTER para voltar...")

def gerenciaPlaylists(user):
    while True:
        limpa()
        print("----- Gerenciar Playlists -----")
        print("1 - Criar, 2 - Adicionar, 3 - Remover, 4 - Listar, 0 - Voltar")
        op = input("Opção: ").strip()
        if op == "1":
            criaPlaylist(user)
        elif op == "2":
            addPlaylist(user)
        elif op == "3":
            remPlaylist(user)
        elif op == "4":
            mostraPlaylists(user)
        elif op == "0":
            break
        else:
            print("Opção inválida!")
            input("ENTER para tentar...")

# ======================= MENU DO USUÁRIO =======================
def menuUsuario(user):
    while True:
        limpa()
        print(f"===== Bem-vindo, {user}! =====")
        print("1 - Buscar música  2 - Curtir  3 - Descurtir")
        print("4 - Ver histórico  5 - Gerenciar playlists")
        print("0 - Logout")
        esc = input("Opção: ").strip()
        if esc == "1":
            termo = input("Digite parte do nome: ").strip()
            res = buscaMusica(termo)
            limpa()
            if res:
                print("----- Resultados -----")
                for m in res:
                    print(f"{m['nome']} | {m['artista']} | {m['album']} | Curtidas: {m['curtidas']} | Descurtidas: {m['descurtidas']}")
            else:
                print("Nenhuma música encontrada.")
            input("\nENTER para voltar...")
        elif esc == "2":
            faixa = input("Nome exato para curtir: ").strip()
            atualizaContagem(faixa, "curtir")
            atualizaHist(user, faixa, "curtir")
            print("Música curtida!")
            input("ENTER...")
        elif esc == "3":
            faixa = input("Nome exato para descurtir: ").strip()
            atualizaContagem(faixa, "descurtir")
            atualizaHist(user, faixa, "descurtir")
            print("Música descurtida!")
            input("ENTER...")
        elif esc == "4":
            mostraHistorico(user)
        elif esc == "5":
            gerenciaPlaylists(user)
        elif esc == "0":
            print("Logout efetuado!")
            input("ENTER para voltar...")
            break
        else:
            print("Opção inválida!")
            input("ENTER para tentar...")

# ======================= MENU PRINCIPAL =======================
def main():
    while True:
        limpa()
        print("===== Spotifei =====")
        print("1 - Cadastrar  2 - Login")
        op = input("Sua opção: ").strip()
        if op == "1":
            cadastro()
        elif op == "2":
            user = login()
            if user:
                menuUsuario(user)
        else:
            print("Opção inválida!")
            input("ENTER para tentar...")

if __name__ == "__main__":
    main()
