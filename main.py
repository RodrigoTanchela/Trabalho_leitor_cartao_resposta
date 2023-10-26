from View.TelaLeitorCartao import TelaLeitorCartao
from controller.ControladorLeitorCartao import ControladorLeitorCartao

# Crie uma instância do controlador
controlador = ControladorLeitorCartao()

# Crie uma instância da tela e associe o controlador a ela
tela = TelaLeitorCartao(controlador)
controlador.visao = tela


# Inicie o loop de eventos da interface gráfica
tela.Iniciar()
