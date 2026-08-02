# Especificação Canônica — Report Schema v1

* **Identificador da Especificação:** `IGNOAGENT-SPEC-REPORT-V1`
* **Versão:** `1.0.0`
* **Status:** Canônico / Estável
* **Autor:** Ignotec Engineering
* **Escopo:** Especificação completa e autossuficiente para implementação de agentes compatíveis com o ecossistema IgnoAgent.

---

## 1. Introdução

O **Server Report (Report Schema v1)** é a especificação do modelo de dados canônico produzido por qualquer agente compatível com o ecossistema IgnoAgent.

Esta especificação é a **única fonte da verdade** para a representação do estado de saúde, postura de segurança, recursos de sistema e vulnerabilidades de uma instância de servidor. 

Um desenvolvedor que siga este documento conseguirá implementar um agente totalmente compatível em qualquer linguagem de programação (ex: Python, Go, Rust, C++) ou sistema operacional suportado sem a necessidade de inspecionar o código-fonte de referência.

---

## 2. Regras Gerais de Formatação

1. **Formato do Arquivo/Payload:** JSON (JavaScript Object Notation), codificado em `UTF-8`.
2. **Formato de Datas e Horários:** Strings em conformidade com a norma **ISO-8601** estendida com suporte a milissegundos ou microssegundos (ex: `YYYY-MM-DDTHH:MM:SS.mmmmmm`).
3. **Chaves e Case:** Todas as chaves utilizam o padrão `snake_case` em inglês.
4. **Precisão Numérica:** Valores percentuais e de armazenamento em gigabytes (`GB`) devem utilizar tipo numérico de ponto flutuante (`float`) com arredondamento para até 2 casas decimais.
5. **Tratamento de Indisponibilidade:** Na ausência de permissões ou ferramentas de sistema (ex: Docker não instalado ou ausência do arquivo de log de autenticação), o contrato prevê chaves alternativas de erro ou listas vazias, **nunca** a omissão de blocos obrigatórios de nível raiz.

---

## 3. Exemplo de Payload Válido Completo

```json
{
    "agent": {
        "agent_id": "vps-prod-01",
        "environment": "production",
        "owner": "ignotec",
        "installation_date": "2026-08-02",
        "version": "0.1.0",
        "instance_id": "882d86be-fe53-49d1-a995-6d772e7d5e19"
    },
    "heartbeat": {
        "last_execution": "2026-08-02T15:45:42.866551",
        "status": "online"
    },
    "timestamp": "2026-08-02T15:45:42.866570",
    "server": {
        "hostname": "vps-prod-01",
        "os": "Linux-6.8.0-136-generic-x86_64-with-glibc2.39",
        "python": "3.11.9"
    },
    "system": {
        "cpu_percent": 1.8,
        "memory_percent": 43.3,
        "disk": {
            "total_gb": 220.53,
            "used_gb": 92.81,
            "free_gb": 116.47,
            "percent": 42.09
        },
        "uptime_seconds": 10256
    },
    "services": {
        "docker": [
            "web-app-production",
            "postgres-db"
        ],
        "failed_services": []
    },
    "hardening": {
        "kernel": "6.8.0-136-generic",
        "firewall": "Status: active\n\nTo Action From\n-- ------ ----\n22/tcp ALLOW Anywhere",
        "fail2ban": "active",
        "open_ports": "tcp LISTEN 0 4096 0.0.0.0:22 0.0.0.0:*",
        "updates": "0"
    },
    "security": {
        "ssh_failed_attempts": 12,
        "source_ips": [
            "206.189.19.232",
            "152.42.164.200"
        ],
        "invalid_users": [
            "root",
            "admin"
        ]
    },
    "analysis": {
        "risk_score": 25,
        "severity": "MEDIUM",
        "alerts": [
            "12 tentativas SSH falhas detectadas",
            "Tentativas de login usando usuário root"
        ],
        "recommendations": [
            "Verificar origem das tentativas de login",
            "Desabilitar login root via SSH"
        ]
    },
    "network_analysis": {
        "risk_score": 15,
        "alerts": [
            "SSH padrão exposto"
        ],
        "recommendations": [
            "Alterar porta SSH ou restringir por IP"
        ]
    }
}
```

---

## 4. Dicionário de Campos Inequívoco

