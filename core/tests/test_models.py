from datetime import date

import pytest
from django.db.utils import IntegrityError

from core.models import Produto


@pytest.mark.django_db
class TestProdutoModel:
    produto = {'nome': 'Produto teste', 'preco': 50.00, 'estoque': 10, 'imagem': 'produtos/exemplo.jpg'}
    imagem = 'produtos/exemplo2.jpg'

    def test_criacao_produto(self):
        produto = Produto.objects.create(**self.produto)

        assert produto.nome == self.produto['nome']
        assert produto.preco == self.produto['preco']
        assert produto.estoque == self.produto['estoque']
        assert produto.ativo is True
        assert produto.slug == 'produto-teste'

        assert produto.criado == date.today()
        assert produto.modificado == date.today()

    def test_slug_gerado_automaticamente(self):
        produto = Produto.objects.create(**self.produto)

        assert produto.slug == 'produto-teste'

    def test_variacoes_imagems(self, settings):
        settings.MEDIA_ROOT = '/tmp/test_media/'
        produto = Produto.objects.create(**self.produto)

        produto.imagem = self.imagem
        produto.save()
        assert produto.imagem.name == self.imagem

    def test_unicidade_nome_produto(self):
        Produto.objects.create(**self.produto)
        with pytest.raises(IntegrityError):
            Produto.objects.create(**self.produto)

    def test_str_retorna_nome(self):
        produto = Produto.objects.create(**self.produto)
        assert str(produto) == self.produto['nome']
