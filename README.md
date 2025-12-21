# 💰 Assistente Financeiro WhatsApp

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![Twilio](https://img.shields.io/badge/Twilio-WhatsApp-brightgreen.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**Controle suas finanças conversando naturalmente pelo WhatsApp!**

[Características](#-características) •
[Demo](#-demonstração) •
[Instalação](#-instalação) •
[Uso](#-como-usar) •
[Documentação](#-documentação) •
[Contribuir](#-contribuindo)

</div>

---

## 📱 Sobre o Projeto

Um assistente financeiro completo e inteligente para WhatsApp que permite gerenciar suas finanças pessoais através de **conversação natural**. Não precisa decorar comandos complexos - basta falar como você falaria com um amigo!

Desenvolvido em Python com Flask e integrado ao WhatsApp via Twilio, o sistema oferece:

- 💬 **Linguagem Natural**: Converse normalmente, sem comandos decorados
- 👥 **Multi-usuário**: Perfeito para casais e famílias
- 💳 **Gestão de Vales**: Controle separado de VR e VA
- 📊 **Contas Fixas**: Nunca mais esqueça de pagar contas
- 🗑️ **Controle Total**: Gerencie histórico e dados facilmente
- 📈 **Relatórios**: Acompanhe gastos e entradas automaticamente

---

## ✨ Características

### 🎯 Principais Funcionalidades

#### 💬 **Conversação Natural**
Fale naturalmente com o bot:
```
"gastei 50 na padaria"
"usei VR no restaurante, 35 reais"
"recebi meu salário de 3000"
"creditaram 600 no vale refeição"
```

#### 👥 **Sistema Multi-usuário**
- Múltiplos usuários no mesmo WhatsApp
- Cada pessoa tem seus próprios saldos
- Perfeito para controle familiar
- Visão consolidada de todos os usuários

#### 💰 **Controle Financeiro Completo**
- **Saldo Geral**: Dinheiro em conta
- **Vale Refeição (VR)**: Gestão separada
- **Vale Alimentação (VA)**: Gestão separada
- **Validação**: Impede gastos acima do saldo disponível

#### 💳 **Contas Fixas Mensais**
- Cadastre todas as contas do mês
- Receba lembretes visuais
- Registre pagamentos facilmente
- Acompanhe o total mensal

#### 📊 **Relatórios e Análises**
- Extrato detalhado de transações
- Resumo mensal automático
- Estatísticas de gastos por categoria
- Histórico completo sempre disponível

#### 🗑️ **Gestão de Dados**
- Apagar histórico (mantendo saldos)
- Desfazer última transação
- Resetar usuário específico
- Limpeza completa do sistema

---

## 🎬 Demonstração

### Fluxo Típico de Uso

```
👤 Pedro: oi
🤖 Bot: 👋 Olá! Sou seu assistente financeiro!
        Usuário: Pedro
        [Menu com opções]

👤 Pedro: recebi salário de 5000
🤖 Bot: ✅ Entrada registrada!
        💵 R$ 5000.00 - salário
        💰 Saldo: R$ 5000.00

👤 Pedro: creditaram 600 no VR
🤖 Bot: ✅ VR creditado!
        💳 + R$ 600.00
        🍽️ Saldo VR: R$ 600.00

👤 Pedro: conta fixa 1200 5 aluguel
🤖 Bot: ✅ Conta fixa cadastrada!
        💳 R$ 1200.00
        📅 Todo dia 5
        📝 aluguel

👤 Pedro: gastei 30 na padaria santa tereza
🤖 Bot: ✅ Gasto registrado!
        💸 R$ 30.00 - padaria santa tereza
        💰 Saldo: R$ 4970.00

👤 Pedro: usei VR no restaurante, 45 reais
🤖 Bot: ✅ Gasto VR registrado!
        🍽️ R$ 45.00 - restaurante
        💳 Saldo VR: R$ 555.00

👤 Pedro: usuario Maria
🤖 Bot: ✅ Usuário Maria criado e selecionado!

👤 Maria: recebi 4000 de salário
🤖 Bot: ✅ Entrada registrada!
        💵 R$ 4000.00 - salário
        💰 Saldo: R$ 4000.00

👤 Maria: usuarios
🤖 Bot: 👥 USUÁRIOS CADASTRADOS:
        
        ✅ Maria
           💰 Saldo: R$ 4.000.00
           🍽️ VR: R$ 0.00
           🛒 VA: R$ 0.00
        
           Pedro
           💰 Saldo: R$ 4.970.00
           🍽️ VR: R$ 555.00
           🛒 VA: R$ 0.00

👤 Pedro: resumo
🤖 Bot: 📊 RESUMO DO MÊS
        [Relatório completo com estatísticas]
```

---

## 🚀 Instalação

### Pré-requisitos

- Python 3.8 ou superior
- Conta no Twilio (gratuita)
- WhatsApp
- ngrok (para testes locais) ou servidor web (para produção)

### Passo 1: Clonar o Repositório

```bash
git clone https://github.com/seu-usuario/assistente-financeiro-whatsapp.git
cd assistente-financeiro-whatsapp
```

### Passo 2: Criar Ambiente Virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Passo 3: Instalar Dependências

```bash
pip install -r requirements.txt
```

### Passo 4: Configurar Twilio

1. Crie uma conta gratuita em [twilio.com](https://www.twilio.com)
2. Ative o WhatsApp Sandbox
3. Anote suas credenciais

Veja o [Guia Completo do Twilio](docs/GUIA_TWILIO.md) para instruções detalhadas.

### Passo 5: Executar Localmente

```bash
# Terminal 1: Iniciar o servidor
python whatsapp_financas.py

# Terminal 2: Iniciar ngrok (para conectar ao WhatsApp)
ngrok http 5000
```

### Passo 6: Configurar Webhook

1. Copie a URL do ngrok (ex: `https://abc123.ngrok.io`)
2. No Twilio, configure o webhook: `https://abc123.ngrok.io/whatsapp`
3. Selecione método **POST**
4. Salve

### Passo 7: Conectar seu WhatsApp

1. No Twilio, copie o número e código (ex: `join happy-duck`)
2. Envie pelo WhatsApp: `join happy-duck`
3. Aguarde confirmação
4. Pronto! 🎉

---

## 💻 Como Usar

### Comandos Principais

#### 💬 Linguagem Natural (Recomendado)

**Registrar Gastos:**
```
gastei 50 no almoço
paguei 30 na padaria santa tereza
comprei remédio, foi 45 reais
```

**Usar Vales:**
```
usei VR no restaurante, 35 reais
gastei 120 com VA no supermercado
VR de 40 na lanchonete
```

**Registrar Entradas:**
```
recebi meu salário de 3000
entrou 500 do freelance
ganhei 200 reais
```

**Creditar Vales:**
```
creditaram 600 no VR
caiu 300 no VA
recebi 500 de vale refeição
```

#### 🤖 Comandos Diretos (Também Funcionam)

```bash
gasto 50 almoço           # Registrar gasto
vr 30 padaria             # Usar VR
va 80 mercado             # Usar VA
entrada 3000 salário      # Registrar entrada
+vr 600                   # Creditar VR
+va 300                   # Creditar VA
```

#### 📊 Consultas

```bash
saldo                     # Ver todos os saldos
extrato                   # Últimas 10 transações
extrato completo          # Todas as transações
resumo                    # Relatório do mês
total                     # Estatísticas
```

#### 👥 Multi-usuário

```bash
usuario Maria             # Trocar/criar usuário
usuario                   # Ver usuário atual
usuarios                  # Listar todos
```

#### 💳 Contas Fixas

```bash
conta fixa 1200 5 aluguel       # Cadastrar conta
conta fixa 150 10 internet
contas fixas                     # Ver todas
pagar conta 1                    # Registrar pagamento
remover conta 2                  # Remover conta
```

#### 🗑️ Gestão de Dados

```bash
apagar historico          # Limpar transações (mantém saldos)
limpar tudo               # Resetar usuário atual
apagar ultima             # Desfazer última transação
zerar                     # Resetar sistema completo
```

---

## 📚 Documentação

### Guias Disponíveis

- 📘 **[Guia VS Code](docs/GUIA_VSCODE.md)** - Setup completo no VS Code
- 📗 **[Guia de Comandos](docs/GUIA_COMANDOS.md)** - Todos os comandos com exemplos
- 📙 **[Guia de Conversação](docs/GUIA_CONVERSACAO.md)** - Como conversar naturalmente
- 📕 **[Guia Twilio](docs/GUIA_TWILIO.md)** - Configuração do WhatsApp
- 📔 **[Novos Recursos](docs/GUIA_NOVOS_RECURSOS.md)** - Multi-usuário e contas fixas

### Estrutura do Projeto

```
assistente-financeiro-whatsapp/
├── whatsapp_financas.py          # Código principal
├── requirements.txt               # Dependências
├── financas_data.json            # Dados (criado automaticamente)
├── README.md                      # Este arquivo
├── LICENSE                        # Licença MIT
│
├── docs/                          # Documentação
│   ├── GUIA_VSCODE.md
│   ├── GUIA_COMANDOS.md
│   ├── GUIA_CONVERSACAO.md
│   ├── GUIA_TWILIO.md
│   └── GUIA_NOVOS_RECURSOS.md
│
├── .env.example                   # Exemplo de variáveis de ambiente
└── .gitignore                     # Arquivos ignorados pelo Git
```

---

## 🔧 Tecnologias

- **[Python 3.8+](https://www.python.org/)** - Linguagem principal
- **[Flask](https://flask.palletsprojects.com/)** - Framework web
- **[Twilio](https://www.twilio.com/)** - API do WhatsApp
- **[ngrok](https://ngrok.com/)** - Túnel para testes locais

---

## 🚀 Deploy em Produção

### Opção 1: Railway (Recomendado)

1. Fork este repositório
2. Crie conta em [railway.app](https://railway.app)
3. Conecte seu GitHub
4. Faça deploy automático
5. Configure variável de ambiente `PORT=5000`
6. Use a URL fornecida no webhook do Twilio

### Opção 2: Render

1. Fork este repositório
2. Crie conta em [render.com](https://render.com)
3. Novo Web Service → Conecte GitHub
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `python whatsapp_financas.py`
6. Deploy!

### Opção 3: Heroku

```bash
heroku create seu-app-financas
git push heroku main
heroku config:set PORT=5000
```

Configure a URL do Heroku no webhook do Twilio.

---

## 📊 Estrutura de Dados

Os dados são armazenados em `financas_data.json`:

```json
{
  "usuario_atual": "Pedro",
  "mes_atual": "2025-12",
  "usuarios": {
    "Pedro": {
      "saldo": 4970.0,
      "vr": 555.0,
      "va": 0.0,
      "transacoes": [
        {
          "tipo": "entrada",
          "valor": 5000.0,
          "descricao": "salário",
          "data": "21/12/2025 10:30",
          "categoria": "geral"
        },
        {
          "tipo": "gasto_vr",
          "valor": 45.0,
          "descricao": "restaurante",
          "data": "21/12/2025 12:45",
          "categoria": "vr"
        }
      ],
      "contas_fixas": [
        {
          "valor": 1200.0,
          "dia": 5,
          "descricao": "aluguel"
        }
      ]
    },
    "Maria": {
      "saldo": 4000.0,
      "vr": 0.0,
      "va": 0.0,
      "transacoes": [],
      "contas_fixas": []
    }
  }
}
```

---

## 🔒 Segurança

### ⚠️ Considerações Importantes

- **Dados Sensíveis**: O arquivo JSON contém informações financeiras
- **Não commite**: Adicione `financas_data.json` ao `.gitignore`
- **HTTPS**: Use sempre HTTPS em produção
- **Backup**: Faça backup regular dos dados
- **Autenticação**: Configure autenticação do webhook no Twilio

### Recomendações

1. Use variáveis de ambiente para credenciais
2. Não compartilhe `financas_data.json`
3. Configure rate limiting
4. Use HTTPS em produção
5. Implemente autenticação adicional se necessário

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Siga estes passos:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abra um Pull Request

### Ideias de Melhorias

- [ ] Interface web para visualização
- [ ] Gráficos de evolução mensal
- [ ] Exportar relatórios em PDF
- [ ] Metas de economia
- [ ] Alertas de gastos excessivos
- [ ] Categorias personalizadas
- [ ] Integração com bancos (Open Banking)
- [ ] App mobile nativo
- [ ] Reconhecimento de voz
- [ ] Análise de padrões com IA

---

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 👤 Autor

**Pedro Souza**

- GitHub: [@seu-usuario](https://github.com/seu-usuario)
- LinkedIn: [seu-perfil](https://linkedin.com/in/seu-perfil)
- Email: seu-email@exemplo.com

---

## 🙏 Agradecimentos

- [Twilio](https://www.twilio.com/) - API do WhatsApp
- [Flask](https://flask.palletsprojects.com/) - Framework web
- [ngrok](https://ngrok.com/) - Túneis seguros
- Comunidade Python - Suporte e inspiração

---

## 📞 Suporte

Encontrou um bug? Tem uma sugestão? 

- 🐛 Abra uma [Issue](https://github.com/seu-usuario/assistente-financeiro-whatsapp/issues)
- 💬 Inicie uma [Discussão](https://github.com/seu-usuario/assistente-financeiro-whatsapp/discussions)
- ⭐ Deixe uma estrela se gostou do projeto!

---

## 📈 Status do Projeto

✅ **Versão Estável** - Pronto para uso

### Roadmap

- [x] Conversação natural
- [x] Multi-usuário
- [x] Contas fixas
- [x] Gestão de vales (VR/VA)
- [x] Relatórios e estatísticas
- [ ] Interface web
- [ ] Gráficos visuais
- [ ] Exportação de dados
- [ ] App mobile
- [ ] Integração bancária

---

<div align="center">

**Feito com ❤️ e Python**

[⬆ Voltar ao topo](#-assistente-financeiro-whatsapp)

</div>