### 4.1 Bloco Raiz (`root`)

| Campo | Tipo | Obrigatório | Significado |
| :--- | :--- | :--- | :--- |
| `agent` | `object` | **Sim** | Metadados do agente e sua identificação de instalação |
| `heartbeat` | `object` | **Sim** | Estado de execução e sinal de vida do agente |
| `timestamp` | `string` | **Sim** | Carimbo de data/hora ISO-8601 da compilação do relatório |
| `server` | `object` | **Sim** | Identificação do host e ambiente do sistema operacional |
| `system` | `object` | **Sim** | Métricas de uso de hardware e recursos do sistema |
| `services` | `object` | **Sim** | Estado dos serviços do sistema e contêineres Docker |
| `hardening` | `object` | **Sim** | Indicadores de postura de segurança, firewall e portas |
| `security` | `object` | **Sim** | Coleta de logs de auditoria e tentativas de intrusão |
| `analysis` | `object` | **Sim** | Avaliação determinística de risco baseada em segurança |
| `network_analysis` | `object` | **Sim** | Avaliação determinística de risco baseada em exposição de portas |

---

### 4.2 Bloco `agent`

#### `agent.agent_id`
* **Tipo:** `string`
* **Obrigatório:** Sim
* **Unidade:** N/A (Texto identificador)
* **Valores permitidos:** Qualquer string não vazia (recomendado formato kebab-case ou alphanumeric).
* **Significado:** Nome identificador do agente configurado na instalação.
* **Origem:** Arquivo de configuração `config/identity.yml` (`agent_id`).
* **Exemplo:** `"ignotec-lab"`

#### `agent.environment`
* **Tipo:** `string`
* **Obrigatório:** Sim
* **Unidade:** N/A (Categoria)
* **Valores permitidos:** `"production"`, `"staging"`, `"laboratory"`, `"development"` (ou string customizada).
* **Significado:** Categoria do ambiente em que o servidor opera.
* **Origem:** Arquivo de configuração `config/identity.yml` (`environment`).
* **Exemplo:** `"production"`

#### `agent.owner`
* **Tipo:** `string`
* **Obrigatório:** Sim
* **Unidade:** N/A
* **Valores permitidos:** String identificadora do cliente ou equipe responsável.
* **Significado:** Proprietário ou organização responsável pela máquina.
* **Origem:** Arquivo de configuração `config/identity.yml` (`owner`).
* **Exemplo:** `"ignotec"`

#### `agent.installation_date`
* **Tipo:** `string`
* **Obrigatório:** Não (Opcional / Nullable)
* **Unidade:** Data (Formato `YYYY-MM-DD`)
* **Valores permitidos:** String de data válida ISO ou nulo.
* **Significado:** Data em que o agente foi instalado originalmente no servidor.
* **Origem:** Arquivo de configuração `config/identity.yml` (`installation_date`).
* **Exemplo:** `"2026-08-02"`

#### `agent.version`
* **Tipo:** `string`
* **Obrigatório:** Sim
* **Unidade:** N/A (SemVer)
* **Valores permitidos:** Versão no formato SemVer (`MAJOR.MINOR.PATCH`).
* **Significado:** Versão do software agente responsável pela coleta.
* **Origem:** Constante do pacote ou metadados de build.
* **Exemplo:** `"0.1.0"`

#### `agent.instance_id`
* **Tipo:** `string`
* **Obrigatório:** Sim
* **Unidade:** N/A (UUID string de 36 caracteres)
* **Valores permitidos:** UUID v4 no formato padrão de 36 caracteres em hexadecimal com hífens (`xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx`).
* **Significado:** Identificador único persistente gerado localmente na primeira inicialização da instância.
* **Origem:** Arquivo persistente local `config/instance_id`.
* **Exemplo:** `"882d86be-fe53-49d1-a995-6d772e7d5e19"`

---

### 4.3 Bloco `heartbeat`

#### `heartbeat.last_execution`
* **Tipo:** `string`
* **Obrigatório:** Sim
* **Unidade:** Data/Hora ISO-8601
* **Valores permitidos:** Timestamp no formato `YYYY-MM-DDTHH:MM:SS.mmmmmm`.
* **Significado:** Momento exato em que o ciclo de coleta foi iniciado.
* **Origem:** Relógio do sistema operacional no momento da execução.
* **Exemplo:** `"2026-08-02T15:45:42.866551"`

