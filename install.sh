#!/usr/bin/env bash
# ==============================================================================
# IgnoAgent Automated Installer & Systemd Service Activator
# ==============================================================================

set -e

GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${CYAN}====================================================================${NC}"
echo -e "${CYAN}🚀 IgnoAgent — Instalador Autônomo & Agendador Systemd${NC}"
echo -e "${CYAN}====================================================================${NC}"

# 1. Verifica se está rodando como root/sudo
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}[ERROR] Este script de instalação precisa ser executado com sudo ou root.${NC}"
    echo -e "Uso: sudo ./install.sh"
    exit 1
fi

INSTALL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo -e "${GREEN}[✓] Diretório do IgnoAgent:${NC} ${INSTALL_DIR}"

# 2. Verifica dependências de sistema
echo -e "${CYAN}[1/5] Verificando dependências de sistema...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[ERROR] Python3 não foi encontrado. Por favor instale o python3.${NC}"
    exit 1
fi

# 3. Cria e configura o ambiente virtual
echo -e "${CYAN}[2/5] Configurando ambiente virtual Python (venv)...${NC}"
if [ ! -d "${INSTALL_DIR}/venv" ]; then
    python3 -m venv "${INSTALL_DIR}/venv"
fi

"${INSTALL_DIR}/venv/bin/pip" install --quiet --upgrade pip
"${INSTALL_DIR}/venv/bin/pip" install --quiet -e "${INSTALL_DIR}"
echo -e "${GREEN}[✓] Dependências Python instaladas com sucesso.${NC}"

# 4. Garante arquivos de configuração Padrão
echo -e "${CYAN}[3/5] Verificando arquivos de configuração...${NC}"
mkdir -p "${INSTALL_DIR}/config" "${INSTALL_DIR}/reports/outbox" "${INSTALL_DIR}/reports/history" "${INSTALL_DIR}/logs"

if [ ! -f "${INSTALL_DIR}/config/identity.yml" ]; then
    HOSTNAME_VAL=$(hostname)
    cat <<EOF > "${INSTALL_DIR}/config/identity.yml"
agent_id: ${HOSTNAME_VAL}
environment: production
owner: ignotec
installation_date: $(date +%Y-%m-%d)
version: 1.0.0
EOF
    echo -e "${GREEN}[✓] Criado arquivo identity.yml padrão (${HOSTNAME_VAL}).${NC}"
fi

# 5. Instala os serviços Systemd
echo -e "${CYAN}[4/5] Instalando e configurando serviço Systemd...${NC}"

SERVICE_DEST="/etc/systemd/system/ignoagent.service"
TIMER_DEST="/etc/systemd/system/ignoagent.timer"

cat <<EOF > "${SERVICE_DEST}"
[Unit]
Description=IgnoAgent Infrastructure Health & Security Audit Service
After=network-online.target
Wants=network-online.target

[Service]
Type=oneshot
User=root
WorkingDirectory=${INSTALL_DIR}
ExecStart=${INSTALL_DIR}/venv/bin/python -m ignoagent
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

cat <<EOF > "${TIMER_DEST}"
[Unit]
Description=IgnoAgent Periodic Execution Timer
Requires=ignoagent.service

[Timer]
Unit=ignoagent.service
OnCalendar=*:0/15
Persistent=true

[Install]
WantedBy=timers.target
EOF

# 6. Recarrega e Ativa o Systemd Timer
echo -e "${CYAN}[5/5] Ativando temporizador systemd...${NC}"
systemctl daemon-reload
systemctl enable --now ignoagent.timer

echo -e "${CYAN}====================================================================${NC}"
echo -e "${GREEN}🎉 IgnoAgent instalado e ativado com sucesso!${NC}"
echo -e "${CYAN}====================================================================${NC}"
echo -e "📌 STATUS DO TIMER:"
systemctl status ignoagent.timer --no-pager | head -n 10 || true
echo -e ""
echo -e "💡 COMANDOS ÚTEIS:"
echo -e "  • Execução manual teste:  ${INSTALL_DIR}/venv/bin/python ${INSTALL_DIR}/run.py"
echo -e "  • Ver logs do systemd:    sudo journalctl -u ignoagent -f"
echo -e "  • Verificar agendamento:  sudo systemctl status ignoagent.timer"
echo -e "  • Editar configurações:   nano ${INSTALL_DIR}/config/config.yml"
echo -e "${CYAN}====================================================================${NC}"
