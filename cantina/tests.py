from django.test import RequestFactory, TestCase

from .forms import CadAlu, CadEsc, EntAlu, EntEsc, ItensForm, Dinheiro
from .models import User, Aluno, Escola, Itens, Mensagem, Pedido

class teste_escola(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_escola(email='a@a.aaa', password='12345')
        self.escola = Escola(nome='escolinha', usuario=self.user)

    def test_details(self):
        request = self.factory.get('/escola')
        request.user = self.user
        response = my_view(request)
        response = MyView.as_view()(request)
        self.assertEqual(response.view_name, 'entrar')
        #login = self.client.login(email='a@a.aaa', password='12345')
