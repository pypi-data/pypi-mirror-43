from .rv_api import RVapi


class Transacao1(RVapi):

    def __init__(self, *args, **kwargs):
        super(Transacao1, self).__init__(self, *args, **kwargs)

    def execute(self, mock=None):
        if mock is not None:
            response = mock
        else:
            response = self.doPOST({
                "codigo_transacao": 1,
                "loja_primaria": self.CREDENCIAIS['loja_primaria'],
                "nome_primario": self.CREDENCIAIS['nome_primario'],
                "senha_primaria": self.CREDENCIAIS['senha_primaria'],
                "versao": self.VERSAO
            })

        return self.convert_xml_to_dict(response)
