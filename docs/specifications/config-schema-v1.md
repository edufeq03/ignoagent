# Especificação Técnica — Configuration Schema v1

* **Versão da Especificação:** 1.0.0
* **Status:** Canônico

## Visão Geral
Esta especificação define os arquivos de configuração suportados pelo IgnoAgent, localizados na pasta `config/` (`config.yml` e `identity.yml`).

---

## 1. `config/identity.yml` (Identidade da Instalação)

Define os metadados de identificação do servidor e organização.

```yaml
agent_id: "ignotec-lab"
environment: "laboratory"
owner: "ignotec"
installation_date: "2026-08-02"
version: "1.0.0"
```

### Campos:
| Campo | Tipo | Obrigatório | Descrição |
| :--- | :--- | :--- | :--- |
| `agent_id` | `string` | Sim | Nome identificador do agente ou host |
| `environment` | `string` | Sim | Categoria do ambiente (`production`, `staging`, `laboratory`) |
| `owner` | `string` | Sim | Organização ou cliente proprietário da máquina |
| `installation_date` | `string` | Não | Data da instalação inicial |
| `version` | `string` | Sim | Versão do agente |

---

## 2. `config/config.yml` (Configurações Operacionais)

Define o comportamento dos coletores, relatórios e envios do agente.

```yaml
agent:
  interval_seconds: 300

collectors:
  system: true
  services: true
  hardening: true
  security: true

reports:
  save_local: true
  outbox_queue: true
```

---

## 3. `config/instance_id` (Identificador Único por Instalação)

Arquivo contendo uma string pura com um UUID v4 de 36 caracteres gerado na primeira inicialização do agente.

* **Exemplo:** `882d86be-fe53-49d1-a995-6d772e7d5e19`
* **Regra:** Este arquivo **nunca deve ser versionado** no repositório de código (`.gitignore`).