#### `heartbeat.status`
* **Tipo:** `string`
* **Obrigatório:** Sim
* **Unidade:** N/A (Estado)
* **Valores permitidos:** `"online"`, `"degraded"`, `"offline"`
* **Significado:** Condição operacional da execução do agente.
* **Origem:** Estado retornado pelo gerenciador do agente.
* **Exemplo:** `"online"`

---

### 4.4 Campo Root `timestamp`

#### `timestamp`
* **Tipo:** `string`
* **Obrigatório:** Sim
* **Unidade:** Data/Hora ISO-8601
* **Valores permitidos:** Timestamp no formato `YYYY-MM-DDTHH:MM:SS.mmmmmm`.
* **Significado:** Carimbo final de conclusão e compilação do relatório JSON.
* **Origem:** Relógio do sistema operacional no encerramento da compilação.
* **Exemplo:** `"2026-08-02T15:45:42.866570"`

---

### 4.5 Bloco `server`

#### `server.hostname`
* **Tipo:** `string`
* **Obrigatório:** Sim
* **Unidade:** N/A (Nome de rede)
* **Valores permitidos:** Hostname válido do sistema Linux.
* **Significado:** Nome de identificação da máquina na rede.
* **Origem:** Chamada de sistema `socket.gethostname()` ou comando `/bin/hostname`.
* **Exemplo:** `"vps-prod-01"`

#### `server.os`
* **Tipo:** `string`
* **Obrigatório:** Sim
* **Unidade:** N/A
* **Valores permitidos:** String detalhada contendo nome do Kernel, arquitetura e distribuição Linux.
* **Significado:** Identificação técnica do sistema operacional e arquitetura do processador.
* **Origem:** Chamada de sistema `platform.platform()`.
* **Exemplo:** `"Linux-6.8.0-136-generic-x86_64-with-glibc2.39"`

#### `server.python`
* **Tipo:** `string`
* **Obrigatório:** Sim
* **Unidade:** N/A (Versão)
* **Valores permitidos:** Versão do runtime do agente (ex: `"3.11.9"` ou `"Go-1.22"` para agentes em Go).
* **Significado:** Versão do ambiente de execução do agente.
* **Origem:** Runtime do agente (`platform.python_version()`).
* **Exemplo:** `"3.11.9"`

---

### 4.6 Bloco `system`

#### `system.cpu_percent`
* **Tipo:** `number` (`float`)
* **Obrigatório:** Sim
* **Unidade:** Porcentagem (`%`)
* **Faixa esperada:** `0.0` a `100.0`
* **Significado:** Porcentagem média de utilização dos núcleos do processador durante o intervalo de amostragem de 1 segundo.
* **Origem:** Métricas de sistema / `/proc/stat` (ex: `psutil.cpu_percent(interval=1)`).
* **Exemplo:** `1.8`

#### `system.memory_percent`
* **Tipo:** `number` (`float`)
* **Obrigatório:** Sim
* **Unidade:** Porcentagem (`%`)
* **Faixa esperada:** `0.0` a `100.0`
* **Significado:** Porcentagem de uso da memória RAM física (considerando memória ativa vs total disponível).
* **Origem:** Métricas de sistema / `/proc/meminfo` (ex: `psutil.virtual_memory().percent`).
* **Exemplo:** `43.3`

#### `system.disk.total_gb`
* **Tipo:** `number` (`float`)
* **Obrigatório:** Sim
* **Unidade:** Gigabytes (`GB`)
* **Faixa esperada:** `>= 0.0`
* **Significado:** Capacidade total de armazenamento do sistema de arquivos montado no ponto `/`.
* **Origem:** Chamada `statvfs` no caminho `/` (convertido dividindo bytes por $1024^3$).
* **Exemplo:** `220.53`

#### `system.disk.used_gb`
* **Tipo:** `number` (`float`)
* **Obrigatório:** Sim
* **Unidade:** Gigabytes (`GB`)
* **Faixa esperada:** `>= 0.0`
* **Significado:** Espaço atualmente utilizado no ponto de montagem `/`.
* **Origem:** Chamada `statvfs` no caminho `/`.
* **Exemplo:** `92.81`

