# Visão Geral da Arquitetura — IgnoAgent

## Visão Geral
O **IgnoAgent** é um sensor autônomo de monitoramento e observabilidade para servidores Linux (VPS, bare-metal e instâncias em nuvem).

O agente opera localmente no host, coletando dados de sistema, serviços, docker, logs de segurança e portas abertas, compilando esses dados em um **Server Report (Report Schema v1)** canônico.

---

## O Ciclo de Vida do Relatório (Report Lifecycle)

O **Report** é a entidade central do ecossistema IgnoAgent.

```text
[ IgnoAgent (Sensor) ]
          │
          ▼ (produz)
   [ Server Report (v1) ]
          │
  ┌───────┼─────────────────────────┐
  ▼       ▼                         ▼
[ Salva ] [ Enfileira em Outbox ] [ Envia via API ]
(status)        │                   │
                ▼                   ▼
     (Sincronização Assíncrona) (Dashboard / Alertas)
```

1. **Produção:** O agente coordena os coletores e executadores de análise para gerar o dicionário do relatório.
2. **Persistência Local:** Salva o relatório em `reports/status.json` e gera um histórico em `reports/history/YYYY-MM-DD_HHMMSS.json`.
3. **Fila Outbox:** Grava uma cópia do relatório na pasta `reports/outbox/` para garantir que dados não sejam perdidos mesmo se a rede ou a API central estiverem indisponíveis.
4. **Sincronização & Consumo:** Componentes de transporte (API, MQTT, CLI) consomem o relatório canônico e o enviam para o ecossistema central de monitoramento.

---

## Separação por Domínio

- **`collectors/`**: Somente letores/coletores de estado do SO. Não fazem análises nem persistem dados.
- **`analyzers/`**: Calculam scores de risco e avaliam vulnerabilidades. Não executam comandos de SO nem salvam arquivos.
- **`outputs/`**: Persistem os relatórios no disco local e tratam do envio para a fila outbox / API.
- **`utils/`**: Utilitários transversais de caminho, configuração, logging e serialização.
- **`models/`**: Representações dos dados do domínio em dataclasses Python.
