# IgnoAgent

**IgnoAgent** é um agente leve e autônomo de monitoramento de infraestrutura e análise de riscos de segurança para servidores Linux.

---

## 🚀 Instalação e Execução

### 1. Criar e ativar o ambiente virtual
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Instalar o pacote
```bash
pip install -e .
```

### 3. Executar o agente
```bash
# Execução direta via módulo
python -m ignoagent

# Ou usando o utilitário run.py
python run.py
```

---

## 📁 Estrutura do Projeto

```
ignoagent/
├── ignoagent/          # Pacote Python principal
│   ├── collectors/     # Coletores de dados do sistema e segurança
│   ├── analyzers/      # Análise de vulnerabilidades e scores de risco
│   ├── outputs/        # Persistência local (status, histórico, outbox)
│   ├── utils/          # Utilitários de filesystem, logger e config
│   └── models/         # Modelos de dados
├── config/             # Arquivos de configuração YAML
├── reports/            # Relatórios gerados (status.json, history, outbox)
├── tests/              # Testes unitários com pytest
└── pyproject.toml      # Configuração do pacote e dependências
```

---

## 🛠️ Executar Testes

```bash
pytest
```

---

## 📜 Licença

MIT License
