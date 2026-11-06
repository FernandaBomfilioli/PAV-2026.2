import requests


class APIClient:
    """Faz as requisições HTTP para a API"""

    def __init__(self, base_url):
        self.base_url = base_url.rstrip(" /")

    def requisitar(self, metodo, rota, **kwargs):
        url = f"{self.base_url}/{rota.lstrip('/')}"

        try:
            resposta = requests.request(
                metodo, url, timeout=8, **kwargs
            )
        except requests.exceptions.ConnectionError:
            raise Exception(
                "Não foi possível conectar à API. "
                "Verifique se ela está em execução."
            )
        except requests.exceptions.Timeout:
            raise Exception("A API demorou muito para responder.")

        if resposta.status_code >= 400:
            try:
                detalhe = resposta.json()
                if isinstance(detalhe, dict):
                    detalhe = detalhe.get("erro", detalhe)
            except ValueError:
                detalhe = (
                    resposta.text
                    or "Sem detalhes retornados pela API."
                )

            raise Exception(
                f"Erro HTTP {resposta.status_code}: {detalhe}"
            )

        if not resposta.content:
            return None

        try:
            return resposta.json()
        except ValueError:
            return resposta.text

    def listar(self, endpoint):
        resultado = self.requisitar("GET", endpoint)

        if isinstance(resultado, list):
            return resultado

        if isinstance(resultado, dict):
            for chave in ("dados", "data", "items", "results"):
                if isinstance(resultado.get(chave), list):
                    return resultado[chave]
            return [resultado]

        return []

    def criar(self, endpoint, dados):
        return self.requisitar(
            "POST", endpoint, json=dados
        )

    def atualizar(self, endpoint, identificador, dados):
        return self.requisitar(
            "PUT",
            f"{endpoint}/{identificador}",
            json=dados
        )

    def excluir(self, endpoint, identificador):
        return self.requisitar(
            "DELETE", f"{endpoint}/{identificador}"
        )

    def consultar_analise(self, rota, parametros=None):
        return self.requisitar(
            "GET", rota, params=parametros or {}
        )
