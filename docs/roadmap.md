# Roadmap de Desenvolvimento — IgnoAgent

## v0.1.0 — Agente Local Funcional (Atual)
- [x] Refatoração arquitetural para o pacote `ignoagent/`.
- [x] Coletores isolados (sistema, Docker, hardening, segurança, SSH).
- [x] Analisadores de risco e portas expostas.
- [x] Persistência local (`status.json`, histórico e outbox).
- [x] Suíte de testes automatizados com `pytest`.
- [x] Versionamento no Git e release inicial (`v0.1.0`).

## v0.2.0 — API Central & Contrato de Dados
- [ ] Definição do contrato de dados JSON estável e identificação/autenticação por instância.
- [ ] Construção do receptor da API Central (`POST /v1/reports`) para persistência dos relatórios das VPSs.
- [ ] Suporte a configuração remota de parâmetros (ex: intervalo de envio retornado na resposta da API).

## v0.3.0 — Sincronização Agente → API
- [ ] Sincronização automática e resiliente da pasta `reports/outbox/` com a API Central.

## v0.4.0 — Dashboard Web & Gestão Centralizada
- [ ] Interface gráfica para visualização unificada das VPS e serviços monitorados.
- [ ] **Controle dinâmico de frequência:** Permitir alterar a frequência de auditoria/envio do agente diretamente pela interface do Dashboard.

## v0.5.0 — Sistema de Alertas
- [ ] Alertas em tempo real (Telegram, Slack, Webhooks) para queda de VPS/serviços e riscos.

## v0.6.0 — Instalação Automática
- [ ] Script de instalação automatizado (`curl -fsSL https://... | bash`).

## v1.0.0 — Primeiro Cliente / Lançamento SaaS
- [ ] Plataforma de observabilidade para VPS de pequenas empresas/aplicações consolidada.
