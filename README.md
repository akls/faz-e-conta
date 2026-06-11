# faz-e-conta

# Contribuir com Código

Em resumo, contribuir com código envolve os seguintes três passos detalhados abaixo:

1. Criar um branch de funcionalidade
2. Fazer commit do código no branch de funcionalidade
3. Criar um pull request (PR) do branch de funcionalidade para `dev` seguido de revisão de código
4. Fazer merge do PR para `dev`

## 1. Criar um Branch de Funcionalidade

Passo 1: Clonar o repositório

`git clone https://github.com/akls/faz-e-conta`

Passo 2: Mudar para o branch `dev`

`git switch dev`

Podes confirmar o branch local atual com `git status`. O resultado deve ser algo como:

​```
On branch dev
Your branch is up to date with 'origin/dev'.

nothing to commit, working tree clean
​```

Passo 3: Criar um branch de funcionalidade

Cria o branch de funcionalidade local usando um nome que siga o padrão _feature/titulo-da-issue_. Após criar o branch local, faz push para o repositório remoto. Exemplo usando o nome _feature/issue10-standardize-cdm_:

​```
git branch -m feature/issue10-standardize-cdm
git push -u origin feature/issue10-standardize-cdm
​```

## 2. Fazer Commit das Alterações de Código no Branch de Funcionalidade

Para adicionar ficheiros novos ou modificados ao próximo commit, usa os seguintes comandos:

​```
git add <nome_do_ficheiro>
git commit -m "Descrição curta das alterações"
git push
​```

## 3. Criar um Pull Request (PR) para fazer merge do branch de funcionalidade para `dev`

Os pull requests (PRs) dos branches de funcionalidade devem ser criados para o branch `dev` e só devem ser feitos merge após revisão de código completa. Ou seja, os branches de funcionalidade não devem ser diretamente merged para o branch `main`.

Para criar um PR para um branch de funcionalidade, vai à secção _Pull Requests_ no site do Github e seleciona _New pull request_. Escolhe o branch de funcionalidade e o branch `dev` e clica em _Create pull request_.

## 4. Revisão de Código

## 5. Fazer Merge do PR para `dev`

# DOCKER

Aqui estão as instruções para utilizar a aplicação com Docker.

1. `git clone <url-do-repositório>`
2. Na diretoria onde foi feito o clone, executa `docker compose up` (ter o Docker iniciado no PC)
3. Abre a aplicação no localHost
4. Conta de administrador padrão: username: `rodri` password: `nuno2013` — recomenda-se alterar após o primeiro login
5. Para gerir utilizadores, aprovar contas pendentes ou alterar credenciais, aceder ao painel de administração em `/admin`