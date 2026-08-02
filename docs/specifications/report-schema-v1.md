# Especificação Técnica — Report Schema v1

* **Versão da Especificação:** 1.0.0
* **Status:** Canônico

## Visão Geral
O **Server Report (Report Schema v1)** define o modelo de dados canônico gerado pelo IgnoAgent. Ele representa o estado completo de saúde, métricas de sistema, configurações de hardening e análises de risco de um servidor Linux em um determinado instante no tempo.

---

## Estrutura do Payload Root

```json
{
  "agent": { ... },
  "heartbeat": { ... },
  "timestamp": "ISO-8601 String",
  "server": { ... },
  "system": { ... },
  "services": { ... },
  "hardening": { ... },
  "security": { ... },
  "analysis": { ... },
  "network_analysis": { ... }
}
```

---

## Detalhamento dos Blocos

### 1. `agent` (Obrigatório)
Identificação do agente instalado no servidor.

| Campo | Tipo | Obrigatório | Descrição / Exemplo |
| :--- | :--- | :--- | :--- |
| `agent_id` | `string` | Sim | Identificador lógico do agente (`"ignotec-lab"`) |
| `environment` | `string` | Sim | Ambiente de execução (`"production"`, `"laboratory"`, `"staging"`) |
| `owner` | `string` | Sim | Proprietário/Organização responsável (`"ignotec"`) |
| `installation_date` | `string` | Não | Data de instalação no formato YYYY-MM-DD |
| `version` | `string` | Sim | Versão do pacote do agente (`"0.1.0"`) |
| `instance_id` | `string` | Sim | UUID v4 único da instância do agente (`"882d86be-..."`) |

---

### 2. `heartbeat` (Obrigatório)
Sinal de vida e estado operacional do agente.

| Campo | Tipo | Obrigatório | Descrição / Exemplo |
| :--- | :--- | :--- | :--- |
| `last_execution` | `string` | Sim | Carimbo ISO-8601 da execução (`"2026-08-02T15:45:42.866551"`) |
| `status` | `string` | Sim | Estado do serviço do agente (`"online"`, `"degraded"`) |

---

### 3. `timestamp` (Obrigatório)
Data e hora da compilação do relatório em formato ISO-8601 UTC/Local.

---

### 4. `server` (Obrigatório)
Identificação do sistema operacional e ambiente do host.

| Campo | Tipo | Obrigatório | Descrição / Exemplo |
| :--- | :--- | :--- | :--- |
| `hostname` | `string` | Sim | Nome de rede da máquina (`"vps-prod-01"`) |
| `os` | `string` | Sim | Descrição do kernel e distribuição (`"Linux-6.8.0-136-generic-x86_64"`) |
| `python` | `string` | Sim | Versão do interpretador Python (`"3.11.9"`) |

---

### 5. `system` (Obrigatório)
Métricas de uso de hardware e recursos do sistema.

| Campo | Tipo | Obrigatório | Unidade | Descrição / Exemplo |
| :--- | :--- | :--- | :--- | :--- |
| `cpu_percent` | `float` | Sim | % | Porcentagem média de uso da CPU (0.0 a 100.0) |
| `memory_percent` | `float` | Sim | % | Porcentagem de uso da memória RAM (0.0 a 100.0) |
| `disk.total_gb` | `float` | Sim | GB | Espaço total em disco montado em `/` |
| `disk.used_gb` | `float` | Sim | GB | Espaço usado em disco |
| `disk.free_gb` | `float` | Sim | GB | Espaço livre em disco |
| `disk.percent` | `float` | Sim | % | Porcentagem ocupada em disco |
| `uptime_seconds` | `integer` | Sim | segundos | Tempo decorrido desde a inicialização do SO |

---

### 6. `services` (Obrigatório)
Status dos contêineres e serviços do sistema.

| Campo | Tipo | Obrigatório | Descrição / Exemplo |
| :--- | :--- | :--- | :--- |
| `docker` | `array[string]`| Sim | Lista com os nomes dos contêineres Docker ativos |
| `failed_services` | `array[string]`| Sim | Lista com os nomes dos serviços systemd em falha |
| `docker_error` | `string` | Não | Mensagem de erro caso a CLI Docker não esteja disponível |
| `systemd_error` | `string` | Não | Mensagem de erro caso o systemctl não esteja disponível |

---

### 7. `hardening` (Obrigatório)
Métricas de postura de segurança e portas abertas.

| Campo | Tipo | Obrigatório | Descrição / Exemplo |
| :--- | :--- | :--- | :--- |
| `kernel` | `string` | Sim | Versão da release do Kernel Linux (`"6.8.0-136-generic"`) |
| `firewall` | `string` | Não | Output ou status do UFW (`"Status: active"`) |
| `fail2ban` | `string` | Não | Status do serviço fail2ban (`"active"`, `null`) |
| `open_ports` | `string` | Não | String formatada com portas em escuta (`LISTEN`) via `ss` |
| `updates` | `string` | Sim | Número de pacotes pendentes de atualização (`"0"`) |

---

### 8. `security` (Obrigatório)
Análise de logs de autenticação (`/var/log/auth.log`).

| Campo | Tipo | Obrigatório | Descrição / Exemplo |
| :--- | :--- | :--- | :--- |
| `ssh_failed_attempts` | `integer` | Sim | Número de tentativas de login falhas detectadas |
| `source_ips` | `array[string]`| Sim | Lista de IPs de origem das tentativas falhas |
| `invalid_users` | `array[string]`| Sim | Nomes de usuários inexistentes/inválidos tentados |

---

### 9. `analysis` (Obrigatório)
Resultado da análise de risco de segurança.

| Campo | Tipo | Obrigatório | Descrição / Exemplo |
| :--- | :--- | :--- | :--- |
| `risk_score` | `integer` | Sim | Pontuação numérica de risco (0 a 100+) |
| `severity` | `string` | Sim | Nível de severidade (`"LOW"`, `"MEDIUM"`, `"HIGH"`) |
| `alerts` | `array[string]`| Sim | Lista de alertas gerados |
| `recommendations` | `array[string]`| Sim | Recomendação de ações corretivas |

---

### 10. `network_analysis` (Obrigatório)
Resultado da análise de exposição de portas de rede.

| Campo | Tipo | Obrigatório | Descrição / Exemplo |
| :--- | :--- | :--- | :--- |
| `risk_score` | `integer` | Sim | Pontuação numérica de risco de exposição |
| `alerts` | `array[string]`| Sim | Alertas de portas sensíveis expostas |
| `recommendations` | `array[string]`| Sim | Recomendações de firewall e proxy |

---

## Regras de Evolução do Esquema (Extensibilidade)

1. **Adição de Novos Campos:** Novos coletores ou campos adicionais podem ser incluídos em sub-objetos existentes sem alterar a versão do esquema, contanto que sejam opcionais para leitores antigos.
2. **Depreciação de Campos:** Nenhum campo obrigatório existente pode ser removido ou ter seu tipo alterado no `v1`. Mudanças incompatíveis exigiriam uma nova especificação `report-schema-v2.md`.
