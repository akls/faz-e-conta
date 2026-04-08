# faz-e-conta



# Contributing Code

In short, contributing code involves the following three steps that are outlined in detail below:

1. Creating a feature branch
2. Commiting code to the feature branch
3. Create a pull request (PR) from feature branch to `dev` followed by code review
5. Merge the PR to `dev`

## 1. Creating a Feature Branch

Step 1: Clone the repository

`git clone https://github.com/akls/faz-e-conta`

Step 2: Switch to the `dev` branch

`git switch dev`

You can confirm the current local branch with `git status`. The output should be something like

```
On branch dev
Your branch is up to date with 'origin/dev'.

nothing to commit, working tree clean
```

Step 3: Create a feature branch

Create the local feature branch using a name that follows the common _feature/issue-title_ pattern. After creating the local branch, push the change to the remote repository. An example using the branch name _feature/issue10-standardize-cdm_:

```
git branch -m feature/issue10-standardize-cdm
git push -u origin feature/issue10-standardize-cdm
```

## 2. Commiting Code Changes to the Feature Branch

In order to add new files or modified files to the next commit, use the following command:

```
git add <file_name>
git -m "This is a short description of the changes"`
git push
```

## 3. Create a pull request (PR) to merge the feature branch into `dev`

Pull requests (PRs) from the feature branches should be created for the `dev` branch and merged only after completed code review. That is, feature branches should not be merged directly to the `main` branch.

To create a PR for a feature branch, go to the section _Pull Requests_ on the Github website and select _New pull request_. Choose the feature branch and `dev` branch and click `Create pull request`.

## 4. Code review

## 5. Merge the PR to `dev`

# First-time Django Installation

1. `pip install django`
2. `python -m django startproject faz_e_conta`
3. `python manage.py startapp data_hub`

After doing changes to the (data) model:

4. `python manage.py makemigrations`
5. `python manage.py migrate`

To run the server:

6. `python manage.py runserver`

# Estado dos Requisitos

## Legenda
- ✅ Feito
- 🔄 Em progresso
- ❌ Não iniciado
- ♻️ Refeito / Melhorado

---

# 1. Funcionalidades

## 1.1 Mensalidades e Pagamentos

- [ ] RQ_F07 - Cálculo da mensalidade  
  Estado:  
  Notas:  

- [ ] RQ_F08 - Registo de pagamentos  
  Estado:  
  Notas:  

- [ ] RQ_F09 - Monitoramento de pagamentos em atraso  
  Estado:  
  Notas:  

---

## 1.2 Despesas

- [ ] RQ_F10 - Registo de despesas diárias  
  Estado:  
  Notas:  

- [ ] RQ_F11 - Definição de despesas fixas  
  Estado:  
  Notas:  

- [ ] RQ_F12 - Revisão de despesas mensais  
  Estado:  
  Notas:  

---

## 1.3 Saúde Financeira

- [ ] RQ_F13 - Análises e cálculos financeiros  
  Estado:  
  Notas:  

- [ ] RQ_F14 - Relatórios (Excel/PDF com filtros)  
  Estado:  
  Notas:  

- [ ] RQ_F15 - Guardar filtros de relatórios  
  Estado:  
  Notas:  

- [ ] RQ_F16 - Envio automático de relatórios  
  Estado:  
  Notas:  

- [ ] RQ_F17 - Comunicação com pais (email/SMS)  
  Estado:  
  Notas:  

---

# 2. Base de Dados

- [ ] RQ_F01 - Criação de contas e aprovação  
  Estado:  
  Notas:  

- [ ] RQ_F04 - Questionário de inscrição  
  Estado:  
  Notas:  

- [ ] RQ_F05 - Dados do aluno  
  Estado:  
  Notas:  

- [ ] RQ_F02 - Importação de Excel/CSV  
  Estado:  
  Notas:  

- [ ] RQ_F03 - Organização por anos letivos  
  Estado:  
  Notas:  

- [ ] RQ_F06 - Dados dos encarregados  
  Estado:  
  Notas:  

- [ ] RQ_F08 - Registo de pagamentos  
  Estado:  
  Notas:  

- [ ] RQ_F21 - Monitorização de vacinação  
  Estado:  
  Notas:  

---

# 3. Segurança

- [ ] RQ_F18 - Aprovação de alterações na BD  
  Estado:  
  Notas:  

- [ ] RQ_F19 - Notificações e logs  
  Estado:  
  Notas:  

- [ ] RQ_F20 - Base de dados alumni  
  Estado:  
  Notas:  

---

# 4. Requisitos Não Funcionais

- [ ] RQ_NF01 - Backend em Python  
  Estado:  
  Notas:  

- [ ] RQ_NF02 - HTML + CSS  
  Estado:  
  Notas:  

- [ ] RQ_NF03 - JavaScript  
  Estado:  
  Notas:  

- [ ] RQ_NF04 - Base de dados SQLite  
  Estado:  
  Notas:  

- [ ] RQ_NF05 - Fácil instalação  
  Estado:  
  Notas:  

- [ ] RQ_NF06 - Interface intuitiva  
  Estado:  
  Notas:  

- [ ] RQ_NF07 - Arquitetura modular  
  Estado:  
  Notas:  

- [ ] RQ_NF08 - Backups automáticos  
  Estado:  
  Notas:  

- [ ] RQ_NF09 - Limpeza de backups (>72h)  
  Estado:  
  Notas:  
