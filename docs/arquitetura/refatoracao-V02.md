ESPECIFICAÇÃO TÉCNICA — Refatoração Arquitetural do Projeto IgnoAgent
Objetivo

Realizar uma refatoração estrutural completa do projeto IgnoAgent, preservando integralmente seu comportamento atual.

O objetivo desta tarefa não é alterar funcionalidades, mas transformar o projeto em uma base profissional, modular e preparada para distribuição, testes automatizados, API centralizada e evolução para um produto SaaS.

Todo comportamento existente deve continuar funcionando exatamente como antes.

Contexto do Projeto

O IgnoAgent é um agente instalado em servidores Linux responsável por:

coletar informações do servidor;
analisar riscos;
gerar relatórios JSON;
manter histórico das execuções;
futuramente enviar os dados para uma API central;
futuramente operar como serviço de monitoramento contínuo.

Hoje o projeto já possui coletores funcionais para:

sistema
segurança
Docker
serviços
hardening
análise de rede
heartbeat

Existe geração de:

status.json
history/
outbox/

Tudo isso deve continuar funcionando.

Objetivos da Refatoração

A arquitetura deve seguir princípios de:

Clean Architecture
Separation of Concerns
Single Responsibility
Alta coesão
Baixo acoplamento
Organização por domínio

Não criar lógica desnecessária.

Não criar abstrações apenas por criar.

Priorizar simplicidade.

Estrutura final desejada

O projeto deve ficar organizado da seguinte forma:

ignoagent/

    ignoagent/

        __init__.py
        __main__.py

        agent.py

        collectors/
        analyzers/
        outputs/
        utils/
        models/

    config/

    reports/
        history/
        outbox/

    cache/

    logs/

    installer/

    scripts/

    tests/

    docs/

    README.md
    LICENSE
    requirements.txt
    pyproject.toml
    .gitignore
    Makefile
Eliminar completamente a pasta src

Toda referência a

src.

deve ser substituída por

ignoagent.

Exemplo:

ANTES

from src.collectors.system import collect

DEPOIS

from ignoagent.collectors.system import collect
Arquivo principal

Criar

ignoagent/agent.py

responsável apenas por:

coordenar coletores
coordenar analisadores
montar o relatório
enviar para outputs

Nenhuma lógica de baixo nível deve permanecer nele.

main.py

Criar

ignoagent/__main__.py

permitindo executar:

python -m ignoagent

Este deve substituir futuramente o run.py.

O run.py poderá permanecer temporariamente apenas chamando o novo módulo para manter compatibilidade.

Separação por domínio
collectors

Apenas coleta dados.

Nunca faz análise.

Nunca grava arquivos.

Nunca envia API.

analyzers

Recebem dados.

Retornam conclusões.

Nunca executam comandos Linux.

Nunca gravam arquivos.

outputs

Responsáveis por persistência.

Exemplos:

file.py

api.py

telegram.py

No futuro poderão existir:

database.py

mqtt.py

s3.py

etc.

utils

Somente funções utilitárias reutilizáveis.

Exemplos:

config.py

shell.py

filesystem.py

logger.py

time.py

Não colocar regras de negócio aqui.

models

Criar modelos responsáveis por representar:

Report

Heartbeat

Identity

No momento podem ser apenas dataclasses.

Configuração

Toda configuração deve vir de:

config/config.yml

Criar funções:

load_config()

load_identity()

load_collector_config()

load_reports_config()

Nenhuma configuração deve permanecer hardcoded.

Caminhos

Eliminar caminhos fixos espalhados pelo código.

Evitar:

Path("/opt/ignoagent")

Criar função central:

get_base_path()

capaz de funcionar tanto em:

desenvolvimento local

quanto

produção

JSON

Toda serialização deve passar por uma única função.

Criar:

save_json()

capaz de serializar automaticamente:

date

datetime

Path

sem repetir código.

Outputs

Hoje existe código duplicado salvando:

status.json

history/

outbox/

Centralizar isso.

Criar funções:

save_status()

save_history()

save_outbox()

dentro de

outputs/file.py
Docker

Toda coleta relacionada ao Docker deve ficar isolada em:

collectors/docker.py

Nunca misturar Docker com segurança.

Hardening

Toda coleta de:

UFW

Fail2Ban

Kernel

Atualizações

Portas

deve permanecer em

collectors/hardening.py
Segurança

Toda análise de

SSH

usuários inválidos

IPs

tentativas

deve permanecer em

collectors/security.py
Análises

Cada tipo de análise deve ficar isolado.

Exemplo:

analyzers/risk.py

analyzers/network.py

analyzers/availability.py

Não criar um único arquivo gigante.

Imports

Eliminar imports circulares.

Eliminar dependências desnecessárias.

Utilizar apenas imports absolutos.

Tipagem

Adicionar type hints em todo o projeto.

Exemplo:

def collect() -> dict:

def analyze(data: dict) -> dict:

def save_report(report: dict) -> None:
Docstrings

Todas as funções públicas devem possuir docstring.

Padrão Google.

Logging

Não utilizar print espalhado.

Criar utilitário:

utils/logger.py

Todo log deve passar por ele.

Testes

Criar estrutura:

tests/

Mesmo que inicialmente existam poucos testes.

Preparar para pytest.

Documentação

Criar:

docs/

contendo:

vision.md

architecture.md

roadmap.md

principles.md

decisions/

README

Criar documentação contendo:

Visão geral

Objetivo

Como instalar

Como executar

Como configurar

Estrutura

Roadmap

Licença

Contribuição

pyproject.toml

Preparar o projeto para instalação futura.

Objetivo:

pip install .

e posteriormente:

pip install ignoagent
Compatibilidade

Após a refatoração, os comandos abaixo devem continuar funcionando:

python -m ignoagent
python run.py
systemctl start ignoagent
ignoagent

caso exista o wrapper em bin/.

Restrições importantes

NÃO alterar o comportamento atual.

NÃO remover funcionalidades.

NÃO modificar a estrutura do JSON produzido.

NÃO alterar nomes das chaves do relatório.

NÃO alterar regras de negócio.

NÃO alterar cálculos de risco.

NÃO remover comentários úteis.

NÃO introduzir dependências pesadas sem necessidade.

Objetivo de longo prazo

Toda a arquitetura deve preparar o projeto para a seguinte evolução:

IgnoAgent (Agente)

        │

        ▼

API Central

        │

        ▼

Banco de Dados

        │

        ▼

Dashboard Web

        │

        ▼

Sistema de Alertas

        │

        ▼

Monitoramento Multi-Servidor

        │

        ▼

Produto SaaS

Cada agente instalado em uma VPS deverá funcionar de forma totalmente independente, gerando relatórios locais mesmo quando a API estiver indisponível. Quando houver conectividade, deverá sincronizar automaticamente os dados pendentes da pasta reports/outbox com a API central.