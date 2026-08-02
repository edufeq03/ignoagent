# Arquitetura — IgnoAgent

## Princípios Arquiteturais
O IgnoAgent adota os princípios de **Clean Architecture**, **Separation of Concerns** (Separação de Responsabilidades) e **Single Responsibility Principle**.

## Estrutura do Pacote (`ignoagent/`)

* **`ignoagent.collectors`**: Responsáveis estritamente pela coleta de dados (sistema, Docker, hardening, segurança). Não realizam análises nem gravações em disco.
* **`ignoagent.analyzers`**: Recebem métricas coletadas e calculam scores de risco e severidade. Não executam comandos de sistema nem escrevem arquivos.
* **`ignoagent.outputs`**: Responsáveis pela persistência dos relatórios (gravação local em `reports/status.json`, histórico e outbox para sincronização).
* **`ignoagent.utils`**: Utilitários transversais (configuração, sistema de arquivos, logging e identificação).
* **`ignoagent.models`**: Modelos de dados (dataclasses) para relatório, heartbeat e identidade.

## Diagrama de Fluxo

```
[ Coletores ] ──► [ Dados Brutos ] ──► [ Analisadores ] ──► [ Relatório Compilado ]
                                                                     │
                                                                     ▼
                                                             [ Output Writers ]
                                                            ┌────────┴────────┐
                                                            ▼                 ▼
                                                     [ status.json ]   [ Outbox / API ]
```
