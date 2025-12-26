"""
Assistente de WhatsApp para Controle Financeiro
Gerencia gastos, entradas, VR e VA
"""

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from datetime import datetime
import json
import os

app = Flask(__name__)

# Arquivo para armazenar dados
DATA_FILE = 'financas_data.json'

def carregar_dados():
    """Carrega dados do arquivo JSON"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            dados = json.load(f)
            # Garantir estrutura completa
            if 'usuario_atual' not in dados:
                dados['usuario_atual'] = 'Principal'
            if 'usuarios' not in dados:
                dados['usuarios'] = {
                    'Principal': {
                        'saldo': dados.get('saldo', 0),
                        'vr': dados.get('vr', 0),
                        'va': dados.get('va', 0),
                        'transacoes': dados.get('transacoes', []),
                        'contas_fixas': []
                    }
                }
            if 'mes_atual' not in dados:
                dados['mes_atual'] = datetime.now().strftime('%Y-%m')
            return dados
    
    return {
        'usuario_atual': 'Principal',
        'usuarios': {
            'Principal': {
                'saldo': 0,
                'vr': 0,
                'va': 0,
                'transacoes': [],
                'contas_fixas': []
            }
        },
        'mes_atual': datetime.now().strftime('%Y-%m')
    }

def obter_dados_usuario(dados):
    """Retorna os dados do usuário atual"""
    usuario = dados['usuario_atual']
    if usuario not in dados['usuarios']:
        dados['usuarios'][usuario] = {
            'saldo': 0,
            'vr': 0,
            'va': 0,
            'transacoes': [],
            'contas_fixas': []
        }
    return dados['usuarios'][usuario]

def salvar_dados(dados):
    """Salva dados no arquivo JSON"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)

def extrair_valor_e_descricao(texto):
    """Extrai valor e descrição de uma mensagem em linguagem natural"""
    import re
    
    # Procurar por padrões de valores: R$ 30, 30 reais, 30,50, 30.50
    padroes = [
        r'r?\$?\s*(\d+[,.]?\d*)\s*(?:reais?)?',  # 30 reais, R$ 30, 30.50
        r'(\d+[,.]?\d*)\s*(?:reais?|R\$)',  # 30 reais, 30 R$
    ]
    
    valor = None
    posicao = -1
    
    for padrao in padroes:
        match = re.search(padrao, texto, re.IGNORECASE)
        if match:
            valor = float(match.group(1).replace(',', '.'))
            posicao = match.start()
            break
    
    # Extrair descrição (tudo exceto o valor e palavras-chave)
    if valor and posicao >= 0:
        # Remove valor e palavras comuns
        descricao = re.sub(
            r'(?:gastei|usei|paguei|comprei|recebi|foi|de|no|na|em|com|r\$|reais?|\d+[,.]?\d*)',
            '',
            texto,
            flags=re.IGNORECASE
        ).strip()
        
        # Remove espaços extras
        descricao = re.sub(r'\s+', ' ', descricao)
        
        return valor, descricao if descricao else 'Sem descrição'
    
    return None, None

