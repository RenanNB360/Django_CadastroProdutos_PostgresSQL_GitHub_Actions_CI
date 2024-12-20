import io

import pytest
from django.contrib.messages import get_messages
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from PIL import Image

from core.forms import ContatoForm, ProdutoModelForm
from core.models import Produto


@pytest.mark.django_db
class TestViews:
    produto = {
        'nome': 'Produto Teste',
        'preco': 50.00,
        'estoque': 30,
        'imagem': 'produtos/exemplo.jpg',
    }

    form_data = {
        'nome': 'Teste',
        'email': 'teste@email.com',
        'assunto': 'Assunto Teste',
        'mensagem': 'Mensagem Teste',
    }

    form_data_invalid = {
        'nome': '',
        'email': 'teste@email.com',
        'assunto': 'Assunto Teste',
        'mensagem': 'Mensagem Teste',
    }

    user = {
        'username': 'testuser',
        'password': 'testpass',
    }

    @staticmethod
    def create_image_file():
        image = Image.new('RGB', (100, 100), color='red')
        image_file = io.BytesIO()
        image.save(image_file, format='JPEG')
        image_file.seek(0)
        return SimpleUploadedFile(
            name='exemplo.jpg',
            content=image_file.read(),
            content_type='image/jpeg',
        )

    def test_index_view(self, client):
        produto = Produto.objects.create(**self.produto)

        response = client.get(reverse('index'))

        assert response.status_code == 200
        assert 'produtos' in response.context
        assert produto in response.context['produtos']
        assert 'index.html' in [t.name for t in response.templates]

    def test_contato_view_get(self, client):
        response = client.get(reverse('contato'))

        assert response.status_code == 200
        assert isinstance(response.context['form'], ContatoForm)
        assert 'contato.html' in [t.name for t in response.templates]

    def test_contato_view_post_valid(self, client, mocker):
        mocked_send_mail = mocker.patch('core.forms.ContatoForm.send_mail')
        response = client.post(reverse('contato'), data=self.form_data)
        messages = list(get_messages(response.wsgi_request))

        assert response.status_code == 200
        assert mocked_send_mail.called
        assert len(messages) == 1
        assert str(messages[0]) == 'Enviado com sucesso!'

    def test_contato_view_post_invalid(self, client):
        response = client.post(reverse('contato'), data=self.form_data_invalid)
        messages = list(get_messages(response.wsgi_request))

        assert response.status_code == 200
        assert len(messages) == 1
        assert str(messages[0]) == 'Erro ao enviar!'

    def test_produto_view_get_authenticated(self, client, django_user_model):
        django_user_model.objects.create_user(**self.user)
        client.login(username=self.user['username'], password=self.user['password'])
        response = client.get(reverse('produto'))

        assert response.status_code == 200
        assert isinstance(response.context['form'], ProdutoModelForm)
        assert 'produto.html' in [t.name for t in response.templates]

    def test_produto_view_get_anonymous(self, client):
        response = client.get(reverse('produto'))

        assert response.status_code == 302
        assert response.url == reverse('index')

    def test_produto_view_post_authenticated_valid(self, client, django_user_model):
        django_user_model.objects.create_user(**self.user)
        client.login(username=self.user['username'], password=self.user['password'])
        self.produto['imagem'] = self.create_image_file()
        response = client.post(reverse('produto'), data=self.produto)
        messages = list(get_messages(response.wsgi_request))

        assert response.status_code == 200
        assert Produto.objects.filter(nome=str(self.produto['nome'])).exists()
        assert len(messages) == 1
        assert str(messages[0]) == 'Produto salvo com sucesso!'

    def test_produto_view_post_authenticated_invalid(self, client, django_user_model):
        django_user_model.objects.create_user(**self.user)
        client.login(username=self.user['username'], password=self.user['password'])
        self.produto['nome'] = ''
        response = client.post(reverse('produto'), data=self.produto)
        messages = list(get_messages(response.wsgi_request))

        assert response.status_code == 200
        assert not Produto.objects.exists()
        assert len(messages) == 1
        assert str(messages[0]) == 'Erro ao salvar produto!'
