import os 
from datetime import datetime
import json

ARQUIVO_TAREFAS = 'tarefas.json'
ARQUIVO_HISTORICO = 'tarefas_arquivadas.json'

'''
    Funções auxiliares que vão imprimir o título do projeto 
    e imprimir para que o usuário dê continuar no programa
'''
def pausar():
    input("\nAperter Enter para continuar...")
    os.system('cls')

def cabecalho():
    print()
    print("- - - - - - - - - - - - - - - - - - - - -")
    print("- - - Gerenciamento da Tarefa Pessoal - - -")
    print("- - - - - - - - - - - - - - - - - - - - -")
    return



def carregar_dados(arquivo):
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
    print(f"Executando a função salvar_dados para {arquivo}")
    try:
        with open(arquivo, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
    except IOError as e:
        print(f"Erro ao salvar o arquivo {arquivo}: {e}")



def cadastro():
    '''
    Funcão de cadastro - Será pedido todas as informações 
    da tarefa para cadastra-las. Todas usam while, try/except
    '''
    cabecalho()
    print("Executando função - Cadastro\n")
    global tarefas

    print("Gerando código para a tarefa")
    codigo = gerarCod()
    pausar()
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
    os.system('cls')

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
    print(data)
    
    print(f"\nTarefa '{titulo.title()}' cadastrada com sucesso")

    tarefa = {
        "Código": codigo,
        "Titulo": titulo,
        "Descrição":descricao,
        "Prioridade": prioridade,
        "Status": status,
        "Origem": origem,
        "Data": data,
    }

    tarefas.append(tarefa)
    return

def tabelaVisualizar():
    '''
    Tabela onde mostra as tarefas com a ordem de prioridade 
    maior para a menor. Além de todos estarem formatados caso 
    em alguma coluna não tem algo preenchido
    '''
    cabecalho()
    print("Executando função - Relatório\n")
    if not tarefas:
        print("Nenhuma tarefa cadastrada.")
        return
    
    ordem_prioridade = {"URGENTE": 1, "ALTA": 2, "MÉDIA": 3, "BAIXA": 4}
    tarefas_ordenadas = sorted(tarefas, key=lambda x: ordem_prioridade.get(x["Prioridade"], 5))

   
    LARGURA_TOTAL = 121 
    
    print(f"{'Índice':<7}{'Código':<8}{'Tarefa':<20}{'Descrição':<30}{'Prioridade':<12}{'Status':<12}{'Origem':<20}{'Data':<12}")
    print("-" * LARGURA_TOTAL)

    for i, descri in enumerate(tarefas_ordenadas, start=1):
        titulo = descri.get('Titulo', 'N/A').title()
        descricao = descri.get('Descricao', 'N/A') 
        prioridade = descri.get('Prioridade', 'N/A')
        status = descri.get('Status', 'N/A')
        origem = descri.get('Origem', 'N/A')
        data = descri.get('Data', 'N/A') 

        print(f"{i:<7}{descri['Código']:<8}{titulo:<20}{descricao:<30}{prioridade:<12}{status:<12}{origem:<20}{data:<12}")
    
    print("-" * LARGURA_TOTAL)

def atualizar():
    '''
    De acordo com o código que o usuário digitar, vai ser possível 
    editar o nível de prioridade caso o código da tarefa esteja correto
    '''
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
    '''
    A função vai verificar se tem tarefas, depois se já não tem
    uma em andamento e caso não seja nenhuma dessas opções, ele vai
    pegar a tarefa que está com a prioridade mais alta e colocar ela 
    para fazer
    '''
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
    '''
    Para concluir uma tarefa, o usuário coloca o código da tarefa que ele
    quer concluir 
    '''
    global tarefas
    cabecalho()
    print("Executando função - Concluir tarefa\n")
    tarefaconclu = input("Código da tarefa concluída: ")

    for tarefa in tarefas:
        if tarefa['Código'] == tarefaconclu:
            tarefa["DataConclusao"]  = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            tarefa["Status"] = 'CONCLUÍDA'
            print(f"Tarefa '{tarefa['Titulo'].title()}' concluída na data {tarefa['DataConclusao']}")
            return
    else:
        print("Tarefa não encontrada")

def excluirTarefa():
    print("Executando função - Excluir tarefa\n")
    global tarefas

    tarefaExcluir = input("Digite o código da tarefa que deseja excluir: ")
    encontrou = False

    for tarefa in tarefas:
        if tarefa['Codigo'] == tarefaExcluir:
            tarefa["Status"] = "Excluída"
            print(f"Tarefa '{tarefa['Titulo'].title()}' marcada como 'EXCLUÍDA'.")
            print("Ela será movida para o arquivo morto na próxima limpeza.")
            encontrou = True
            break
    
    if encontrou:
        salvar_dados(ARQUIVO_TAREFAS, tarefas)
    else:
        print("Tarefa não encontrada")

def arquivamento():
    print("Executando função - Limpar e Arquivar tarefas\n")
    global tarefas
    global tarefas_arquivadas

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
                data_conclusao = datetime.strptime(tarefa["DataConclusao"], "%d/%m/%Y %H:%M:%S")
                if (dataAtual - data_conclusao).days > 7:
                    tarefa["Status"] = "ARQUIVADO" 
                    mover = True
            except (ValueError, KeyError, TypeError):
                print(f"Aviso: Tarefa '{tarefa.get('Titulo')}' CONCLUÍDA mas sem DataConclusao válida.")
                pass
        
        if mover:
            tarefasMover.append(tarefa)
            tarefas_movidas += 1
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
    Exibe todas as tarefas do arquivo de histórico
    que NÃO estejam com o status 'EXCLUÍDA'.
    Parâmetros: nenhum
    Retorno: nenhum
    """
    print("Executando função - Relatório de Arquivadas\n")
    
    if not tarefas_arquivadas:
        print("Nenhuma tarefa foi arquivada ainda.")
        return

    print("--- Histórico de Tarefas Arquivadas (não-excluídas) ---")

    tarefas_para_exibir = []
    for t in tarefas_arquivadas:
        if t.get('Status') != 'EXCLUÍDA':
            tarefas_para_exibir.append(t)

    if not tarefas_para_exibir:
        print("Nenhuma tarefa arquivada (que não seja 'EXCLUÍDA') foi encontrada.")
        return

    print(f"{'Índice':<7}{'Título':<20}{'Status':<12}{'Concluída em':<20}")
    
    for i, tarefa in enumerate(tarefas_para_exibir, start=1):
        titulo = tarefa.get('Titulo', 'N/A').title()
        status = tarefa.get('Status', 'N/A')
        data_conclusao = tarefa.get('DataConclusao', 'N/A')
        
        print(f"{i:<7}{titulo:<20}{status:<12}{data_conclusao:<20}")




def gerarCod():
    '''
        Cada tarefa terá o seu código que será calculado 
        pelo contador e convetido para ter 3 caracters
    '''
    global contadorId
    contadorId += 1 
    return str(contadorId).zfill(3)

def verificarTarefa():
    '''
    Verificar Tarefa - A função vai identificar se o título está vazio 
    e se é apenas letras
    '''
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

        







'''
    Main - Tudo o que o usuário pode ver 
'''

tarefas = carregar_dados(ARQUIVO_TAREFAS)
tarefasArquivadas = carregar_dados(ARQUIVO_HISTORICO)
contadorId = 0

if tarefas:
    '''
        Vai encontrar o maior código 
    '''
    try:
        maiorId = int(max(tarefas, key=lambda x: int(x.get('Código', 0))).get('Código', 0))
        contadorId = maiorId
    except (ValueError, TypeError):
        contadorId = 0 
pausar()

while True: 
    cabecalho()
    print("1 - Cadastrar")
    print("2 - Visualizar tabela de tarefas")
    print("3 - Atualizar tarefa")
    print("4 - Ver urgência de tarefa")
    print("5 - Concluir tarefa")
    print("6 - Arquivar tarefa")
    print("7 - Encerrar programa")

    escolha = input("\nEscolha o número do que deseja fazer: ")
    pausar()

    match escolha:
        case "1":
            cadastro()
            salvar_dados(ARQUIVO_TAREFAS, tarefas)
        case "2":
            tabelaVisualizar()
        case "3":
            atualizar()
            salvar_dados(ARQUIVO_TAREFAS, tarefas)
        case "4":
            tarefaAndamento = verificarUrgencia()
            if tarefaAndamento:
                print("\nResumo da tarefa em andamento:")
                print(f"Código: {tarefaAndamento['Código']}")
                print(f"Título: {tarefaAndamento['Titulo'].title()}")
                print(f"Prioridade: {tarefaAndamento['Prioridade']}")
                print(f"Status: {tarefaAndamento['Status']}")
                salvar_dados(ARQUIVO_TAREFAS, tarefas)
        case "5": 
            concluir()

        case "6":
            relatorioArquivamento()
            salvar_dados(ARQUIVO_TAREFAS, tarefas)
        case "7":
            print("Salvando dados antes de sair...")
            salvar_dados(ARQUIVO_TAREFAS, tarefas)
            salvar_dados(ARQUIVO_HISTORICO, tarefasArquivadas)
            print("Programa encerrado.")
            exit()
        case _: 
            print("Opção inválida!")
    pausar()