#### `system.disk.free_gb`
* **Tipo:** `number` (`float`)
* **Obrigatório:** Sim
* **Unidade:** Gigabytes (`GB`)
* **Faixa esperada:** `>= 0.0`
* **Significado:** Espaço livre disponível para gravação no ponto de montagem `/`.
* **Origem:** Chamada `statvfs` no caminho `/`.
* **Exemplo:** `116.47`

#### `system.disk.percent`
* **Tipo:** `number` (`float`)
* **Obrigatório:** Sim
* **Unidade:** Porcentagem (`%`)
* **Faixa esperada:** `0.0` a `100.0`
* **Significado:** Porcentagem ocupada do espaço em disco no ponto de montagem `/` (calculado por `(used_gb / total_gb) * 100`).
* **Origem:** Cálculo derivado das métricas de disco.
* **Exemplo:** `42.09`

#### `system.uptime_seconds`
* **Tipo:** `integer`
* **Obrigatório:** Sim
* **Unidade:** Segundos
* **Faixa esperada:** `>= 0`
* **Significado:** Tempo total em segundos desde a última inicialização do sistema operacional.
* **Origem:** Diferença entre o horário atual do sistema e a hora de boot (`/proc/uptime` ou `psutil.boot_time()`).
* **Exemplo:** `10256`

---

### 4.7 Bloco `services`

#### `services.docker`
* **Tipo:** `array` de `string`
* **Obrigatório:** Sim
* **Unidade:** N/A (Lista de nomes)
* **Valores permitidos:** Array contendo os nomes dos contêineres Docker em execução (`running`). Se não houver contêineres rodando, retorna array vazio `[]`.
* **Origem:** Comando `docker ps --format "{{.Names}}"`.
* **Exemplo:** `["agentego-dashboard", "agentego-bot"]`

#### `services.failed_services`
* **Tipo:** `array` de `string`
* **Obrigatório:** Sim
* **Unidade:** N/A (Lista de nomes)
* **Valores permitidos:** Array contendo o nome dos serviços `systemd` que estão em estado de falha (`failed`). Retorna `[]` se nenhum serviço estiver falho.
* **Origem:** Comando `systemctl --failed --no-legend`.
* **Exemplo:** `["nginx.service"]`

#### `services.docker_error`
* **Tipo:** `string`
* **Obrigatório:** Não (Apenas presente em caso de erro)
* **Unidade:** N/A (Mensagem de erro)
* **Valores permitidos:** String de exceção capturada caso a execução do comando Docker falhe (ex: daemon Docker parado ou permissão negada).
* **Origem:** Captura de exceção ao tentar consultar o Docker.
* **Exemplo:** `"Command 'docker ps' returned non-zero exit status 1."`

#### `services.systemd_error`
* **Tipo:** `string`
* **Obrigatório:** Não (Apenas presente em caso de erro)
* **Unidade:** N/A (Mensagem de erro)
* **Valores permitidos:** String de exceção capturada caso o `systemctl` não esteja disponível.
* **Origem:** Captura de exceção no comando `systemctl`.
* **Exemplo:** `"systemctl not found"`

---

### 4.8 Bloco `hardening`

#### `hardening.kernel`
* **Tipo:** `string`
* **Obrigatório:** Sim
* **Unidade:** N/A (Versão)
* **Valores permitidos:** Release do Kernel Linux retornada pelo sistema.
* **Origem:** Chamada `platform.release()` ou `uname -r`.
* **Exemplo:** `"6.8.0-136-generic"`

#### `hardening.firewall`
* **Tipo:** `string`
* **Obrigatório:** Não (Nullable)
* **Unidade:** N/A (Texto bruto de status)
* **Valores permitidos:** Saída resumida das 5 primeiras linhas do comando `ufw status`, ou `null` caso indisponível.
* **Origem:** Comando `sudo /usr/sbin/ufw status | head -5`.
* **Exemplo:** `"Status: active"`

#### `hardening.fail2ban`
* **Tipo:** `string`
* **Obrigatório:** Não (Nullable)
* **Unidade:** N/A (Estado)
* **Valores permitidos:** `"active"`, `"inactive"`, ou `null` caso o Fail2Ban não esteja instalado.
* **Origem:** Comando `/usr/bin/systemctl is-active fail2ban`.
* **Exemplo:** `"active"`

