import os, re, hashlib, json, sys, base64
from datetime import datetime
from getpass import getpass
from selenium import webdriver
from cryptography.fernet import Fernet
from termcolor import colored

ARQUIVO_DADOS = os.path.expanduser('~/.senhasegura/db.sqlite3')
ENDERECO_PLATAFORMA = 'http://localhost:8000/core'
ARQUIVO_REGISTRO = os.path.expanduser('~/.senhasegura/registro.xlsx')
ARQUIVO_PERFIL = os.path.expanduser('~/.senhasegura/profile.json')
ARQUIVO_MANAGE = os.path.expanduser('~/.senhasegura/manage.py')
VERSAO = '24.1.2'

def printAviso(texto):
    try:
        return input(colored(texto, 'white', 'on_blue', attrs=['bold']))
    except KeyboardInterrupt:
        limpar()
        sys.exit()

def inputSenha(parametro, texto):
    try:
        return str(getpass(colored(texto, 'black', 'on_white'))) if parametro != 'm' else str(input(colored(texto, 'black', 'on_white', attrs=['bold'])))
    except KeyboardInterrupt:
        limpar()
        sys.exit()

limpar = lambda: os.system('clear')
printTitulo = lambda: print(colored('SenhaSegura', 'white', 'on_blue', attrs=['bold']))
printAvisoCritico = lambda texto: print(colored(texto, 'black', 'on_yellow', attrs=['bold']))

def definirChave(entrada):
    chave = entrada.encode('ascii')
    while len(chave) < 32:
        chave += chave
    chave = chave[:32]
    chave64 = base64.urlsafe_b64encode(chave)
    return chave64

def criptografarArquivo(entrada):
    fernet = Fernet(entrada)
    with open(ARQUIVO_DADOS, 'rb') as arqA:
        dadosAbertos = arqA.read()
    dadosFechados = fernet.encrypt(dadosAbertos)
    with open(ARQUIVO_DADOS, 'wb') as arqF:
        arqF.write(dadosFechados)

def descriptografarArquivo(entrada):
    try:
        fernet = Fernet(entrada)
        with open(ARQUIVO_DADOS, 'rb') as arqF:
            dadosFechados = arqF.read()
        dadosAbertos = fernet.decrypt(dadosFechados)
        with open(ARQUIVO_DADOS, 'wb') as arqA:
            arqA.write(dadosAbertos)
    except:
        pass

def registrarEntrada(registrar, acesso):
    if registrar:
        escrever = datetime.now().strftime(f"%d/%m/%Y;%H:%M:%S;{acesso}\n")
    else:
        escrever = 'Data;Hora\n'
    with open(ARQUIVO_REGISTRO, "a") as arq:
        arq.write(escrever)
        
def deletarDados():
    printTitulo()
    os.system('rm -f db.sqlite3 profile.json >/dev/null')
    os.system(f'python3 {ARQUIVO_MANAGE} migrate >/dev/null')
    printAviso('Todas as senhas foram apagadas.')

def exportarDados(parametro):
    printTitulo()
    entrada = inputSenha(parametro, 'Digite sua senha: ')
    entradaHash = encriptarHash(entrada)
    hashPerfil = lerPerfil('principal')
    if entradaHash == hashPerfil:
        localArquivo = inputSenha('m', 'Digite o endereço para exportar o banco de dados: ')
        localArquivo = os.path.expanduser(localArquivo)
        chave = definirChave(entrada)
        descriptografarArquivo(chave)
        os.system(f'cp {ARQUIVO_DADOS} {localArquivo}')
        criptografarArquivo(chave)
        registrarEntrada(True, "Dados exportados.")
        printAvisoCritico(f'O arquivo exportado para \'{localArquivo}\' NÃO está criptografado.')
    else:
        printAviso('Senha incorreta.')

def mostrarAjuda():
    printTitulo()
    print('-a ou --ajuda ➜\nApresenta alguns parâmetros e funcionalidades, além do link para a documentação online da ferramenta.\n\n')
    print('-e ou --editar ➜\nInicia a função de editar a senha de entrada da ferramenta. É necessária a senha atual.\n\n')
    print('-h ou --historico ➜\nApresenta um breve histórico das últimas vezes que a ferramenta foi utilizada.\n\n')
    print('-m ou --mostrar ➜\nCom este parâmetro as senhas são visíveis ao inserir. Pode ser combinada com outros parâmetros de funções.\n\n')
    print('-p ou --panico ➜\nInicia a função de definir uma senha pânico. A senha pânico quando inserida deleta todo o banco de dados com as senhas salvas de modo permanente. É necessária a senha atual.\n\n')
    print(f'-v ou --versao ➜\nApresenta a versão instalada. ({VERSAO})\n\n')
    print('-x ou --exportar ➜\nInicia a função de exportação de banco de dados com as senhas salvas, mas este arquivo não é criptografado. É necessário a senha atual.\n\n')
    print('Documentação: http://127.0.0.1:8000/core/docs ou https://bill1300.github.io/senhasegura-docs/')
    input()

def mostrarVersao():
    printTitulo()
    print(f'Versão: {VERSAO}')

