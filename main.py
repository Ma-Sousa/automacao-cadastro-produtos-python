import time
import os
import pyautogui
import pandas as pd

#==============================================================
#Projeto (estudo): Automação de cadastro de produtos via web
#Lê um CSV e preenche um formulário automaticamente.
#
#Observações: As coordenadas (x, y) dependem da sua tela.
#==============================================================

#===== CONFIGURAÇÕES =======
LINK = "https://dlp.hashtagtreinamentos.com/python/intensivao/login"

#Ajuste conforme sua tela (use o arquivo "pegar_posicao_mouse" para descobrir.)
POS_EMAIL = (705, 405)          # campo de e-mail no login
POS_CAMPO_CODIGO = (789,286)    # primeiro campo do formulário (código)

TEMPO_CARREGAR_PAGINA = 2
SCROLL_POS_ENVIO = 5000         # se ficar invertido, troque para -5000

# Coloque um número (ex:5) para testar. Use None para cadastrar todos
LIMITE_CADASTROS = 5
#===============================================================

pyautogui.PAUSE = 0.3
pyautogui.FAILSAFE = True


def abrir_chrome_e_acessar():
    """Abre o Chrome e acessa o link do sistema."""
    pyautogui.press("win")
    pyautogui.write("Google Chrome")
    pyautogui.press("enter")
    time.sleep(1)

    pyautogui.write(LINK)
    pyautogui.press("enter")
    time.sleep(TEMPO_CARREGAR_PAGINA)


def fazer_login(email: str, senha: str):
    """Realiza o login usando clique + digitação + TAB."""
    pyautogui.click(*POS_EMAIL)
    pyautogui.write(email)
    pyautogui.press("tab")
    pyautogui.write(senha)
    pyautogui.press("tab")
    pyautogui.press("enter")
    time.sleep(TEMPO_CARREGAR_PAGINA)


def cadastrar_produto(produto: dict):
    """Preenche o formulário com os dados de um produto e envia."""
    pyautogui.click(*POS_CAMPO_CODIGO)

    pyautogui.write(str(produto["codigo"])); pyautogui.press("tab")
    pyautogui.write(str(produto["marca"])); pyautogui.press("tab")
    pyautogui.write(str(produto["tipo"])); pyautogui.press("tab")
    pyautogui.write(str(produto["categoria"])); pyautogui.press("tab")
    pyautogui.write(str(produto["preco_unitario"])); pyautogui.press("tab")
    pyautogui.write(str(produto["custo"])); pyautogui.press("tab")

    obs = produto.get("obs")
    if not pd.isna(obs):
        pyautogui.write(str(obs))

    pyautogui.press("tab")
    pyautogui.press("enter")
    pyautogui.scroll(SCROLL_POS_ENVIO)


def carregar_produtos_csv() -> list[dict]:
    """Carregar o CSV que está na mesma pasta do script e retorna lista de produtos."""
    caminho_csv = os.path.join(os.path.dirname(__file__), "produtos.csv")
    print("Lendo CSV de:", caminho_csv)

    tabela = pd.read_csv(caminho_csv)
    produtos = tabela.to_dict(orient="records")

    if LIMITE_CADASTROS is not None:
        produtos = produtos[:LIMITE_CADASTROS]

    return produtos


def main():
    email = input("Email (ambiente de teste): ")
    senha = input("Senha (ambiente de teste): ")

    abrir_chrome_e_acessar()
    fazer_login(email, senha)

    produtos = carregar_produtos_csv()

    if not produtos:
        print("Nenhum produto encontrado no CSV.")
        return
    total = len(produtos)
    for i, produto in enumerate(produtos, start=1):
        print(f"[{i}/{total}] Cadastrando: {produto['codigo']} - {produto['marca']}")
        cadastrar_produto(produto)

    print(f"Cadastro finalizado! Total de produtos cadastrados:{total}")

if __name__ == "__main__":
    main()
                     