#### `hardening.open_ports`
* **Tipo:** `string`
* **Obrigatório:** Não (Nullable)
* **Unidade:** N/A (Texto bruto de portas em escuta)
* **Valores permitidos:** String multilinha contendo a lista de sockets TCP/UDP em estado `LISTEN`, ou `null`.
* **Origem:** Comando `/usr/bin/ss -tulpn | grep LISTEN`.
* **Exemplo:** `"tcp LISTEN 0 4096 0.0.0.0:22 0.0.0.0:*"`

#### `hardening.updates`
* **Tipo:** `string` (Representação numérica em string)
* **Obrigatório:** Sim
* **Unidade:** Contagem de pacotes
* **Valores permitidos:** String representando o número inteiro de pacotes com atualização pendente.
* **Origem:** Saída filtrada do gerenciador de pacotes (ex: `/usr/bin/apt list --upgradable`).
* **Exemplo:** `"0"`

---

### 4.9 Bloco `security`

#### `security.ssh_failed_attempts`
* **Tipo:** `integer`
* **Obrigatório:** Sim
* **Unidade:** Contagem de tentativas
* **Faixa esperada:** `>= 0`
* **Significado:** Número total de tentativas de login SSH mal-sucedidas registradas no arquivo de log de autenticação (analisando as últimas 500 linhas).
* **Origem:** Leitura do arquivo `/var/log/auth.log` procurando por marcas de `"Failed password"` ou `"Invalid user"`.
* **Exemplo:** `83`

#### `security.source_ips`
* **Tipo:** `array` de `string`
* **Obrigatório:** Sim
* **Unidade:** N/A (Lista de Endereços IP IPv4/IPv6)
* **Valores permitidos:** Lista de strings de endereços IP distintos que originaram tentativas falhas de login SSH.
* **Origem:** Expressão regular extraindo IPs de origem em `/var/log/auth.log`.
* **Exemplo:** `["206.189.19.232", "152.42.164.200"]`

#### `security.invalid_users`
* **Tipo:** `array` de `string`
* **Obrigatório:** Sim
* **Unidade:** N/A (Lista de nomes de usuário)
* **Valores permitidos:** Lista de nomes de usuários inexistentes tentados durante ataques de força bruta no SSH.
* **Origem:** Expressão regular extraindo nomes de usuário em `/var/log/auth.log`.
* **Exemplo:** `["root", "easypanel", "admin"]`

---

### 4.10 Bloco `analysis`

#### `analysis.risk_score`
* **Tipo:** `integer`
* **Obrigatório:** Sim
* **Unidade:** Pontos de Risco (Score)
* **Faixa esperada:** `>= 0` (Tipicamente entre `0` e `100+`)
* **Regra de Cálculo Determinística:**
  - Se `ssh_failed_attempts > 0`: soma `+10`
  - Se `"root"` presente em `invalid_users`: soma `+15`
  - Se `ssh_failed_attempts > 100`: soma `+25`
* **Significado:** Pontuação agregada de risco de segurança cibernética do servidor.
* **Origem:** Função de análise de risco executada sobre os dados do bloco `security`.
* **Exemplo:** `25`

#### `analysis.severity`
* **Tipo:** `string`
* **Obrigatório:** Sim
* **Unidade:** N/A (Nível de Risco)
* **Valores permitidos:** `"LOW"`, `"MEDIUM"`, `"HIGH"`
* **Regra de Mapeamento Determinística:**
  - `score >= 50`: `"HIGH"`
  - `score >= 25`: `"MEDIUM"`
  - `score < 25`: `"LOW"`
* **Significado:** Classificação categórica de severidade de segurança.
* **Origem:** Função de análise baseada no `risk_score`.
* **Exemplo:** `"MEDIUM"`

#### `analysis.alerts`
* **Tipo:** `array` de `string`
* **Obrigatório:** Sim
* **Unidade:** N/A (Lista de alertas em texto legível)
* **Valores permitidos:** Mensagens descritivas em português/inglês identificando as ameaças encontradas.
* **Origem:** Avaliação das regras de segurança.
* **Exemplo:** `["83 tentativas SSH falhas detectadas", "Tentativas de login usando usuário root"]`

