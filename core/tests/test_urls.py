import pytest
from django.urls import resolve, reverse

from core.views import contato, index, produto


@pytest.mark.django_db
class TestURLS:
    form_data = {
        'nome': 'Teste',
        'email': 'test@email.com',
        'assunto': 'Assunto Teste',
        'mensagem': 'Mensagem Teste',
    }

    user = {
        'username': 'testuser',
        'password': 'testpass',
    }

    produto = {
        'nome': 'Produto Teste',
        'preco': 50.00,
        'estoque': 30,
        'imagem': '',
    }

    def test_index_url(self, client):
        url = reverse('index')
        response = client.get(url)

        assert response.status_code == 200
        assert resolve(url).func == index
        assert 'index.html' in [t.name for t in response.templates]

    def test_contato_url_get(self, client):
        url = reverse('contato')
        response = client.get(url)

        assert response.status_code == 200
        assert resolve(url).func == contato
        assert 'contato.html' in [t.name for t in response.templates]

    def test_contato_url_post_valid(self, client, mocker):
        mocker.patch('core.forms.ContatoForm.send_mail', return_value=None)
        url = reverse('contato')
        response = client.post(url, data=self.form_data)

        assert response.status_code == 200
        assert 'contato.html' in [t.name for t in response.templates]

    def test_produto_url_authenticated_get(self, client, django_user_model):
        django_user_model.objects.create_user(**self.user)
        client.login(username=self.user['username'], password=self.user['password'])
        url = reverse('produto')
        response = client.get(url)

        assert response.status_code == 200
        assert resolve(url).func == produto
        assert 'produto.html' in [t.name for t in response.templates]

    def test_produto_url_anonymous_get(self, client):
        url = reverse('produto')
        response = client.get(url)

        assert response.status_code == 302
        assert response.url == reverse('index')

    def test_produto_url_autheticated_post_valid(self, client, django_user_model):
        django_user_model.objects.create_user(**self.user)
        client.login(username=self.user['username'], password=self.user['password'])
        url = reverse('produto')
        response = client.post(url, data=self.produto)

        assert response.status_code == 200

    def test_produto_url_authenticated_post_invalid(self, client, django_user_model):
        django_user_model.objects.create_user(**self.user)
        client.login(username=self.user['username'], password=self.user['password'])
        url = reverse('produto')
        self.produto['nome'] = ''
        response = client.post(url, data=self.produto)

        assert response.status_code == 200
        assert 'Erro ao salvar produto!' in response.content.decode('utf-8')
