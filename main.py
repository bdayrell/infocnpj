"""
--------------------------------------------------------------------------------------------------------------------
Script para varredura automática de informações de empresas, dado uma lista de CNPJ

Input:  
        O arquivo de entrada precisa estar no formato csv. 
        Cada nova linha de entrada precisa ser um CNPJ válido
        O scrip pergunta pelo nome do arquivo de leitura, que deve ser informado como "nome.csv" (tirando as aspas)
        Os CNPJs devem conter 14 números, com ou sem alfanuméricos 12345678000190 ou 12.345.678/0001-90

Output: 
        A saída retornada é um arquivo csv com 1 empresa por linha, no formato:
        | CNPJ só numeros | CNAE principal | Atividade Principal |

Informações:
        Utilizamos a API pública receitasw.com.br/v1/cnpj
        esta api possui o limite de 3 requisições por minuto
        consideramos o delay de 30s para cada requisição. 
        este valor é empírico e hardcoded

Next:
        Loop de leitura de nome
        request inteligente com timeout dinamico
--------------------------------------------------------------------------------------------------------------------
"""

"""--------------------------------------------------------------------------------------------------------------------
        IMPORT MODULES 
--------------------------------------------------------------------------------------------------------------------"""
import requests     # para requisições HTTP
import json         # manipulação JSON dos parametros
import re           # modulo utilizado para validar os digitos do cnpj
import csv          # import e export do JSON, modulo já incluso na instalação (python 3.12)
import time         # utilizado para delay entre as requisições


"""--------------------------------------------------------------------------------------------------------------------
        GLOBAL VARIABLES
--------------------------------------------------------------------------------------------------------------------"""
FILENAME = ""

def get_filename():
    global FILENAME
    return FILENAME

def set_filename(name="input.csv"):
    global FILENAME
    FILENAME = name
"""
--------------------------------------------------------------------------------------------------------------------
        Consulta CNPJs 
--------------------------------------------------------------------------------------------------------------------

Faz a requisição em si, para cada cnpj válido
utiliza módulo request
retorna um JSON com as informações publicas da empresa fornecida
"""
def consulta_cnpj(cnpj):

    url = f"https://www.receitaws.com.br/v1/cnpj/{cnpj}"
    querystring = {"token":"XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX","cnpj":"06990590000123","plugin":"RF"}
    response = requests.request("GET", url, params=querystring)

    resp = json.loads(response.text)

    return resp

"""
--------------------------------------------------------------------------------------------------------------------
        Valida CNPJs 
--------------------------------------------------------------------------------------------------------------------

Faz a validação de cada cnpj, retornando somente numeros em forma de texto
Lembrando que a api requer somente numeros como input
"""
def valida_cnpj(cnpj):

    # Remove caracteres que não são números
    cnpj = re.sub(r'\D', '', cnpj)
        
    # Verifica se o CNPJ possui 14 dígitos
    if len(cnpj) != 14:
        return False
    
    # Verifica se todos os dígitos são iguais
    if cnpj == cnpj[0] * 14:
        return False
    
    # [TO-DO] Calcula os digitos verificadores

    return cnpj
    

"""
--------------------------------------------------------------------------------------------------------------------
        Salva em csv
--------------------------------------------------------------------------------------------------------------------
Salva o input como um csv no path especificado
"""
def salvar_to_csv(dicionario,cabecalho = ['chave','valor'], nome_arquivo = None):
    if not(nome_arquivo):
        nome_arquivo = f'results_{get_filename()}'
    print(f'nome arquivo = {nome_arquivo}')
    print(f'leitura = {get_filename()}')
    with open(nome_arquivo, 'w', newline='') as arquivo_csv:
        writer = csv.writer(arquivo_csv)
        writer.writerow(['cnpj']+cabecalho)  # Escreve o cabeçalho, com cnpj na primeira coluna

        for chave, valor in dicionario.items():
            row = [str(chave)]
            for key in cabecalho:
                row.append(valor.get(key,"NOT FOUND"))

            writer.writerow(row)

