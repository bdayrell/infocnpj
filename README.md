# infocnpj
Script para varredura automática de informações de empresas, dado uma lista de CNPJ

## Como utilizar
1 - Crie uma lista em formato csv com os cnpjs que você deseja analisar 

2 - Siga o exemplo fornecido, que contém os cnpjs da Petrobras, Banco do brasil e Vale.

3 - Coloque a lista na mesma pasta que o arquivo main.py

4 - Execute o script principal com o comando:
>python main.py

5 - digite o nome do arquivo que você colocou para análise 
>nome arquivo = inputexample.csv

6 - aguarde o final da execução. O nome do arquivo final será exibido na penúltima linha no formato
>results_<nome_inicial>.csv

7 - o resultado estará na mesma pasta de origem

Dados coletados:
<span style="background-color:#5d5d5d; color:white; padding: 5px 10px; border-radius: 5px;line-height: 30px;">CNPJ</span> 
<span style="background-color:#5d5d5d; color:white; padding: 5px 10px; border-radius: 5px;line-height: 30px;">Nome Fantasia</span> 
<span style="background-color:#5d5d5d; color:white; padding: 5px 10px; border-radius: 5px;line-height: 30px;">CNAE</span>
<span style="background-color:#5d5d5d; color:white; padding: 5px 10px; border-radius: 5px;line-height: 30px;">Atividade</span> 
<span style="background-color:#5d5d5d; color:white; padding: 5px 10px; border-radius: 5px; line-height: 30px;">CNPJ de Origem</span>
<span style="background-color:#5d5d5d; color:white; padding: 5px 10px; border-radius: 5px;line-height: 30px;">Capital Social</span>
<span style="background-color:#5d5d5d; color:white; padding: 5px 10px; border-radius: 5px;line-height: 30px;">UF</span>
 <span style="background-color:#5d5d5d; color:white; padding: 5px 10px; border-radius: 5px;line-height: 30px;">Município</span> 



## Como funciona
O script varre a lista, executando chamadas de APIs públicas para obtenção de informações das empresas.
API utilizada: https://www.receitaws.com.br/v1/cnpj
A limitação do serviço gratuito é de 1 chamada a cada 30s. Por isso, sua ação pode demorar um pouco a ser executada

### Comandos básicos git
#### Get Started
##### Baixando o script pelo git
- se não tiver, baixe e instale o git [aqui](https://git-scm.com/downloads)
- na pasta desejada, execute os comandos
>git init
>git clone https://github.com/bdayrell/infocnpj.git

##### Baixando o pacote zip 
1 - acima nesta página, clique em <span style="background-color:#1f883d; color:white; padding: 5px 10px; border-radius: 5px;line-height: 30px;">Code</span>  
2 - clique em download zip, extraia e execute em seu computador.

#### Stage & Commit
|Syntax | Description|
|------- |-----------|
git status | mostra os arquivos staged modificados
git add . |adiciona todos os arquivos
git reset [file] | tira o arquivo de stage
git diff | diff do que está diferente do staged
git commit -m "[message]" | comita o staged 
#### Branch & Merge
|Syntax | Description|
|------- |-----------|
git branch | lista as branches
git branch [branch] | cria uma nova branch com o commit atual
git branch -d [branch] | deleta branch
git checkout | muda de branch e atualiza o diretório
git merge [betterBranch] | Traz a betterBranch para a brench atual, mesclando
git checkout -b newbranch | cria uma branch, muda pra ela com o commit atual
#### Share & update
|Syntax | Description|
|------- |-----------|
git remote add [alias][url] | add git URL as an alias
git merge [alias]/[branch] | merge remote branch to current branch
git push [alias][branch] | Joga a logal no repositorio remoto
git pull | fetch and merge any commints from the tracking remote branch
git reset | joga fora todas as alterações não comitadas


uso: Desconsiderar as alterações locais e trazer a nova versão do repositório
> git reset --hard
> git pull origin branch


uso: Fazer as alterações atuais virarem a branch-pai (descartando alterações da branch-pai)
> git checkout better-branch
> git merge --strategy=ours master
> git checkout master
> git merge better-branch
