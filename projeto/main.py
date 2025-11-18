import os 
import json
from datetime import datetime


#Arquivos json em variáveis
ARQUIVO_TAREFAS = 'tarefas.json'
ARQUIVO_HISTORICO = 'tarefas_arquivadas.json'

#Definir o tamanho das tabelas dentro do terminal 
SEP = " | " 
W_IDX = 5
W_COD = 5
W_TIT = 18 
W_DESC = 15 
W_PRI = 10
W_STAT = 10
W_ORI = 15
W_DATA = 20
W_TEMPO = 20

#Somar para saber o tamanho total
LARGURA_TOTAL = (W_IDX + W_COD + W_TIT + W_DESC + W_PRI + W_STAT + W_ORI + W_DATA + W_TEMPO + (8 * len(SEP)))

def limparTela():
    """
    Limpa a tela do console (terminal)
    Verifica se o SO é Windows ('nt') ou Linux/macOS
    
    Parâmetros: 
        Nenhum
    Retorno: 
        Nenhum
    """

    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def pausar():
    """
    Pausa o programa, aguarda o usuário pressionar Enter
    e depois limpa a tela
    
    Parâmetros: 
        Nenhum
    Retorno: 
        Nenhum
    """

    input("\nAperter Enter para continuar...")
    limparTela()

def cabecalho():
    """
    Imprime o cabeçalho visual padronizado do programa
    
    Parâmetros: 
        Nenhum
    Retorno: 
        Nenhum
    """
    titulo = "Gerenciamento da Tarefa Pessoal"
    autores = "Giulia Ayumi | Vinicius Oliveira"
        
    print("-" * LARGURA_TOTAL)
    print(f"{titulo.center(LARGURA_TOTAL, ' ')}")
    print(f"{autores.center(LARGURA_TOTAL, ' ')}")
    print("-" * LARGURA_TOTAL)

def carregar_dados(arquivo):
    """
    Carrega os dados de um arquivo JSON
    Se o arquivo não existir, ele o cria com uma lista vazia
    Também trata arquivos vazios ou corrompidos
    
    Parâmetros:
        arquivo (str): O nome do arquivo JSON para carregar
    
    Retorno:
        list: A lista de dados (tarefas) carregada, ou uma lista vazia se houver erro
    """

    print(f"Executando a função carregar_dados para {arquivo}")
    if not os.path.exists(arquivo):
        print(f"Arquivo {arquivo} não encontrado. Criando um novo...")
        salvar_dados(arquivo, [])
        return []
    
    try:
        with open(arquivo, 'r', encoding='utf-8') as f:
            dados = json.load(f)
            if not isinstance(dados, list):
                 print(f"Conteúdo de {arquivo} inválido. Iniciando com lista vazia.")
                 return []
            return dados
    except json.JSONDecodeError:
        print(f"Erro ao ler {arquivo}. O arquivo pode estar corrompido. Iniciando com lista vazia.")
        return []
    except IOError as e:
        print(f"Erro de I/O ao carregar {arquivo}: {e}")
        return []