def mostrarHistorico():
    try:
        printTitulo()
        print('Data        |  Hora      |  Acesso')
        with open(ARQUIVO_REGISTRO, "r") as arquivo:
            contador_linha = 0
            for linha in arquivo:
                if contador_linha > 0:
                    linha_completa = linha.strip()
                    linha_completa = linha_completa.replace(";", "  |  ")
                    print(linha_completa)
                contador_linha += 1
    except FileNotFoundError:
        printAviso('Ainda não há registros.')

def encriptarHash(entrada):
    criptografia = hashlib.sha256()
    criptografia.update(entrada.encode('utf-8'))
    texto_criptografado = criptografia.hexdigest()
    return texto_criptografado

def gravarPerfil(hashEntrada, nomeEntrada):
    try:
        with open(ARQUIVO_PERFIL, "r") as arq:
            perfis = json.load(arq)
    except (FileNotFoundError, json.JSONDecodeError):
        perfis = []
    novo_perfil = {nomeEntrada: hashEntrada}
    perfis.append(novo_perfil)
    with open(ARQUIVO_PERFIL, "w") as arq:
        json.dump(perfis, arq, indent=2)

def lerPerfil(nome):
    try:
        with open(ARQUIVO_PERFIL, 'r') as arq:
            dados = json.load(arq)
            for perfil in dados:
                if nome in perfil:
                    return perfil[nome]
        return None
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def editarPerfil(parametro):

    def mudarPerfil(entrada):
        with open(ARQUIVO_PERFIL, 'r') as f:
            dados = json.load(f)
        for item in dados:
            if 'principal' in item:
                item['principal'] = entrada

        with open(ARQUIVO_PERFIL, 'w') as f:
            json.dump(dados, f, indent=2)
        limpar()
        registrarEntrada(True, "Senha alterada.")
        printAviso('Senha alterada.')

    def editarSenha():
        limpar()
        printTitulo()
        print('Redefina uma senha forte de entrada. Ela deve conter:\n- 12 dígitos\n- Números\n- Letras maiúsculas e minúsculas\n- Caracteres especiais\n')
        entrada1 = inputSenha(parametro, 'Digite a nova senha: ')
        if validar(entrada1):
            entrada2 = None
            while not entrada1 == entrada2:
                limpar()
                printTitulo()
                print('Redefina uma senha forte de entrada. Ela deve conter:\n- 12 dígitos\n- Números\n- Letras maiúsculas e minúsculas\n- Caracteres especiais\n\nDigite a senha:')
                entrada2 = inputSenha(parametro, 'Digite a nova senha novamente: ')
                if entrada1 == entrada2:
                    novoPerfil = encriptarHash(entrada1)
                    mudarPerfil(novoPerfil)
                else:
                    limpar()
                    printTitulo()
                    input('Redefina uma senha forte de entrada. Ela deve conter:\n- 12 dígitos\n- Números\n- Letras maiúsculas e minúsculas\n- Caracteres especiais\n\nDigite a senha:\nDigite a senha novamente:\n\nAs senhas não são iguais. Tente novamente.')
        printAviso('A senha não é forte.')
        editarSenha()

    limpar()
    printTitulo()
    entrada = inputSenha(parametro, 'Digite a senha: ')
    hashEntrada = encriptarHash(entrada)
    hashPerfil = lerPerfil('principal')
    if hashEntrada == hashPerfil:
        limpar()
        editarSenha()
    else:
        printAviso('Senha incorreta.')

def validar(entrada):
    dig = True if len(entrada) > 11 else False
    num = bool(re.search(r'\d', entrada))
    lma = bool(re.search(r'[A-Z]', entrada))
    lmi = bool(re.search(r'[a-z]', entrada))
    car = bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', entrada))
    return dig and num and lma and lmi and car

def abrirNavegador(entrada):

    def executarServidor(estado):
        printTitulo()
        if estado:
            limpar()
            print('Iniciando servidor')
            os.system(f'python3 {ARQUIVO_MANAGE} runserver &')
        else:
            print('Finalizando servidor')
            os.system('fuser -k 8000/tcp >/dev/null')
            limpar()

    params = {
        'scrollbars': 'yes',
        'resizable': 'no',
        'status': 'no',
        'location': 'no',
        'toolbar': 'no',
        'menubar': 'no',
        'width': 1200,
        'height': 1000,
        'left': 0,
        'top': 0
    }

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f'--window-position={params["left"]},{params["top"]}')
    chrome_options.add_argument(f'--window-size={params["width"]},{params["height"]}')
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    executarServidor(True)
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)
    driver.get(ENDERECO_PLATAFORMA)
    limpar()
    try:
        printAviso(f'SenhaSegura em execução em \'{ENDERECO_PLATAFORMA}\'. Utilize a tecla [ENTER] para sair da sessão.\n')
    except KeyboardInterrupt:
        executarServidor(False)
        descriptografarArquivo(entrada)

    executarServidor(False)
    driver.quit()

def abrirPlataforma(entrada):
    chave = definirChave(entrada)
    descriptografarArquivo(chave)
    abrirNavegador(chave)
    criptografarArquivo(chave)

