import io

import pytest
from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image

from core.forms import ContatoForm, ProdutoModelForm


@pytest.mark.django_db
class TestForms:
    form_data = {
        'nome': 'Paulo',
        'email': 'paulo@example.com',
        'assunto': 'Teste de Assunto',
        'mensagem': 'Teste de Mensagem',
    }

    produto_model = {
        'nome': 'Produto teste',
        'preco': 50.00,
        'estoque': 100,
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

    def test_contato_form_valid(self):
        form = ContatoForm(data=self.form_data)

        assert form.is_valid()

    def test_contato_form_invalid(self):
        invalid_data = self.form_data.copy()
        invalid_data['email'] = ''

        form = ContatoForm(data=invalid_data)
        assert not form.is_valid()
        assert 'email' in form.errors

    def test_contato_form_send_email(self, mocker):
        form = ContatoForm(data=self.form_data)

        form = ContatoForm(data=self.form_data)

        if form.is_valid():
            form.send_mail()

        assert len(mail.outbox) == 1
        email = mail.outbox[0]
        assert email.subject == 'E-mail enviado pelo Django!'
        assert 'Nome Paulo' in email.body
        assert 'Email: paulo@example.com' in email.body

    def test_produto_model_form_valid(self):
        form = ProdutoModelForm(
            data={
                'nome': self.produto_model['nome'],
                'preco': self.produto_model['preco'],
                'estoque': self.produto_model['estoque'],
            },
            files={'imagem': self.create_image_file()},
        )

        assert form.is_valid()

    def test_produto_model_form_invalid(self):
        form = ProdutoModelForm(data=self.produto_model)

        assert not form.is_valid()
        assert 'imagem' in form.errors
