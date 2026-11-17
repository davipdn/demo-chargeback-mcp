"""Dados FICTÍCIOS para a demonstração. Nada aqui vem da YouShop."""
from datetime import datetime

# "Agora" fixo, para a demo dar sempre o mesmo resultado
AGORA_DEMO = datetime(2026, 11, 18, 10, 0)

CHARGEBACKS = {
    "CB-001": {
        "pedido": "PED-1001",
        "motivo": "compra_nao_reconhecida",
        "valor": 297.00,
        "notificado_em": datetime(2026, 11, 17, 15, 0),
    },
    "CB-002": {
        "pedido": "PED-1002",
        "motivo": "produto_nao_recebido",
        "valor": 189.90,
        "notificado_em": datetime(2026, 11, 17, 9, 0),
    },
    "CB-003": {
        "pedido": "PED-1003",
        "motivo": "cobranca_em_dobro",
        "valor": 97.00,
        "notificado_em": datetime(2026, 11, 17, 18, 0),
    },
}

PEDIDOS = {
    "PED-1001": {
        "tipo": "digital",
        "produto": "Curso Fictício de Fotografia",
        "comprador": {"nome": "Ana Souza", "email": "ana.souza@exemplo.com"},
        "pagamento": "cartao_credito",
        "criado_em": "2026-10-20 21:14",
    },
    "PED-1002": {
        "tipo": "fisico",
        "produto": "Kit Fictício de Cosméticos",
        "comprador": {"nome": "Bruno Lima", "endereco": "Rua A, 10 - Recife/PE"},
        "pagamento": "cartao_credito",
        "criado_em": "2026-10-25 14:02",
    },
    "PED-1003": {
        "tipo": "digital",
        "produto": "E-book Fictício de Finanças",
        "comprador": {"nome": "Carla Dias", "email": "carla.dias@exemplo.com"},
        "pagamento": "cartao_credito",
        "criado_em": "2026-10-30 08:40",
    },
}

LOGS_ACESSO = {
    "PED-1001": [
        {"data": "2026-10-20 21:20", "evento": "login na área de membros", "ip": "187.10.0.1"},
        {"data": "2026-10-21 08:02", "evento": "aula 1 concluída", "ip": "187.10.0.1"},
        {"data": "2026-10-23 19:30", "evento": "aula 2 concluída", "ip": "187.10.0.1"},
    ],
    "PED-1003": [],
}

RASTREIOS = {
    "PED-1002": {
        "codigo": "BR000000000XX",
        "status": "entregue",
        "entregue_em": "2026-11-03",
        "recebedor_assinatura": False,  # sem assinatura: prova fraca
        "endereco_entrega_confere": True,
    },
}

INTERACOES = {
    "PED-1001": [
        {"data": "2026-10-22", "de": "comprador", "texto": "Consegui acessar, obrigada!"},
    ],
    "PED-1002": [
        {"data": "2026-11-05", "de": "comprador", "texto": "Meu pedido ainda não chegou."},
        {"data": "2026-11-05", "de": "produtor", "texto": "Consta entregue em 03/11, pode conferir com a portaria?"},
    ],
    "PED-1003": [],
}

# Cobrança em dobro: duas transações do mesmo pedido
TRANSACOES = {
    "PED-1003": [
        {"id": "TX-9001", "valor": 97.00, "data": "2026-10-30 08:41"},
        {"id": "TX-9002", "valor": 97.00, "data": "2026-10-30 08:41"},
    ],
}
