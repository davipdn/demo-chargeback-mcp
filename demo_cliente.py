"""Demonstração do fluxo do dossiê de chargeback.

IMPORTANTE (honestidade): aqui NÃO há um LLM. Este script faz o papel do "agente" com
um roteiro fixo, só para mostrar o fluxo e as chamadas MCP reais ao servidor.
Numa versão real, um LLM decidiria quais ferramentas chamar e redigiria a defesa.
O servidor MCP (server.py) é real; os dados são fictícios.

Uso:  python demo_cliente.py CB-001      (ou CB-002, CB-003)
"""
import asyncio
import json
import sys

from mcp.client import Client
from mcp.client.stdio import StdioServerParameters


async def chamar(c, nome, args):
    r = await c.call_tool(nome, args)
    if r.structured_content and "result" in r.structured_content:
        dado = r.structured_content["result"]  # ferramentas que devolvem lista
    else:
        dado = json.loads(r.content[0].text) if r.content else None
    print(f"   [MCP] {nome}({', '.join(f'{k}={v}' for k, v in args.items())})")
    return dado


async def main(cb_id):
    params = StdioServerParameters(command=sys.executable, args=["server.py"])
    async with Client(params) as c:
        print(f"\n=== Caso {cb_id} ===")
        ferramentas = [t.name for t in (await c.list_tools()).tools]
        print(f"   O servidor MCP oferece {len(ferramentas)} ferramentas (Tools): {', '.join(ferramentas)}")
        regras = await c.read_resource("regras://documentos-aceitos")
        print("   [MCP] Resource lido: regras://documentos-aceitos")
        modelo = await c.get_prompt("montar_dossie", {"chargeback_id": cb_id})
        print("   [MCP] Prompt carregado: montar_dossie (instruções que um LLM seguiria)")
        cb = await chamar(c, "buscar_chargeback", {"chargeback_id": cb_id})
        prazo = await chamar(c, "checar_prazo", {"chargeback_id": cb_id})
        print(f"   Motivo: {cb['motivo']} | Valor: R$ {cb['valor']:.2f}")
        print(f"   Prazo: {prazo['horas_restantes']}h restantes (vencido: {prazo['vencido']})")
        ped_id = cb["pedido"]
        pedido = await chamar(c, "buscar_pedido", {"pedido_id": ped_id})

        if prazo["vencido"]:
            print("   !! PRAZO VENCIDO: avisar o produtor imediatamente.")
        provas, faltas = [], []
        recomenda_reembolso = False
        motivo = cb["motivo"]

        if motivo == "compra_nao_reconhecida":
            logs = await chamar(c, "buscar_logs_acesso", {"pedido_id": ped_id})
            msgs = await chamar(c, "buscar_interacoes", {"pedido_id": ped_id})
            if logs:
                provas.append(f"{len(logs)} registros de uso da área de membros (primeiro: {logs[0]['data']}, IP {logs[0]['ip']})")
            else:
                faltas.append("logs de acesso (nenhum registro de uso)")
            if msgs:
                provas.append("mensagem do próprio comprador confirmando o acesso")
        elif motivo == "produto_nao_recebido":
            rast = await chamar(c, "buscar_rastreio", {"pedido_id": ped_id})
            val = await chamar(c, "validar_prova_entrega", {"pedido_id": ped_id})
            if val["aceita"]:
                provas.append(f"entrega confirmada em {rast['entregue_em']}")
            else:
                faltas.append("comprovante de entrega aceito: " + "; ".join(val["problemas"]))
                provas.append(f"rastreio {rast['codigo']} marcado como entregue em {rast['entregue_em']} (prova FRACA)")
            await chamar(c, "buscar_interacoes", {"pedido_id": ped_id})
        elif motivo == "cobranca_em_dobro":
            tx = await chamar(c, "buscar_transacoes", {"pedido_id": ped_id})
            if len(tx) > 1:
                faltas.append(f"há {len(tx)} transações no mesmo pedido: possível cobrança duplicada real")
                recomenda_reembolso = True

        print("\n--- DOSSIÊ (rascunho para revisão humana) ---")
        print("Provas encontradas:")
        for p in provas:
            print("  +", p)
        print("Pontos de atenção / o que falta:")
        for f in faltas or ["nada crítico"]:
            print("  !", f)
        if recomenda_reembolso:
            print("\nRecomendação: NÃO contestar. Evidência de cobrança em dobro; avaliar reembolso.")
        else:
            print("\nRascunho de defesa (modelo fixo; um LLM redigiria de forma personalizada):")
            print(f"  \"Contestamos o chargeback {cb_id} referente ao pedido {ped_id} ({pedido['produto']}). "
                  f"Seguem as evidências: {' | '.join(provas) or 'nenhuma'}.\"")
        print("\n>>> STATUS: AGUARDANDO APROVAÇÃO DO PRODUTOR. Nada foi enviado. <<<")


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1] if len(sys.argv) > 1 else "CB-001"))
