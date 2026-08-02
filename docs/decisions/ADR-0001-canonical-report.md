# ADR-0001: Modelo de Dados Canônico do Relatório (Report Schema v1)

* **Status:** Aprovado
* **Data:** 2026-08-02
* **Autor:** Ignotec Engineering

## Contexto
O IgnoAgent é um sensor instalado em servidores Linux que coleta métricas de sistema, segurança, serviços e hardening. Atualmente, os relatórios gerados são salvos em arquivos locais (`reports/status.json`, `reports/history/` e `reports/outbox/`).

Com a evolução planejada para uma arquitetura distribuída (SaaS Multi-Servidor), múltiplos componentes — como a API Central, bancos de dados, painéis web e sistemas de alerta — precisarão consumir esses dados.

Sem um modelo de dados formalmente definido, qualquer alteração na estrutura do relatório local arriscaria quebrar os consumidores de API e a retrocompatibilidade.

## Decisão
Decidimos que o **Server Report (Report Schema v1)** é a entidade canônica central e a **única fonte da verdade** do ecossistema IgnoAgent.

1. **Independência de Protocolo e Linguagem:** A estrutura do relatório é independente da linguagem de implementação do agente (Python, Go, Rust) ou da camada de transporte (arquivo local, HTTP REST, MQTT, gRPC).
2. **Consumo por Referência:** A futura API Central, o Dashboard Web e os serviços de alerta consumirão este esquema canônico sem redefinir ou duplicar a estrutura dos campos.
3. **Regra de Extensibilidade Sem Quebra (Non-Breaking Extensibility):** Novos coletores e campos podem ser adicionados como chaves opcionais no esquema, mantendo retrocompatibilidade estrita.

## Consequências
* **Positivas:**
  * Desacoplamento total entre o agente coletor e a API Central/Dashboard.
  * Permite a criação futura de agentes em outras linguagens (ex: Go/Rust) ou plataformas (Windows, Kubernetes) mantendo o mesmo protocolo.
  * Garante estabilidade nos testes automatizados e validação de schema.
* **Desafios:**
  * Mudanças que alterem ou removam campos existentes exigirão versionamento explícito do esquema (`report-schema-v2.md`).