#### `analysis.recommendations`
* **Tipo:** `array` de `string`
* **Obrigatório:** Sim
* **Unidade:** N/A (Lista de recomendações acionáveis)
* **Valores permitidos:** Recomendações de remediação correspondentes a cada alerta gerado.
* **Origem:** Mapeamento de recomendações de segurança.
* **Exemplo:** `["Verificar origem das tentativas de login", "Desabilitar login root via SSH"]`

---

### 4.11 Bloco `network_analysis`

#### `network_analysis.risk_score`
* **Tipo:** `integer`
* **Obrigatório:** Sim
* **Unidade:** Pontos de Risco (Score de Rede)
* **Faixa esperada:** `>= 0`
* **Regra de Cálculo Determinística:** Cada porta sensível detectada no parâmetro `hardening.open_ports` adiciona `15` pontos ao score (`quantidade_de_riscos * 15`).
* **Portas Sensíveis Inspecionadas:**
  - Porta `2377`: Docker Swarm Manager exposto publicamente
  - Porta `7946`: Porta de comunicação Docker Swarm detectada
  - Porta `3000`: Serviço web administrativo detectado na porta 3000
  - Porta `22`: SSH padrão exposto
* **Origem:** Função de análise de portas sobre o texto de `hardening.open_ports`.
* **Exemplo:** `15`

#### `network_analysis.alerts`
* **Tipo:** `array` de `string`
* **Obrigatório:** Sim
* **Unidade:** N/A (Lista de alertas de rede)
* **Valores permitidos:** Lista de strings descrevendo exposições de portas sensíveis detectadas.
* **Origem:** Regras de análise de portas de rede.
* **Exemplo:** `["Serviço web administrativo detectado na porta 3000"]`

#### `network_analysis.recommendations`
* **Tipo:** `array` de `string`
* **Obrigatório:** Sim
* **Unidade:** N/A (Lista de recomendações de rede)
* **Valores permitidos:** Instruções de configuração de firewall ou proxy para mitigação.
* **Origem:** Regras de análise de portas de rede.
* **Exemplo:** `["Manter protegido por firewall ou proxy reverso"]`

---

## 5. Regras de Compatibilidade e Evolução do Esquema

Para garantir que o ecossistema IgnoAgent evolua de forma previsível sem interromper consumidores (APIs, Dashboards, Banco de Dados), qualquer implementação DEVE seguir as diretrizes abaixo:

### 5.1 Adição de Novos Campos (Backward Compatible)
- Novos coletores ou métricas (ex: uso de GPU, métricas Nginx, temperatura) DEVEM ser adicionados como chaves opcionais dentro dos sub-objetos existentes ou em novos objetos de nível raiz.
- Consumidores da API e do banco de dados DEVEM ignorar chaves desconhecidas recebidas no JSON sem falhar a compilação ou desserialização.

### 5.2 Alterações Incompatíveis (Breaking Changes)
As seguintes alterações são consideradas **incompatíveis** e são estritamente **proibidas** dentro da versão `v1`:
- Remover ou renomear qualquer chave definida como **Obrigatória** na Seção 4.
- Alterar o tipo de dado de uma chave (ex: alterar `cpu_percent` de `number` para `string`).
- Alterar as unidades de medida (ex: alterar `disk.total_gb` de Gigabytes para Megabytes ou Bytes).

Caso qualquer uma dessas alterações seja estritamente necessária no futuro, uma nova especificação **`report-schema-v2.md`** deverá ser criada, mantendo o suporte ao `v1` durante o período de transição.

---

## 6. Guia de Validação para Implementadores

Uma implementação de agente (em qualquer linguagem) será considerada **100% compatível com a especificação Report Schema v1** se, e somente se:

1. **Validação de Sintaxe e Codificação:** Produzir uma string JSON UTF-8 válida.
2. **Validação de Presença:** Conter todas as 10 chaves obrigatórias no objeto raiz (`agent`, `heartbeat`, `timestamp`, `server`, `system`, `services`, `hardening`, `security`, `analysis`, `network_analysis`).
3. **Validação de Tipos:** Todos os tipos de dados (float, integer, string, array, object) corresponderem exatamente ao Dicionário de Campos (Seção 4).
4. **Validação de Formatos:** O `instance_id` ser um UUID v4 válido e os timestamps estarem no formato ISO-8601.
