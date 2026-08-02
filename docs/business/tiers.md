# Estratégia de Produto e Planos de Uso (Tiers Specification)

* **Versão:** `1.0.0`
* **Status:** Visão de Negócio

## Visão Geral
Esta especificação define a estratégia de monetização e diferenciação dos planos de uso para a plataforma SaaS IgnoAgent.

> **Regra de Arquitetura Fundamental:**  
> O agente local (`IgnoAgent v0.1.0+`) instalado nas VPSs é **universal e canônico**. Ele sempre coleta e envia o payload completo ([Report Schema v1](../specifications/report-schema-v1.md)).  
> A diferenciação de planos é aplicada **exclusivamente na Plataforma Central (API/Dashboard)**, permitindo que upgrades de plano sejam instantâneos sem necessidade de intervenção ou reinstalação na VPS do cliente.

---

## Tabela de Planos de Uso

| Funcionalidade / Recurso | 🚀 **Starter** (Gratuito) | 🛡️ **Pro** (Assinatura) | 🏢 **Enterprise** (Corporativo) |
| :--- | :--- | :--- | :--- |
| **Público-Alvo** | Devs / Projetos Pessoais | Freelancers / PMEs | Agências / DevOps / TI Gerenciada |
| **Limite de Servidores (VPS)** | Até 2 VPSs | Até 10 VPSs | Ilimitado |
| **Intervalo de Monitoramento** | A cada 15 minutos | A cada 5 minutos | A cada 1 minuto |
| **Identificação da VPS** | Hostname básico | IP Público + Provedor + Bandeira do País | IP Público + Provedor + País + ASN + Tags |
| **Métricas de Hardware** | CPU %, RAM %, Disco % | CPU %, RAM %, Disco % + Histórico | CPU %, RAM %, Disco % + Histórico + Alertas |
| **Monitoramento Docker & Serviços** | ❌ Oculto | ✅ Exibição de contêineres e falhas | ✅ Exibição + Alerta de Queda de Serviços |
| **Análise de Segurança & SSH** | ❌ Oculto | ❌ Oculto | ✅ IPs Atacantes + Alerta de Exposição de Portas |
| **Alertas Instantâneos** | ❌ Sem alertas | ✅ Telegram & E-mail | ✅ WhatsApp, Telegram, Slack & Webhooks |
| **Retenção de Histórico** | 24 Horas | 30 Dias | 90 Dias |
| **Relatórios Executivos em PDF** | ❌ | ❌ | ✅ Exportação de Evidências em PDF para SLA |
