# Contrato da API Central — v1 Specification

* **Versão:** 1.0.0
* **Referência de Payload:** [Report Schema v1](../specifications/report-schema-v1.md)

## Visão Geral
Este documento especifica o contrato HTTP da futura API Central do IgnoAgent para recepção e sincronização dos relatórios produzidos pelos agentes instalados em servidores remotos.

---

## Endpoint: Envio de Relatório

### `POST /v1/reports`

Recebe um **Server Report** completo gerado pelo agente.

#### Cabeçalhos de Requisição (Headers)

```http
POST /v1/reports HTTP/1.1
Host: api.ignoagent.com
Content-Type: application/json
Authorization: Bearer <INSTANCE_TOKEN_OU_API_KEY>
X-Agent-Version: 0.1.0
```

#### Corpo da Requisição (Request Payload)

O corpo da requisição DEVE seguir rigorosamente a especificação do **[Report Schema v1](../specifications/report-schema-v1.md)**.

Exemplo reduzido:
```json
{
  "agent": {
    "agent_id": "vps-prod-01",
    "environment": "production",
    "owner": "ignotec",
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
    "os": "Linux-6.8.0-136-generic-x86_64",
    "python": "3.11.9"
  },
  "system": { ... },
  "services": { ... },
  "hardening": { ... },
  "security": { ... },
  "analysis": { ... },
  "network_analysis": { ... }
}
```

---

#### Respostas da API (Responses)

##### 1. Sucesso (`201 Created` / `200 OK`)
```json
{
  "status": "received",
  "instance_id": "882d86be-fe53-49d1-a995-6d772e7d5e19",
  "received_at": "2026-08-02T15:45:43.102Z",
  "next_poll_seconds": 300
}
```

##### 2. Erro de Autenticação (`401 Unauthorized`)
```json
{
  "error": "unauthorized",
  "message": "Token de instância inválido ou expirado"
}
```

##### 3. Erro de Validação de Schema (`422 Unprocessable Entity`)
```json
{
  "error": "schema_validation_error",
  "message": "Campo obrigatório 'agent.instance_id' ausente"
}
```
