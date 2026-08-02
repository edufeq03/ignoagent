# Especificação Técnica — API Protocol v1 Specification

* **Identificador da Especificação:** `IGNOAGENT-SPEC-API-V1`
* **Versão do Protocolo:** `1.0.0`
* **Status:** Canônico / Estável
* **Autor:** Ignotec Engineering
* **Escopo:** Especificação completa e autossuficiente para implementação da API Central do IgnoAgent (servidor receptor) e clientes compatíveis (agentes).

---

## 1. Visão Geral da Arquitetura da API

A **API Protocol v1** do IgnoAgent é uma interface HTTP REST/JSON projetada para a recepção resiliente, autenticada e imutável de relatórios de servidores e controle de agentes.

### 1.1 Princípio da Imutabilidade de Eventos
Toda requisição enviada para o endpoint `POST /v1/reports` é tratada como um **evento histórico imutável**:
- **Sem Sobrescrita:** A API nunca "atualiza" um relatório anterior. Cada execução do agente grava uma nova entrada temporal.
- **Estado Atual Derivado:** O "estado atual" de uma VPS no Dashboard é o resultado derivado da consulta do relatório imutável mais recente (`latest`).
- **Observabilidade Temporal:** A preservação histórica permite auditar a linha do tempo completa da infraestrutura (ex: métricas pré-queda, horários de picos de uso, histórico de ataques SSH e momento exato de exposição de portas).

---

## 2. Padrões Globais de Rede e Protocolo

### 2.1 Transporte e Criptografia
- **Protocolo Base:** HTTP/1.1 ou HTTP/2 sobre **TLS 1.3 (HTTPS)** obrigatório em produção.
- **Codificação:** `UTF-8`
- **Content-Type:** `application/json`

### 2.2 Cabeçalhos Padrão de Requisição (Headers)

Todo agente compatível DEVE enviar os seguintes cabeçalhos HTTP em todas as requisições:

```http
Content-Type: application/json
Authorization: Bearer <AGENT_TOKEN>
X-Instance-ID: 882d86be-fe53-49d1-a995-6d772e7d5e19
X-Protocol-Version: 1.0
X-Agent-Version: 0.1.0
```

| Cabeçalho | Obrigatório | Significado | Exemplo |
| :--- | :--- | :--- | :--- |
| `Authorization` | **Sim** | Token de autenticação Bearer atribuído à instalação do agente | `Bearer ignt_tok_9a8b7c6d...` |
| `X-Instance-ID` | **Sim** | UUID v4 único e permanente gerado localmente na instalação | `882d86be-fe53-49d1-a995...` |
| `X-Protocol-Version` | **Sim** | Versão do protocolo de comunicação utilizado | `1.0` |
| `X-Agent-Version` | **Sim** | Versão do software agente emissor | `0.1.0` |

---

## 3. Padrão Unificado de Respostas de Erro

Todas as respostas HTTP com códigos de erro (`4xx` e `5xx`) MUST retornar a seguinte estrutura JSON padronizada:

```json
{
  "error": {
    "code": "INVALID_SCHEMA",
    "message": "Field 'system.cpu_percent' is required.",
    "details": [
      {
        "field": "system.cpu_percent",
        "issue": "missing_required_property"
      }
    ],
    "timestamp": "2026-08-02T16:56:00.102Z"
  }
}
```

### Códigos de Erro Padronizados (`code`):

| Código de Erro | Status HTTP | Significado |
| :--- | :--- | :--- |
| `BAD_REQUEST` | 400 | Payload JSON malformado ou cabeçalhos ausentes |
| `UNAUTHORIZED` | 401 | Token Bearer ausente, inválido ou expirado |
| `FORBIDDEN` | 403 | Token válido, mas a instância do agente foi desativada |
| `DUPLICATE_REPORT` | 409 | Tentativa de reenvio de relatório com timestamp/ID idêntico |
| `INVALID_SCHEMA` | 422 | Payload JSON não atende à especificação `Report Schema v1` |
| `RATE_LIMIT_EXCEEDED` | 429 | Agente excedeu o limite de requisições permitidas por minuto |
| `INTERNAL_ERROR` | 500 | Erro não tratado no servidor central |

---

## 4. Catálogo de Endpoints

### 4.1 Ingestão de Relatório de Servidor (Evento Imutável)

#### `POST /v1/reports`

Recebe um relatório de servidor completo gerado pelo agente e o armazena como um evento imutável.

* **Payload da Requisição:** DEVE obedecer rigorosamente à especificação **[Report Schema v1](../specifications/report-schema-v1.md)**.