def processar_mensagem(mensagem):
    """Processa a mensagem e retorna a resposta"""
    dados = carregar_dados()
    msg = mensagem.lower().strip()
    msg_original = mensagem.strip()
    
    # Verificar se mudou de mês
    mes_atual = datetime.now().strftime('%Y-%m')
    if dados['mes_atual'] != mes_atual:
        dados['mes_atual'] = mes_atual
        # Resetar transações de todos os usuários
        for usuario in dados['usuarios']:
            dados['usuarios'][usuario]['transacoes'] = []
    
    usuario_dados = obter_dados_usuario(dados)
    
    # ===== COMANDOS DE SISTEMA =====
    
    # Comando: TROCAR USUÁRIO
    if msg.startswith('usuario ') or msg.startswith('usuário ') or msg.startswith('mudar para '):
        nome_usuario = msg.replace('usuario ', '').replace('usuário ', '').replace('mudar para ', '').strip().title()
        
        if not nome_usuario:
            return "❌ Digite o nome do usuário!\nEx: usuario Maria"
        
        dados['usuario_atual'] = nome_usuario
        
        if nome_usuario not in dados['usuarios']:
            dados['usuarios'][nome_usuario] = {
                'saldo': 0,
                'vr': 0,
                'va': 0,
                'transacoes': [],
                'contas_fixas': []
            }
            salvar_dados(dados)
            return f"✅ Usuário *{nome_usuario}* criado e selecionado!\n\n💡 Agora todas as transações serão registradas para {nome_usuario}."
        
        salvar_dados(dados)
        usuario_dados = dados['usuarios'][nome_usuario]
        return f"✅ Usuário alterado para *{nome_usuario}*\n\n💰 Saldo: R$ {usuario_dados['saldo']:.2f}\n🍽️ VR: R$ {usuario_dados['vr']:.2f}\n🛒 VA: R$ {usuario_dados['va']:.2f}"
    
    # Comando: VER USUÁRIO ATUAL
    if msg in ['usuario', 'usuário', 'qual usuario', 'quem sou']:
        return f"👤 Usuário atual: *{dados['usuario_atual']}*\n\n💡 Para trocar: usuario [nome]\nEx: usuario Maria"
    
    # Comando: LISTAR USUÁRIOS
    if msg in ['usuarios', 'usuários', 'listar usuarios', 'ver usuarios']:
        lista = "👥 *USUÁRIOS CADASTRADOS:*\n\n"
        for nome, info in dados['usuarios'].items():
            atual = "✅" if nome == dados['usuario_atual'] else "  "
            lista += f"{atual} *{nome}*\n"
            lista += f"   💰 Saldo: R$ {info['saldo']:.2f}\n"
            lista += f"   🍽️ VR: R$ {info['vr']:.2f}\n"
            lista += f"   🛒 VA: R$ {info['va']:.2f}\n\n"
        lista += "💡 Para trocar: usuario [nome]"
        return lista
    
    # Comando: APAGAR HISTÓRICO
    if msg in ['apagar historico', 'apagar histórico', 'limpar historico', 'limpar histórico', 'deletar historico']:
        usuario_dados['transacoes'] = []
        salvar_dados(dados)
        return f"🗑️ Histórico de transações apagado!\n\n💡 Seus saldos foram mantidos:\n💰 Saldo: R$ {usuario_dados['saldo']:.2f}\n🍽️ VR: R$ {usuario_dados['vr']:.2f}\n🛒 VA: R$ {usuario_dados['va']:.2f}"
    
    # Comando: ADICIONAR CONTA FIXA
    if msg.startswith('conta fixa ') or msg.startswith('pagamento fixo '):
        try:
            texto = msg.replace('conta fixa ', '').replace('pagamento fixo ', '')
            partes = texto.split(' ', 2)
            valor = float(partes[0].replace(',', '.'))
            dia = int(partes[1])
            descricao = partes[2] if len(partes) > 2 else 'Conta fixa'
            
            if dia < 1 or dia > 31:
                return "❌ Dia inválido! Use um dia entre 1 e 31."
            
            conta = {
                'valor': valor,
                'dia': dia,
                'descricao': descricao
            }
            
            usuario_dados['contas_fixas'].append(conta)
            salvar_dados(dados)
            
            return f"✅ Conta fixa cadastrada!\n💳 R$ {valor:.2f}\n📅 Todo dia {dia}\n📝 {descricao}\n\n💡 Use 'contas fixas' para ver todas"
        except:
            return "❌ Formato inválido!\n\nUse: conta fixa [valor] [dia] [descrição]\nEx: conta fixa 150 10 aluguel"
    
    # Comando: LISTAR CONTAS FIXAS
    if msg in ['contas fixas', 'pagamentos fixos', 'ver contas', 'contas']:
        if not usuario_dados['contas_fixas']:
            return "📋 Nenhuma conta fixa cadastrada.\n\n💡 Cadastre: conta fixa [valor] [dia] [descrição]\nEx: conta fixa 150 10 aluguel"
        
        total = sum(c['valor'] for c in usuario_dados['contas_fixas'])
        lista = "💳 *CONTAS FIXAS DO MÊS*\n\n"
        
        for i, conta in enumerate(sorted(usuario_dados['contas_fixas'], key=lambda x: x['dia']), 1):
            lista += f"{i}. 📅 Dia {conta['dia']}\n"
            lista += f"   💰 R$ {conta['valor']:.2f}\n"
            lista += f"   📝 {conta['descricao']}\n\n"
        
        lista += f"📊 *Total mensal:* R$ {total:.2f}"
        return lista
    
    # Comando: REMOVER CONTA FIXA
    if msg.startswith('remover conta ') or msg.startswith('deletar conta '):
        try:
            numero = int(msg.split()[-1])
            if numero < 1 or numero > len(usuario_dados['contas_fixas']):
                return f"❌ Conta #{numero} não encontrada!\nUse 'contas fixas' para ver a lista."
            
            conta_removida = usuario_dados['contas_fixas'].pop(numero - 1)
            salvar_dados(dados)
            
            return f"🗑️ Conta fixa removida!\n💳 R$ {conta_removida['valor']:.2f}\n📝 {conta_removida['descricao']}"
        except:
            return "❌ Formato inválido!\nUse: remover conta [número]\nEx: remover conta 1"
    
    # Comando: PAGAR CONTA FIXA
    if msg.startswith('pagar conta ') or msg.startswith('paguei conta '):
        try:
            numero = int(msg.split()[-1])
            if numero < 1 or numero > len(usuario_dados['contas_fixas']):
                return f"❌ Conta #{numero} não encontrada!"
            
            conta = usuario_dados['contas_fixas'][numero - 1]
            
            usuario_usuario_dados['saldo'] -= conta['valor']
            usuario_usuario_dados['transacoes'].append({
                'tipo': 'gasto',
                'valor': conta['valor'],
                'descricao': f"[CONTA FIXA] {conta['descricao']}",
                'data': datetime.now().strftime('%d/%m/%Y %H:%M'),
                'categoria': 'conta_fixa'
            })
            salvar_dados(dados)
            
            return f"✅ Pagamento registrado!\n💳 R$ {conta['valor']:.2f}\n📝 {conta['descricao']}\n💰 Saldo: R$ {usuario_dados['saldo']:.2f}"
        except:
            return "❌ Formato inválido!\nUse: pagar conta [número]\nEx: pagar conta 1"
    
    # ===== LINGUAGEM NATURAL =====
    
    # Detectar GASTO em linguagem natural
    if any(palavra in msg for palavra in ['gastei', 'paguei', 'comprei', 'saiu']) and \
       not any(palavra in msg for palavra in ['vr', 'vale refeição', 'va', 'vale alimentação']):
        valor, descricao = extrair_valor_e_descricao(msg_original)
        if valor:
            usuario_usuario_dados['saldo'] -= valor
            usuario_usuario_dados['transacoes'].append({
                'tipo': 'gasto',
                'valor': valor,
                'descricao': descricao,
                'data': datetime.now().strftime('%d/%m/%Y %H:%M'),
                'categoria': 'geral'
            })
            salvar_dados(dados)
            return f"✅ Gasto registrado!\n💸 R$ {valor:.2f} - {descricao}\n💰 Saldo: R$ {usuario_dados['saldo']:.2f}"
    
    # Detectar GASTO VR em linguagem natural
    if any(palavra in msg for palavra in ['vr', 'vale refeição', 'vale refeicao', 'vale-refeição']):
        if any(palavra in msg for palavra in ['creditaram', 'creditou', 'caiu', 'recebi', 'chegou']) or '+' in msg:
            # É crédito
            valor, _ = extrair_valor_e_descricao(msg_original)
            if valor:
                usuario_usuario_dados['vr'] += valor
                usuario_usuario_dados['transacoes'].append({
                    'tipo': 'credito_vr',
                    'valor': valor,
                    'descricao': 'Crédito VR',
                    'data': datetime.now().strftime('%d/%m/%Y %H:%M'),
                    'categoria': 'vr'
                })
                salvar_dados(dados)
                return f"✅ VR creditado!\n💳 + R$ {valor:.2f}\n🍽️ Saldo VR: R$ {usuario_dados['vr']:.2f}"
        else:
            # É gasto
            valor, descricao = extrair_valor_e_descricao(msg_original)
            if valor:
                if valor > usuario_dados['vr']:
                    return f"⚠️ Saldo insuficiente no VR!\n💳 Disponível: R$ {usuario_dados['vr']:.2f}"
                
                usuario_usuario_dados['vr'] -= valor
                usuario_usuario_dados['transacoes'].append({
                    'tipo': 'gasto_vr',
                    'valor': valor,
                    'descricao': descricao,
                    'data': datetime.now().strftime('%d/%m/%Y %H:%M'),
                    'categoria': 'vr'
                })
                salvar_dados(dados)
                return f"✅ Gasto VR registrado!\n🍽️ R$ {valor:.2f} - {descricao}\n💳 Saldo VR: R$ {usuario_dados['vr']:.2f}"
    
    # Detectar GASTO VA em linguagem natural
    if any(palavra in msg for palavra in ['va', 'vale alimentação', 'vale alimentacao', 'vale-alimentação']):
        if any(palavra in msg for palavra in ['creditaram', 'creditou', 'caiu', 'recebi', 'chegou']) or '+' in msg:
            # É crédito
            valor, _ = extrair_valor_e_descricao(msg_original)
            if valor:
                usuario_usuario_dados['va'] += valor
                usuario_usuario_dados['transacoes'].append({
                    'tipo': 'credito_va',
                    'valor': valor,
                    'descricao': 'Crédito VA',
                    'data': datetime.now().strftime('%d/%m/%Y %H:%M'),
                    'categoria': 'va'
                })
                salvar_dados(dados)
                return f"✅ VA creditado!\n💳 + R$ {valor:.2f}\n🛒 Saldo VA: R$ {usuario_dados['va']:.2f}"
        else:
            # É gasto
            valor, descricao = extrair_valor_e_descricao(msg_original)
            if valor:
                if valor > usuario_dados['va']:
                    return f"⚠️ Saldo insuficiente no VA!\n🛒 Disponível: R$ {usuario_dados['va']:.2f}"
                
                usuario_usuario_dados['va'] -= valor
                usuario_usuario_dados['transacoes'].append({
                    'tipo': 'gasto_va',
                    'valor': valor,
                    'descricao': descricao,
                    'data': datetime.now().strftime('%d/%m/%Y %H:%M'),
                    'categoria': 'va'
                })
                salvar_dados(dados)
                return f"✅ Gasto VA registrado!\n🛒 R$ {valor:.2f} - {descricao}\n💳 Saldo VA: R$ {usuario_dados['va']:.2f}"
    
    # Detectar ENTRADA em linguagem natural
    if any(palavra in msg for palavra in ['recebi', 'caiu', 'entrou', 'ganhei', 'salário', 'salario']):
        valor, descricao = extrair_valor_e_descricao(msg_original)
        if valor:
            usuario_usuario_dados['saldo'] += valor
            usuario_usuario_dados['transacoes'].append({
                'tipo': 'entrada',
                'valor': valor,
                'descricao': descricao,
                'data': datetime.now().strftime('%d/%m/%Y %H:%M'),
                'categoria': 'geral'
            })
            salvar_dados(dados)
            return f"✅ Entrada registrada!\n💵 R$ {valor:.2f} - {descricao}\n💰 Saldo: R$ {usuario_dados['saldo']:.2f}"
    
    # ===== COMANDOS DIRETOS (mantidos para compatibilidade) =====
    
    # Comando: Boas-vindas (primeira mensagem)
    if msg in ['oi', 'olá', 'ola', 'hey', 'opa']:
        return f"""👋 Olá! Sou seu assistente financeiro!

👤 *Usuário:* {dados['usuario_atual']}

💬 *Fale naturalmente comigo:*
• "gastei 50 na padaria"
• "usei VR no restaurante, 35 reais"
• "recebi salário de 3000"
• "creditaram 600 no VR"

📊 *Consultas:*
• saldo
• extrato
• resumo

👥 *Multi-usuário:*
• usuario [nome]
• usuarios

💳 *Contas fixas:*
• conta fixa [valor] [dia] [desc]
• contas fixas

❓ Digite *ajuda* para ver todos os comandos"""
    
    # Comando: AJUDA (menu completo)
    if msg in ['ajuda', 'help', 'menu', 'comandos']:
        return """📱 *ASSISTENTE FINANCEIRO - GUIA COMPLETO*

💬 *CONVERSE NATURALMENTE:*

*Registrar gastos:*
• "gastei 50 reais no almoço"
• "paguei 30 na padaria santa tereza"
• "comprei remédio, foi 45 reais"

*Usar Vale Refeição:*
• "usei o VR, 35 reais no restaurante"
• "gastei 28 com VR na lanchonete"

*Usar Vale Alimentação:*
• "usei o VA, 120 no mercado"
• "gastei 85 com VA no supermercado"

*Registrar entradas:*
• "recebi meu salário de 3000"
• "entrou 500 do freelance"

*Creditar vales:*
• "creditaram 600 no VR"
• "caiu 300 no VA"

💰 *CONSULTAS:*
• saldo - Ver todos os saldos
• extrato - Últimas 10 transações
• extrato completo - Ver TODAS
• resumo - Relatório do mês
• total - Estatísticas de transações

👥 *MULTI-USUÁRIO:*
• usuario [nome] - Trocar/criar usuário
• usuarios - Ver todos os usuários
• usuario - Ver usuário atual

💳 *CONTAS FIXAS:*
• conta fixa [valor] [dia] [desc]
  Ex: conta fixa 150 10 aluguel
• contas fixas - Ver todas as contas
• pagar conta [número] - Registrar pagamento
• remover conta [número] - Remover conta

🗑️ *GERENCIAR DADOS:*
• apagar historico - Limpa transações (mantém saldos)
• limpar tudo - Reseta usuário atual
• apagar ultima - Desfazer última transação
• zerar - Reinicia TUDO (todos usuários)

🤖 *OU USE COMANDOS DIRETOS:*
• gasto 50 almoço
• vr 30 padaria
• va 80 mercado
• entrada 3000 salário
• +vr 600 / +va 300

Fale comigo naturalmente! 😊"""
    
    # Comando: GASTO
    elif msg.startswith('gasto '):
        try:
            partes = msg[6:].split(' ', 1)
            valor = float(partes[0].replace(',', '.'))
            descricao = partes[1] if len(partes) > 1 else 'Sem descrição'
            
            usuario_dados['saldo'] -= valor
            usuario_dados['transacoes'].append({
                'tipo': 'gasto',
                'valor': valor,
                'descricao': descricao,
                'data': datetime.now().strftime('%d/%m/%Y %H:%M'),
                'categoria': 'geral'
            })
            salvar_dados(dados)
            
            return f"✅ Gasto registrado!\n💸 R$ {valor:.2f} - {descricao}\n💰 Saldo: R$ {usuario_dados['saldo']:.2f}"
        except:
            return "❌ Formato inválido!\nUse: gasto [valor] [descrição]\nEx: gasto 50 almoço"
    
    # Comando: VR (Vale Refeição)
    elif msg.startswith('vr '):
        try:
            partes = msg[3:].split(' ', 1)
            valor = float(partes[0].replace(',', '.'))
            descricao = partes[1] if len(partes) > 1 else 'Refeição'
            
            if valor > usuario_dados['vr']:
                return f"⚠️ Saldo insuficiente no VR!\n💳 Disponível: R$ {usuario_dados['vr']:.2f}"
            
            usuario_dados['vr'] -= valor
            usuario_dados['transacoes'].append({
                'tipo': 'gasto_vr',
                'valor': valor,
                'descricao': descricao,
                'data': datetime.now().strftime('%d/%m/%Y %H:%M'),
                'categoria': 'vr'
            })
            salvar_dados(dados)
            
            return f"✅ Gasto VR registrado!\n🍽️ R$ {valor:.2f} - {descricao}\n💳 Saldo VR: R$ {usuario_dados['vr']:.2f}"
        except:
            return "❌ Formato inválido!\nUse: vr [valor] [descrição]\nEx: vr 25 restaurante"
    
    # Comando: VA (Vale Alimentação)
    elif msg.startswith('va '):
        try:
            partes = msg[3:].split(' ', 1)
            valor = float(partes[0].replace(',', '.'))
            descricao = partes[1] if len(partes) > 1 else 'Alimentação'
            
            if valor > usuario_dados['va']:
                return f"⚠️ Saldo insuficiente no VA!\n🛒 Disponível: R$ {usuario_dados['va']:.2f}"
            
            usuario_dados['va'] -= valor
            usuario_dados['transacoes'].append({
                'tipo': 'gasto_va',
                'valor': valor,
                'descricao': descricao,
                'data': datetime.now().strftime('%d/%m/%Y %H:%M'),
                'categoria': 'va'
            })
            salvar_dados(dados)
            
            return f"✅ Gasto VA registrado!\n🛒 R$ {valor:.2f} - {descricao}\n💳 Saldo VA: R$ {usuario_dados['va']:.2f}"
        except:
            return "❌ Formato inválido!\nUse: va [valor] [descrição]\nEx: va 80 mercado"
    
    # Comando: ENTRADA
    elif msg.startswith('entrada '):
        try:
            partes = msg[8:].split(' ', 1)
            valor = float(partes[0].replace(',', '.'))
            descricao = partes[1] if len(partes) > 1 else 'Entrada'
            
            usuario_dados['saldo'] += valor
            usuario_dados['transacoes'].append({
                'tipo': 'entrada',
                'valor': valor,
                'descricao': descricao,
                'data': datetime.now().strftime('%d/%m/%Y %H:%M'),
                'categoria': 'geral'
            })
            salvar_dados(dados)
            
            return f"✅ Entrada registrada!\n💵 R$ {valor:.2f} - {descricao}\n💰 Saldo: R$ {usuario_dados['saldo']:.2f}"
        except:
            return "❌ Formato inválido!\nUse: entrada [valor] [descrição]\nEx: entrada 3000 salário"
    
    # Comando: +VR
    elif msg.startswith('+vr '):
        try:
            valor = float(msg[4:].replace(',', '.'))
            usuario_dados['vr'] += valor
            usuario_dados['transacoes'].append({
                'tipo': 'credito_vr',
                'valor': valor,
                'descricao': 'Crédito VR',
                'data': datetime.now().strftime('%d/%m/%Y %H:%M'),
                'categoria': 'vr'
            })
            salvar_dados(dados)
            
            return f"✅ VR creditado!\n💳 + R$ {valor:.2f}\n🍽️ Saldo VR: R$ {usuario_dados['vr']:.2f}"
        except:
            return "❌ Formato inválido!\nUse: +vr [valor]\nEx: +vr 500"
    
    # Comando: +VA
    elif msg.startswith('+va '):
        try:
            valor = float(msg[4:].replace(',', '.'))
            usuario_dados['va'] += valor
            usuario_dados['transacoes'].append({
                'tipo': 'credito_va',
                'valor': valor,
                'descricao': 'Crédito VA',
                'data': datetime.now().strftime('%d/%m/%Y %H:%M'),
                'categoria': 'va'
            })
            salvar_dados(dados)
            
            return f"✅ VA creditado!\n💳 + R$ {valor:.2f}\n🛒 Saldo VA: R$ {usuario_dados['va']:.2f}"
        except:
            return "❌ Formato inválido!\nUse: +va [valor]\nEx: +va 300"
    
    # Comando: SALDO
    elif msg in ['saldo', 'saldos', 'extrato saldo']:
        return f"""💰 *SALDOS ATUAIS*

💵 *Saldo Geral:* R$ {usuario_dados['saldo']:.2f}
🍽️ *Vale Refeição:* R$ {usuario_dados['vr']:.2f}
🛒 *Vale Alimentação:* R$ {usuario_dados['va']:.2f}

📊 *Total Disponível:*
R$ {usuario_dados['saldo'] + usuario_dados['vr'] + usuario_dados['va']:.2f}"""
    
    # Comando: EXTRATO
    elif msg in ['extrato', 'historico', 'transacoes']:
        if not usuario_dados['transacoes']:
            return "📋 Nenhuma transação registrada ainda."
        
        ultimas = usuario_dados['transacoes'][-10:]
        texto = "📋 *ÚLTIMAS 10 TRANSAÇÕES*\n\n"
        
        for t in reversed(ultimas):
            emoji = {
                'entrada': '💵',
                'gasto': '💸',
                'gasto_vr': '🍽️',
                'gasto_va': '🛒',
                'credito_vr': '💳',
                'credito_va': '💳'
            }.get(t['tipo'], '📌')
            
            sinal = '+' if 'entrada' in t['tipo'] or 'credito' in t['tipo'] else '-'
            texto += f"{emoji} {sinal}R$ {t['valor']:.2f}\n"
            texto += f"   {t['descricao']}\n"
            texto += f"   {t['data']}\n\n"
        
        total_transacoes = len(usuario_dados['transacoes'])
        if total_transacoes > 10:
            texto += f"💡 Total: {total_transacoes} transações\n"
            texto += "Use 'extrato completo' para ver todas"
        
        return texto.strip()
    
    # Comando: EXTRATO COMPLETO
    elif msg in ['extrato completo', 'historico completo', 'ver tudo', 'ver todas']:
        if not usuario_dados['transacoes']:
            return "📋 Nenhuma transação registrada ainda."
        
        texto = f"📋 *TODAS AS TRANSAÇÕES ({len(usuario_dados['transacoes'])})*\n\n"
        
        for t in reversed(usuario_dados['transacoes']):
            emoji = {
                'entrada': '💵',
                'gasto': '💸',
                'gasto_vr': '🍽️',
                'gasto_va': '🛒',
                'credito_vr': '💳',
                'credito_va': '💳'
            }.get(t['tipo'], '📌')
            
            sinal = '+' if 'entrada' in t['tipo'] or 'credito' in t['tipo'] else '-'
            texto += f"{emoji} {sinal}R$ {t['valor']:.2f} - {t['descricao']}\n"
            texto += f"   {t['data']}\n\n"
        
        return texto.strip()
    
    # Comando: LIMPAR TUDO (apaga histórico e zera saldos do usuário atual)
    elif msg in ['limpar tudo', 'resetar', 'limpar dados']:
        usuario_dados['saldo'] = 0
        usuario_dados['vr'] = 0
        usuario_dados['va'] = 0
        usuario_dados['transacoes'] = []
        usuario_dados['contas_fixas'] = []
        salvar_dados(dados)
        return f"🗑️ *Dados limpos!*\n\n✅ Usuário *{dados['usuario_atual']}* resetado:\n💰 Saldos zerados\n📋 Histórico apagado\n💳 Contas fixas removidas\n\n💡 Outros usuários não foram afetados"
    
    # Comando: APAGAR ÚLTIMA TRANSAÇÃO
    elif msg in ['apagar ultima', 'apagar última', 'desfazer', 'cancelar ultima']:
        if not usuario_dados['transacoes']:
            return "❌ Nenhuma transação para apagar!"
        
        ultima = usuario_dados['transacoes'].pop()
        
        # Reverter o valor
        if ultima['tipo'] == 'gasto':
            usuario_dados['saldo'] += ultima['valor']
        elif ultima['tipo'] == 'entrada':
            usuario_dados['saldo'] -= ultima['valor']
        elif ultima['tipo'] == 'gasto_vr':
            usuario_dados['vr'] += ultima['valor']
        elif ultima['tipo'] == 'credito_vr':
            usuario_dados['vr'] -= ultima['valor']
        elif ultima['tipo'] == 'gasto_va':
            usuario_dados['va'] += ultima['valor']
        elif ultima['tipo'] == 'credito_va':
            usuario_dados['va'] -= ultima['valor']
        
        salvar_dados(dados)
        
        return f"🔙 *Última transação desfeita!*\n\n❌ {ultima['descricao']}\n💰 R$ {ultima['valor']:.2f}\n⏰ {ultima['data']}\n\n💰 Saldo atual: R$ {usuario_dados['saldo']:.2f}"
    
    # Comando: CONTAR TRANSAÇÕES
    elif msg in ['total', 'contar', 'quantas transacoes']:
        total = len(usuario_dados['transacoes'])
        gastos = len([t for t in usuario_dados['transacoes'] if 'gasto' in t['tipo']])
        entradas = len([t for t in usuario_dados['transacoes'] if 'entrada' in t['tipo'] or 'credito' in t['tipo']])
        
        return f"""📊 *ESTATÍSTICAS*

📝 Total de transações: {total}
💸 Gastos: {gastos}
💵 Entradas: {entradas}

💡 Use 'extrato' para ver as últimas 10
💡 Use 'extrato completo' para ver todas"""
    
    # Comando: RESUMO
    elif msg in ['resumo', 'relatorio', 'mes']:
        total_entradas = sum(t['valor'] for t in usuario_dados['transacoes'] 
                            if t['tipo'] in ['entrada', 'credito_vr', 'credito_va'])
        total_gastos = sum(t['valor'] for t in usuario_dados['transacoes'] 
                          if 'gasto' in t['tipo'])
        
        gastos_vr = sum(t['valor'] for t in usuario_dados['transacoes'] if t['tipo'] == 'gasto_vr')
        gastos_va = sum(t['valor'] for t in usuario_dados['transacoes'] if t['tipo'] == 'gasto_va')
        gastos_geral = sum(t['valor'] for t in usuario_dados['transacoes'] if t['tipo'] == 'gasto')
        
        return f"""📊 *RESUMO DO MÊS*

💰 *SALDOS ATUAIS:*
• Geral: R$ {usuario_dados['saldo']:.2f}
• VR: R$ {usuario_dados['vr']:.2f}
• VA: R$ {usuario_dados['va']:.2f}

📈 *MOVIMENTAÇÃO:*
• Total Entradas: R$ {total_entradas:.2f}
• Total Gastos: R$ {total_gastos:.2f}

💸 *GASTOS POR CATEGORIA:*
• Geral: R$ {gastos_geral:.2f}
• Vale Refeição: R$ {gastos_vr:.2f}
• Vale Alimentação: R$ {gastos_va:.2f}

📝 *Transações:* {len(usuario_dados['transacoes'])}"""
    
    # Comando: ZERAR
    elif msg == 'zerar':
        dados = {
            'usuario_atual': 'Principal',
            'usuarios': {
                'Principal': {
                    'saldo': 0,
                    'vr': 0,
                    'va': 0,
                    'transacoes': [],
                    'contas_fixas': []
                }
            },
            'mes_atual': datetime.now().strftime('%Y-%m')
        }
        salvar_dados(dados)
        return "✅ Dados zerados com sucesso!\n\n⚠️ Todos os usuários e dados foram apagados!"
    
    else:
        return "❓ Comando não reconhecido.\nEnvie *ajuda* para ver os comandos disponíveis."

@app.route('/whatsapp', methods=['POST'])
def whatsapp_webhook():
    """Webhook para receber mensagens do WhatsApp via Twilio"""
    mensagem_recebida = request.form.get('Body', '')
    
    resposta_texto = processar_mensagem(mensagem_recebida)
    
    resp = MessagingResponse()
    resp.message(resposta_texto)
    
    return str(resp)

@app.route('/teste', methods=['GET', 'POST'])
def teste():
    """Endpoint de teste sem Twilio"""
    if request.method == 'POST':
        mensagem = request.json.get('mensagem', '')
        return {'resposta': processar_mensagem(mensagem)}
    return {'status': 'ok', 'mensagem': 'Envie POST com {"mensagem": "seu comando"}'}

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