def salvar_dados(arquivo, dados):
    """
    Salva a lista de dados (tarefas) em um arquivo JSON
    
    Parâmetros:
        arquivo (str): O nome do arquivo JSON onde salvar os dados
        dados (list): A lista de dados (tarefas) a ser salva
    
    Retorno:
        Nenhum
    """

    print(f"Executando a função salvar_dados para {arquivo}")
    try:
        with open(arquivo, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
    except IOError as e:
        print(f"Erro ao salvar o arquivo {arquivo}: {e}")



def cadastro():
    """
    Coleta dados da tarefa do usuário como: (código, titulo,
    descrição, prioridade, status, origem e data). Além disso 
    usamos funções para gerar o código e ver se o nome
    está correto
    
    Parâmetros:
        Nenhum
    
    Retorno:
        Nenhum
    """

    cabecalho()
    print("Executando função - Cadastro\n")
    global tarefas

    print("Gerando código para a tarefa")
    codigo = gerarCod()
    pausar()
    cabecalho()
    print("Executando função - Cadastro\n")
    titulo = verificarTarefa()
    print(f"Código da tarefa '{titulo.title()}': {codigo}")
    pausar()

    cabecalho()
    print("Executando função - Cadastro\n")
    print(f"Digite a Descrição para '{titulo.title()}' (Opcional, aperte Enter para pular):")
    descricao = input("Descrição: ").strip()
    pausar()
    
    while True:
        cabecalho()
        print("Executando função - Cadastro\n")
        print(f"Qual o nível de prioridade da tarefa '{titulo}'")
        print("1 - URGENTE")
        print("2 - ALTA")
        print("3 - MÉDIA")
        print("4 - BAIXA")

        try:
            prioridade = input("Número da resposta: ").strip()
            prioridades = {"1": "URGENTE", "2": "ALTA", "3": "MÉDIA", "4": "BAIXA"}
            if prioridade not in prioridades:
                raise ValueError("Opção Inválida")
            prioridade = prioridades[prioridade]
            break

        except ValueError as e:
            print(e)
            pausar()
            continue
    pausar()

    status = "PENDENTE"

    while True:
        cabecalho()
        print("Executando função - Cadastro\n")
        print(f"Qual a origem da tarefa '{titulo}'")
        print("1 - E-MAIL")
        print("2 - TELEFONE")
        print("3 - CHAMADO DO SISTEMA")
        try: 
            origem = input("Número da resposta: ").strip()
            origens = {"1": "E-MAIL", "2": "TELEFONE", "3": "CHAMADA DO SISTEMA"}
            if origem not in origens:
                raise ValueError("Opção Inválida")
            origem = origens[origem]
            break

        except ValueError as e:
            print(e)
            pausar()
            continue
    os.system('cls')

    data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print(f"Data de criação: {data}")
    
    print(f"\nTarefa '{titulo.title()}' cadastrada com sucesso")

    tarefa = {
        "Código": codigo,
        "Titulo": titulo,
        "Descrição":descricao,
        "Prioridade": prioridade,
        "Status": status,
        "Origem": origem,
        "Data": data,
        "dataConclusao": None
    }

    tarefas.append(tarefa)
    return

def tabelaVisualizar():
    """
    Exibe o relatório principal de tarefas ativas (da lista global 'tarefas')
    As tarefas são ordenadas por prioridade
    
    Para tarefas com status 'CONCLUÍDA', chama a função 'calcularTempo' 
    para exibir o tempo total de execução
    
    Parâmetros:
        Nenhum
        
    Retorno:
        Nenhum
    """

    cabecalho()
    print("Executando função - Relatório\n")
    if not tarefas:
        print("Nenhuma tarefa cadastrada.")
        return
    ordem_status = {
        "FAZENDO": 1,
        "PENDENTE": 2,
        "CONCLUÍDA": 3
    }
    ordem_prioridade = {
        "URGENTE": 1,
        "ALTA": 2, 
        "MÉDIA": 3, 
        "BAIXA": 4
    }
    tarefas_ordenadas = sorted(tarefas, key=lambda x: 
                               (ordem_status.get(x.get("Status", "PENDENTE"), 99), 
                                ordem_prioridade.get(x.get("Prioridade"), 5)))
    
    print(f"{'Índice':<{W_IDX}}{SEP}"
          f"{'Código':<{W_COD}}{SEP}"
          f"{'Tarefa':<{W_TIT}}{SEP}"
          f"{'Descricao':<{W_DESC}}{SEP}"
          f"{'Prioridade':<{W_PRI}}{SEP}"
          f"{'Status':<{W_STAT}}{SEP}"
          f"{'Origem':<{W_ORI}}{SEP}"
          f"{'Data Criação':<{W_DATA}}{SEP}"
          f"{'Tempo Exec.':<{W_TEMPO}}")
    
    print("-" * LARGURA_TOTAL)


    for i, tarefa in enumerate(tarefas_ordenadas, start=1):
    
        titulo = tarefa.get('Titulo', 'N/A').title()
        descricao = tarefa.get('Descrição', 'N/A') 
        prioridade = tarefa.get('Prioridade', 'N/A')
        status = tarefa.get('Status', 'N/A')
        origem = tarefa.get('Origem', 'N/A')
        dataCriacao = tarefa.get('Data', 'N/A') 

        tempoExec = "---" 
        if status == "CONCLUÍDA":
            tempoExec = calcularTempo(dataCriacao, tarefa.get('dataConclusao'))
        
        print(f"{str(i):<{W_IDX}.{W_IDX}}{SEP}"
              f"{tarefa['Código']:<{W_COD}.{W_COD}}{SEP}"
              f"{titulo:<{W_TIT}.{W_TIT}}{SEP}"
              f"{descricao:<{W_DESC}.{W_DESC}}{SEP}"
              f"{prioridade:<{W_PRI}.{W_PRI}}{SEP}"
              f"{status:<{W_STAT}.{W_STAT}}{SEP}"
              f"{origem:<{W_ORI}.{W_ORI}}{SEP}"
              f"{dataCriacao:<{W_DATA}.{W_DATA}}{SEP}"
              f"{tempoExec:<{W_TEMPO}.{W_TEMPO}}")
    
    print("-" * LARGURA_TOTAL)

def atualizar():
    """
    Permite o usuário selecionar uma tarefa pelo código e
    alterar seu nível de prioridade 
    
    A função busca na lista global 'tarefas' pelo código informado
    Se encontrar, solicita a nova prioridade e valida a entrada
    
    Parâmetros:
        Nenhum
        
    Retorno:
        Nenhum
    """

    global tarefas
    cabecalho()
    print("Executando função - Atualizar tarefa\n")
    tarefamod = input("Qual o código da tarefa que será modificada: ")

    for tarefa in tarefas:
        if tarefa['Código'] == tarefamod:
            while True:
                cabecalho() 
                print(f"Modificando a tarefa: '{tarefa['Titulo'].title()}' (Prioridade atual: {tarefa['Prioridade']})")
                print("1 - URGENTE")
                print("2 - ALTA")
                print("3 - MÉDIA")
                print("4 - BAIXA")

                try:
                    novaprioridade = input(f"Qual a nova prioridade da tarefa? ").strip()
                    prioridades = {"1": "URGENTE", "2": "ALTA", "3": "MÉDIA", "4": "BAIXA"}

                    if novaprioridade not in prioridades:
                        raise ValueError("Opção inválida.")
                    
                    tarefa['Prioridade'] = prioridades[novaprioridade] 
                    print(f"\nNova prioridade da tarefa '{tarefa['Titulo'].title()}': {tarefa['Prioridade']}") 
                    return
                
                except ValueError as e:
                    print(e)
                    pausar()
                    continue 
    else: 
        print("Tarefa não encontrada")
    
def verificarUrgencia():
    """
    Verifica a tarefa pendente de maior prioridade
    
    Primeiro, checa se já existe alguma tarefa com status "FAZENDO"
    Se não houver, procura a primeira tarefa "PENDENTE" seguindo a
    ordem de prioridade (URGENTE > ALTA > MÉDIA > BAIXA)
    
    Se encontrar uma, atualiza seu status para "FAZENDO"
    
    Parâmetros:
        Nenhum
        
    Retorno:
        A tarefa que foi colocada em andamento (status atualizado)
        Se nenhuma tarefa foi iniciada (ou por já ter uma "FAZENDO"
              ou por não haver tarefas pendentes)
    """

    cabecalho()
    print("Executando função - Verificar urgencia da tarefa\n")
    if not tarefas:
        print("Não há tarefas cadastradas")
        return None
    
    for t in tarefas:
        if t["Status"] == "FAZENDO":
            print(f"Já existe uma tarefa em andamento: '{t['Titulo'].title()}' (cód: {t['Código']})\n")
            return
    
    ordem_prioridade = ["URGENTE", "ALTA", "MÉDIA", "BAIXA"]
    
    for prioridade in ordem_prioridade:
        for tarefa in tarefas:
            if tarefa["Prioridade"] == prioridade and tarefa["Status"] == "PENDENTE":
                tarefa["Status"] = "FAZENDO"
                print(f"Tarefa '{tarefa['Titulo'].title()}' (cód: {tarefa['Código']}) agora está em andamento")
                return tarefa
    
    else:
        print("Não há tarefas pendentes")
        return None

def concluir():
    """
    Permite ao usuário selecionar uma tarefa pelo código
    e marcá-la como "CONCLUÍDA" 
    
    A função registra a data e hora exatas da conclusão
    no campo 'dataConclusao' da tarefa.
    
    Parâmetros:
        Nenhum
        
    Retorno:
        Nenhum
    """

    global tarefas
    cabecalho()
    print("Executando função - Concluir tarefa\n")
    tarefaconclu = input("Código da tarefa concluída: ")

    for tarefa in tarefas:
        if tarefa['Código'] == tarefaconclu:
            tarefa["dataConclusao"]  = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            tarefa["Status"] = 'CONCLUÍDA'
            print(f"Tarefa '{tarefa['Titulo'].title()}' concluída na data {tarefa['dataConclusao']}")
            return
    else:
        print("Tarefa não encontrada")

def excluirTarefa():
    """
    Realiza a "exclusão lógica" de uma tarefa
    
    A função encontra a tarefa pelo código e altera seu status
    para "EXCLUÍDA". A tarefa não é removida da lista 'tarefas'
    imediatamente, ela será movida para o histórico pela função 'arquivamento'.
    
    Parâmetros:
        Nenhum
        
    Retorno:
        Nenhum
    """

    print("Executando função - Excluir tarefa\n")
    global tarefas

    tarefaExcluir = input("Digite o código da tarefa que deseja excluir: ")
    encontrou = False

    for tarefa in tarefas:
        if tarefa['Código'] == tarefaExcluir:
            tarefa["Status"] = "EXCLUÍDA"
            print(f"Tarefa '{tarefa['Titulo'].title()}' marcada como 'EXCLUÍDA'.")
            print("Ela será movida para o arquivo morto na próxima limpeza.")
            encontrou = True
            break
    
    if encontrou:
        salvar_dados(ARQUIVO_TAREFAS, tarefas)
    else:
        print("Tarefa não encontrada")

def arquivamento():
    """    
    Verifica a lista global 'tarefas' e move tarefas para a lista
    global 'tarefasArquivadas' se:
    1. O status for "EXCLUÍDA" 
    2. O status for "CONCLUÍDA" há mais de 7 dias 
    
    Ao final, salva ambos os arquivos JSON (tarefas e histórico).
    
    Parâmetros:
        Nenhum
        
    Retorno:
        Nenhum
    """

    print("Executando função - Limpar e Arquivar tarefas\n")
    global tarefas
    global tarefasArquivadas

    dataAtual = datetime.now()
    tarefasAtivas = []
    tarefasMover = []
    tarefasMovidas = 0

    for tarefa in tarefas:
        mover = False

        if tarefa.get("Status") == "EXCLUÍDA":
            mover = True

        elif tarefa.get("Status") == "CONCLUÍDA":
            try:
                data_conclusao = datetime.strptime(tarefa["dataConclusao"], "%d/%m/%Y %H:%M:%S")
                if (dataAtual - data_conclusao).days >= 7:
                    tarefa["Status"] = "ARQUIVADO" 
                    mover = True
            except (ValueError, KeyError, TypeError):
                print(f"Aviso: Tarefa '{tarefa.get('Titulo')}' CONCLUÍDA mas sem Data de Conclusão válida.")
                pass
        
        if mover:
            tarefasMover.append(tarefa)
            tarefasMovidas += 1
        else:
            tarefasAtivas.append(tarefa)
        
    if tarefasMovidas > 0:
        tarefas = tarefasAtivas
        tarefasArquivadas.extend(tarefasMover)

        salvar_dados(ARQUIVO_TAREFAS, tarefas)
        salvar_dados(ARQUIVO_HISTORICO, tarefasArquivadas)
        
        print(f"{tarefasMovidas} tarefa(s) foram movidas para o arquivo de histórico.")
    else:
        print("Nenhuma tarefa para arquivar no momento.")

def relatorioArquivamento():
    """
    Exibe um relatório de todas as tarefas do histórico ('tarefasArquivadas'),
    EXCETO aquelas com status "EXCLUÍDA"
    
    Parâmetros:
        Nenhum
        
    Retorno:
        Nenhum
    """

    cabecalho()
    print("Executando função - Relatório de Arquivadas\n")

    if not tarefasArquivadas:
        print(f"Nenhuma tarefa foi arquivada ainda.")
        return

    tarefasNaoExcluidas = []
    for t in tarefasArquivadas:
        if t.get('Status') != 'EXCLUÍDA':
            tarefasNaoExcluidas.append(t)

    if not tarefasNaoExcluidas:
        print(f"Nenhuma tarefa arquivada foi encontrada.")
        return

    print(f"{'Índice':<{W_IDX}}{SEP}"
          f"{'Código':<{W_COD}}{SEP}"
          f"{'Tarefa':<{W_TIT}}{SEP}"
          f"{'Descrição':<{W_DESC}}{SEP}"
          f"{'Prioridade':<{W_PRI}}{SEP}"
          f"{'Status':<{W_STAT}}{SEP}"
          f"{'Origem':<{W_ORI}}{SEP}"
          f"{'Data Criação':<{W_DATA}}{SEP}"
          f"{'Tempo Exec.':<{W_TEMPO}}")
    
    print("-" * LARGURA_TOTAL)

    for i, tarefa in enumerate(tarefasNaoExcluidas, start=1):
        titulo = tarefa.get('Titulo', 'N/A').title()
        descricao = tarefa.get('Descrição', 'N/A')
        prioridade = tarefa.get('Prioridade', 'N/A')
        status = tarefa.get('Status', 'N/A')
        origem = tarefa.get('Origem', 'N/A')
        dataCriacao = tarefa.get('Data', 'N/A')
        dataConclusao = tarefa.get('dataConclusao') 

        tempoExec = "---" 
        if status == "CONCLUÍDA" or status == "ARQUIVADO":
             tempoExec = calcularTempo(dataCriacao, dataConclusao)
        
        print(f"{str(i):<{W_IDX}.{W_IDX}}{SEP}"
              f"{tarefa.get('Código', 'N/A'):<{W_COD}.{W_COD}}{SEP}"
              f"{titulo:<{W_TIT}.{W_TIT}}{SEP}"
              f"{descricao:<{W_DESC}.{W_DESC}}{SEP}"
              f"{prioridade:<{W_PRI}.{W_PRI}}{SEP}"
              f"{status:<{W_STAT}.{W_STAT}}{SEP}"
              f"{origem:<{W_ORI}.{W_ORI}}{SEP}"
              f"{dataCriacao:<{W_DATA}.{W_DATA}}{SEP}"
              f"{tempoExec:<{W_TEMPO}.{W_TEMPO}}")
    
    print("-" * LARGURA_TOTAL)




def gerarCod():
    """
    Gera um novo código de tarefa único
    
    Acessa o 'contadorId' global, incrementa em 1, e formata
    o novo número como uma string de 3 dígitos
    
    Parâmetros:
        Nenhum
        
    Retorno:
        O novo código de tarefa formatado.
    """

    global contadorId
    contadorId += 1 
    return str(contadorId).zfill(3)

def verificarTarefa():
    """
    Solicita e valida o título de uma nova tarefa 
    A função entra em loop até que o usuário digite um título que:
    1. Não esteja vazio (após remover espaços em branco).
    2. Contenha apenas letras e espaços (sem números ou símbolos).
    
    Parâmetros:
        Nenhum
        
    Retorno:
        str: O título da tarefa validado.
    """

    while True: 
        titulo = input("Digite a tarefa: ")

        if not titulo.strip():
            cabecalho()
            print("Executando função - Cadastro\n")
            print("O título não pode estar vazio. Tente novamente.")
            pausar()
            continue 

        
        if titulo.replace(" ", "").isalpha():
            return titulo
        else: 
            cabecalho()
            print("Executando função - Cadastro\n")
            print("Título inválido. Digite apenas letras e espaços (sem números ou símbolos).")
            pausar()

def calcularTempo(dataInicioSTR, dataFinalSTR):
    """
    Calcula o tempo de execução entre duas datas
    Recebe duas datas como strings, tenta convertê-las para
    objetos datetime e calcula a diferença
    
    Parâmetros:
        dataInicioSTR (str): A data/hora de início no formato "%d/%m/%Y %H:%M:%S"
        dataFinalSTR (str): A data/hora de fim no formato "%d/%m/%Y %H:%M:%S"
        
    Retorno:
        O tempo de execução formatado ou
        "N/A" se as datas forem inválidas
    """

    try:
        formato = "%d/%m/%Y %H:%M:%S"
        dataInicio = datetime.strptime(dataInicioSTR, formato)
        dataFinal = datetime.strptime(dataFinalSTR, formato)

        tempo = dataFinal - dataInicio

        dias = tempo.days
        segundosTotais = tempo.seconds

        horas = segundosTotais // 3600
        minutos = (segundosTotais % 3600) // 60
        segundos = segundosTotais % 60

        if dias > 0:
            return f"{dias} dia(s), {horas:02}:{minutos:02}:{segundos:02}"
        else:
            return f"{horas:02}:{minutos:02}:{segundos:02}"
            
    except (ValueError, TypeError):
        return "N/A"


tarefas = carregar_dados(ARQUIVO_TAREFAS)
tarefasArquivadas = carregar_dados(ARQUIVO_HISTORICO)
contadorId = 0

bibliotecaCodTarefas = tarefas + tarefasArquivadas

#Verificar qual o maior código para a próxima tarefa ser +1
if bibliotecaCodTarefas:
    try:
        maiorId = int(max(bibliotecaCodTarefas, key=lambda x: int(x.get('Código', 0))).get('Código', 0))
        contadorId = maiorId
    except (ValueError, TypeError):
        contadorId = 0 
pausar()

while True: 
    cabecalho()
    #Lista de escolha do usuário
    print("1 - Cadastrar")
    print("2 - Visualizar tabela de tarefas")
    print("3 - Ver urgência de tarefa")
    print("4 - Atualizar tarefa") 
    print("5 - Concluir tarefa")
    print("6 - Arquivar tarefa")
    print("7 - Visualizar tabela de tarefas arquivadas")
    print("8 - Excluir tarefa")
    print("9 - Encerrar programa")

    escolha = input("\nEscolha o número do que deseja fazer: ")
    pausar()

    #De acordo com a escolha, o match direciona para a função correta
    match escolha:
        case "1":
            cadastro()
            salvar_dados(ARQUIVO_TAREFAS, tarefas)
        case "2":
            tabelaVisualizar()
        case "3":
            tarefaAndamento = verificarUrgencia()
            if tarefaAndamento:
                print("\nResumo da tarefa em andamento:")
                print(f"Código: {tarefaAndamento['Código']}")
                print(f"Título: {tarefaAndamento['Titulo'].title()}")
                print(f"Prioridade: {tarefaAndamento['Prioridade']}")
                print(f"Status: {tarefaAndamento['Status']}")
                salvar_dados(ARQUIVO_TAREFAS, tarefas)
        case "4":
            atualizar()
            salvar_dados(ARQUIVO_TAREFAS, tarefas)
        case "5": 
            concluir()
            salvar_dados(ARQUIVO_TAREFAS, tarefas)
        case "6":
            arquivamento()
        case "7":
            relatorioArquivamento()
        case "8":
            excluirTarefa()
        case "9":
            print("Salvando dados antes de sair...")
            salvar_dados(ARQUIVO_TAREFAS, tarefas)
            salvar_dados(ARQUIVO_HISTORICO, tarefasArquivadas)
            print("Programa encerrado.")
            exit()
        case _: 
            print("Opção inválida!")
    pausar()