##### Exemplo de Requisição HTTP:
```http
POST /v1/reports HTTP/1.1
Host: api.ignoagent.com
Content-Type: application/json
Authorization: Bearer ignt_tok_9a8b7c6d5e4f
X-Instance-ID: 882d86be-fe53-49d1-a995-6d772e7d5e19
X-Protocol-Version: 1.0
X-Agent-Version: 0.1.0

{
    "agent": {
        "agent_id": "vps-prod-01",
        "environment": "production",
        "owner": "ignotec",
        "version": "0.1.0",
        "instance_id": "882d86be-fe53-49d1-a995-6d772e7d5e19"
    },
    "heartbeat": {
        "last_execution": "2026-08-02T16:56:00.000000",
        "status": "online"
    },
    "timestamp": "2026-08-02T16:56:00.000000",
    "server": { ... },
    "system": { ... },
    "services": { ... },
    "hardening": { ... },
    "security": { ... },
    "analysis": { ... },
    "network_analysis": { ... }
}
```

##### Resposta de Sucesso (`201 Created` / `202 Accepted`):
```json
{
  "status": "received",
  "report_id": "rep_9a8b7c6d5e4f1234",
  "instance_id": "882d86be-fe53-49d1-a995-6d772e7d5e19",
  "received_at": "2026-08-02T16:56:00.102Z",
  "next_sync_seconds": 300
}
```

---

### 4.2 Signal Heartbeat (Sinal de Vida Leve)

#### `POST /v1/heartbeat`

Ping ultraleve para confirmar que o agente está ativo sem enviar o relatório de métricas completo.

##### Corpo da Requisição:
```json
{
  "instance_id": "882d86be-fe53-49d1-a995-6d772e7d5e19",
  "status": "online",
  "timestamp": "2026-08-02T16:56:00.000000"
}
```

##### Resposta de Sucesso (`200 OK`):
```json
{
  "status": "acknowledged",
  "received_at": "2026-08-02T16:56:00.050Z",
  "next_poll_seconds": 300
}
```

---

### 4.3 Consulta de Configuração Remota

#### `GET /v1/config`

Permite ao agente consultar alterações remota de política de monitoramento (ex: alterar intervalo de coleta).

##### Resposta de Sucesso (`200 OK`):
```json
{
  "agent": {
    "interval_seconds": 300,
    "log_level": "INFO"
  },
  "collectors": {
    "system": true,
    "services": true,
    "hardening": true,
    "security": true
  }
}
```

---

### 4.4 Consulta de Versão e Compatibilidade

#### `GET /v1/version`

Endpoint público para verificação da versão ativa da API e compatibilidade do protocolo.

##### Resposta de Sucesso (`200 OK`):
```json
{
  "api_version": "1.0.0",
  "supported_protocol_versions": ["1.0"],
  "min_agent_version": "0.1.0"
}
```

---

## 5. Tabela de Códigos de Status HTTP

| Código | Nome HTTP | Condição de Uso na API Central |
| :--- | :--- | :--- |
| **`200 OK`** | OK | Sucesso para `GET /v1/config`, `GET /v1/version` e `POST /v1/heartbeat`. |
| **`201 Created`** | Created | Sucesso na ingestão e gravação de um novo evento de relatório (`POST /v1/reports`). |
| **`202 Accepted`** | Accepted | Relatório aceito e colocado na fila assíncrona de processamento da API Central. |
| **`400 Bad Request`** | Bad Request | JSON malformado, sintaxe inválida ou cabeçalhos obrigatórios ausentes. |
| **`401 Unauthorized`** | Unauthorized | Token `Authorization: Bearer` ausente ou inválido. |
| **`403 Forbidden`** | Forbidden | Token válido, mas o agente ou conta do cliente está suspensa/desativada. |
| **`409 Conflict`** | Conflict | Relatório duplicado com o mesmo identificador/timestamp de evento. |
| **`422 Unprocessable Entity`** | Unprocessable Entity | Erro de validação: o JSON é válido, mas violou o `Report Schema v1`. |
| **`429 Too Many Requests`** | Too Many Requests | Taxa de envio excedida (Rate Limit ativado). |
| **`500 Internal Server Error`** | Internal Server Error | Erro inesperado ou falha interna no servidor central. |

---

## 6. Regras de Compatibilidade e Evolução

1. **Tolerância a Campos Desconhecidos:** O servidor API DEVE aceitar e ignorar silenciosamente novos campos enviados por agentes mais recentes sem quebrar a ingestão.
2. **Respostas Não-Quebrantes:** A API pode adicionar novas chaves em respostas sem alterar a versão `/v1/`.
3. **Mudanças Incompatíveis:** Qualquer mudança que exija alteração no contrato de autenticação ou remoção de campos do `Report Schema v1` exigirá o lançamento do prefixo `/v2/` no endpoint (ex: `POST /v2/reports`).
