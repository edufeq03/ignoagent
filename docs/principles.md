# Princípios de Engenharia — IgnoAgent

1. **Simplicidade Acima de Abstrações**: Não crie padrões ou camadas sem necessidade prática comprovada.
2. **Resiliência e Execução Silenciosa**: Falhas em coletores individuais não devem paralisar a geração dos demais relatórios.
3. **Respeito aos Contratos de Dados**: Mudanças estruturais no JSON produzido devem manter estrita compatibilidade retroativa.
4. **Sem Efeitos Colaterais Escondidos**: Coletores apenas coletam; analisadores apenas analisam; outputs apenas persistem.