"""
results[cnpj] = {'nome_fantasia':nome_fantasia, 
        'cnae':cnae, 'atividade':desc,
        'cnpj_origin':cnpj_origin,
        'capital_social':money,
        'uf':uf,
        'municipio':municipio}
"""

def leitura_do_csv(nome_arquivo):
    rows = []
    with open(nome_arquivo, 'r') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            rows.append(row)
    return rows
"""
--------------------------------------------------------------------------------------------------------------------
        Leitura CNPJs 
--------------------------------------------------------------------------------------------------------------------

Faz a leitura manual do input (isso pode ser melhorado)
Tenta ler o arquivo
Retorna uma lista dos cnpjs já validados
"""
def leitura_cnpjs():

    # Leitura do csv 
    # O arquivo precisa ter o formato correto e possuir todos os cnpjs na primeira linha
    # há uma pequena lógica que valida o nome do arquivo e acrescenta automaticamente a extensão .csv
    nomearquivo = input(' nome  do arquivo << ')
    if nomearquivo == "":
        nomearquivo = 'inputexample.csv'
    elif not nomearquivo.endswith('.csv'):
        nomearquivo+= ".csv"
    list_cnpj =[]

    # Tenta ler o nome validado
    set_filename(nomearquivo) 
    try:
        rows = leitura_do_csv(nomearquivo)
    except:
        return list_cnpj             # Retorna lista vazia, caso haja erro
    #print(f'arquivo:{rows}')        # [DEBUG] imprime todos os inputs na tela (pode ser melhorado)
    

    # Valida os cnpjs e junta todos os válidos em uma lista
    # esta lista já está no formato correto de requisição
    for row in rows:
        strcnpj = valida_cnpj(row[0])
        if strcnpj:
            list_cnpj.append(strcnpj)
        else:
            # Exibe erro na tela
            print(f'row invalid ->{row[0]} type{type(row[0])}')
            continue

    return list_cnpj

"""
--------------------------------------------------------------------------------------------------------------------
        Main function
--------------------------------------------------------------------------------------------------------------------

Inicializa as variáveis,
realiza a leitura da entrada
Varre os cnpjs e faz as requisições (executado direto)
Salva os resultados no csv
"""
def main():
    # Inicialização --------------------------
    results = {}

    
    # Inputs  --------------------------------
    cnpjs = leitura_cnpjs()
    if len(cnpjs)==0:
        print(f'Lista de cnpjs inexistente ou vazia')
        return
    
    print(f'Verificando {len(cnpjs)} cnpjs')

    # Sweeping  ------------------------------
    firstcall = False
    for cnpj in cnpjs:
        # A ansiedade não deixa esperar 30s na primeira chamada a toa
        if not(firstcall):
            firstcall = True
        else:
            time.sleep(30)

        # Todos os cnpjs são exibidos com x ou v.
        # Se a consulta falhou, pula pra próxima interação
        try:
            a = consulta_cnpj(cnpj)
        except Exception as e:
            print(f"{cnpj}-x")
            print(f'  {e}')
            time.sleep(30)          # HARDCODED delay de 30s
            continue
        
        # Obtenção dos parâmetros aninhados
        cnae = a.get('atividade_principal')[0].get('code')
        desc = a.get('atividade_principal')[0].get('text')
        municipio = a.get('municipio')
        uf = a.get('uf')
        nome_fantasia = a.get('fantasia')
        cnpj_origin = a.get('cnpj')
        money = a.get('capital_social')


        
        # Resultado é uma dict de dicts, com a chave principal sendo o cnpj numerico
        results[cnpj] = {'nome_fantasia':nome_fantasia, 
                         'cnae':cnae, 
                         'atividade':desc,
                         'cnpj_origin':cnpj_origin,
                         'capital_social':money,
                         'uf':uf,
                         'municipio':municipio}
        print(f"{cnpj}-v")
        
    # Saving  --------------------------------
    salvar_to_csv(results,['nome_fantasia','cnae','atividade','cnpj_origin','capital_social','uf','municipio'])


# Handler que identifica que o código foi executado como standalone, não chamado por outro
if __name__ == '__main__':
    main()