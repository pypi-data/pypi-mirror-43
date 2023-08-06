"""
Transação 3 - Venda de PINs
"""
from decimal import Decimal

from .rv_api import RVapi
from .objetos.recarga import Recarga


class Transacao3(RVapi):

    def execute(self, compra: int, produto: str, mock=None) -> Recarga:
        if mock is not None:
            response = mock
        else:
            payload = {
                "codigo_transacao": 3,
                "loja_primaria": self.CREDENCIAIS['loja_primaria'],
                "nome_primario": self.CREDENCIAIS['nome_primario'],
                "senha_primaria": self.CREDENCIAIS['senha_primaria'],
                "versao": self.VERSAO,
                "compra": compra,
                "produto": produto,
                # "ddd": ddd,
                # "fone": fone,
                # "codigoAssinante": codigo_assinante,
            }

            # if valor is not None:
            #     payload['valor'] = valor

            response = self.doPOST(payload)

        return Recarga().parse_dict(self.convert_xml_to_dict(response))