def criarPanico(parametro):

    def salvarPanico(entradaPanico):
        entradaPanicoHash = encriptarHash(entradaPanico)
        gravarPerfil(entradaPanicoHash, 'panico')
        registrarEntrada(True, "Senha pânico salva.")
        printAviso('Senha pânico salva.')

    limpar()
    printTitulo()
    entrada = inputSenha(parametro, 'Digite a senha: ')
    hashEntrada = encriptarHash(entrada)
    hashPerfil = lerPerfil('principal')
    if hashEntrada == hashPerfil:
        entradaP1 = None
        while entradaP1 == entrada or entradaP1 is None:
            limpar()
            printTitulo()
            print('A senha pânico quando inserida deleta todo o banco de dados com as senhas salvas de modo permanente. Esta senha não pode ser editada.\n')
            print('Defina uma senha forte de pânico. Ela deve ser diferente da sua senha verdadeira e deve conter:\n- 12 dígitos\n- Números\n- Letras maiúsculas e minúsculas\n- Caracteres especiais\n')
            entradaP1 = inputSenha(parametro, 'Digite a senha pânico: ')
        if validar(entradaP1):
            entradaP2 = None
            while not entradaP1 == entradaP2:
                limpar()
                printTitulo()
                print('A senha pânico quando inserida deleta todo o banco de dados com as senhas salvas de modo permanente. Esta senha não pode ser editada.\n')
                print('Defina uma senha forte de pânico. Ela deve ser diferente da sua senha verdadeira e deve conter:\n- 12 dígitos\n- Números\n- Letras maiúsculas e minúsculas\n- Caracteres especiais\n\nDigite a senha pânico:')
                entradaP2 = inputSenha(parametro, 'Digite a senha pânico novamente: ')
                if entradaP1 == entradaP2:
                    salvarPanico(entradaP1)
    else:
        printAviso('Senha incorreta.')

def entrarSenhaSegura(parametro):

    def salvar(entrada):
        hashEntrada = encriptarHash(entrada)
        gravarPerfil(hashEntrada, 'principal')
        printAviso('Perfil salvo.')

    def criar():
        limpar()
        print('Defina uma senha forte de entrada. Ela deve conter:\n- 12 dígitos\n- Números\n- Letras maiúsculas e minúsculas\n- Caracteres especiais\n')
        entrada1 = inputSenha(parametro, 'Digite a senha: ')
        if validar(entrada1):
            entrada2 = None
            while not entrada1 == entrada2:
                limpar()
                print('Defina uma senha forte de entrada. Ela deve conter:\n- 12 dígitos\n- Números\n- Letras maiúsculas e minúsculas\n- Caracteres especiais\n\nDigite a senha:')
                entrada2 = inputSenha(parametro, 'Digite a senha novamente: ')
                if entrada1 == entrada2:
                    salvar(entrada1)
                    chave = definirChave(entrada1)
                    criptografarArquivo(chave)
                    registrarEntrada(False, None)
                else:
                    limpar()
                    input('Defina uma senha forte de entrada. Ela deve conter:\n- 12 dígitos\n- Números\n- Letras maiúsculas e minúsculas\n- Caracteres especiais\n\nDigite a senha:\nDigite a senha novamente:\n\nAs senhas não são iguais. Tente novamente.')
                    criar()

        else:
            criar()

    def entrar():
        entrada = inputSenha(parametro, 'Digite a senha: ')
        hashEntrada = encriptarHash(entrada)
        hashPerfil = lerPerfil('principal')
        hashPanico = lerPerfil('panico')
        limpar()
        if hashEntrada == hashPerfil:
            registrarEntrada(True, "Permitido.")
            abrirPlataforma(entrada)
        elif hashEntrada == hashPanico:
            deletarDados()
        else:
            registrarEntrada(True, "Negado. (Senha incorreta)")
            printAviso('Senha incorreta.')
    
    printTitulo()
    if os.path.exists(ARQUIVO_PERFIL):
        entrar()
    else:
        criar()  

def main():
    limpar()
    parametros = sys.argv[1:] if len(sys.argv) > 1 else []
    mostrar = '-m' in parametros or '--mostrar' in parametros
    panico = '-p' in parametros or '--panico' in parametros
    editar = '-e' in parametros or '--editar' in parametros
    ajudar = '-a' in parametros or '--ajuda' in parametros
    versao = '-v' in parametros or '--versao' in parametros
    exportar = '-x' in parametros or '--exportar' in parametros
    historico = '-h' in parametros or '--historico' in parametros
    if mostrar and panico:
        criarPanico('m')
    elif mostrar and editar:
        editarPerfil('m')
    elif mostrar and exportar:
        exportarDados('m')
    elif mostrar:
        entrarSenhaSegura('m')
    elif exportar:
        exportarDados(None)
    elif panico:
        criarPanico(None)
    elif ajudar:
        mostrarAjuda()
    elif versao:
        mostrarVersao()
    elif historico:
        mostrarHistorico()
    else:
        entrarSenhaSegura(None)

if __name__ == "__main__":
    main()