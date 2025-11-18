# 🚀 Gerenciador de Tarefas

![Status do Projeto](https://img.shields.io/badge/Status-Concluído-brightgreen)
![Tecnologia](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Tecnologia](https://img.shields.io/badge/JSON-000000?style=flat&logo=json&logoColor=white)

Este projeto é uma ferramenta simples de linha de comando para gerenciamento de tarefas, criada como parte da "Atividade de Aplicação: Estruturando Soluções". O sistema permite armazenar e acompanhar múltiplas tarefas, gerenciando-as por prioridade e status.

## 🚧 Status do Projeto
✅ Concluído

## 💻 Tecnologias Utilizadas
* **Python**
* **JSON** (para persistência de dados)

## ✨ Funcionalidades Principais

O sistema implementa um ciclo de vida completo para o gerenciamento de tarefas:

### 1. CRUD de Tarefas
* **Criar Tarefas:** Adiciona uma nova tarefa à lista. Cada tarefa contém:
    * ID Único (gerado automaticamente)
    * Título 
    * Descrição
    * Prioridade (Urgente, alta, média, baixa)
    * Origem (E-mail, Telefone, Chamado do Sistema)
    * Data de Criação (automática)
    * Status (começa como "Pendente")
* **Atualizar Prioridade:** Permite ao usuário alterar a prioridade de uma tarefa existente.
* **Concluir Tarefas:** Altera o status para "Concluída" e armazena a data/hora de conclusão.
* **Excluir Tarefas:** Realiza uma "exclusão lógica" alterando o status para "Excluída". O dado não é removido permanentemente.

### 2. Gerenciamento de Fluxo
* **Arquivamento Automático:** Tarefas que foram "Concluídas" há mais de uma semana são automaticamente atualizadas para o status "Arquivado".

### 3. Relatórios
* **Relatório Geral:** Exibe todas as informações de todas as tarefas. Para tarefas concluídas, calcula e exibe o tempo total de execução.
* **Relatório de Arquivadas:** Exibe uma lista contendo apenas as tarefas com status "Arquivado". Tarefas excluídas não aparecem neste relatório.

### 4. Persistência de Dados
* **`tarefas.json`:** O sistema carrega todas as tarefas ativas deste arquivo ao iniciar e salva a lista atualizada ao sair.
* **`tarefasArquivadas.json`:** Tarefas com status "Arquivado" ou "Excluída" são movidas para este arquivo de histórico.
* **Criação Automática:** Se os arquivos `.json` não existirem no início, o sistema os cria automaticamente com uma lista vazia `[]`.


## 🏗️ Estrutura e Boas Práticas

O código foi estruturado seguindo os requisitos de boas práticas:

* **Menu de Controle:** Um menu principal centraliza todas as ações do sistema.
* **Modularização:** Cada opção do menu é implementada como uma função separada para facilitar a manutenção e leitura.
* **Escopo de Variáveis:** Utiliza variáveis globais para a lista de tarefas e o contador de ID, e variáveis locais para processamento interno em funções. A palavra-chave `global` é usada quando necessário.
* **Defesas do Código:**
    * **1ª Defesa (Validação Lógica):** Funções de validação garantem que os dados inseridos pelo usuário (como Prioridade ou opções de menu) sejam válidos.
    * **2ª Defesa (Robustez Técnica):** Blocos `try/except` são usados para tratar erros de conversão de tipo (ex: usuário digita texto em vez de número no menu), evitando que o programa pare abruptamente.
* **Documentação:** Todas as funções contêm *Docstrings* (`"""..."""`) explicando seu propósito, parâmetros e retorno.

## 👨‍💻 Autores

<p align="center">
  <b>Giulia Ayumi</b>
  <br>
  <a href="https://github.com/giuayumii" target="_blank">
   <img src=https://img.shields.io/badge/github-%2324292e.svg?&style=for-the-badge&logo=github&logoColor=white alt=github style="margin-bottom: 5px;" />
</p>
<br>
<p align="center">
  <b>Vinicius Oliveira</b>
  <br>
  <a href="https://github.com/ViniEduOliveira" target="_blank">
   <img src=https://img.shields.io/badge/github-%2324292e.svg?&style=for-the-badge&logo=github&logoColor=white alt=github style="margin-bottom: 5px;" />
</p>



