from View.TelaLeitorCartao import TelaLeitorCartao
from controller.ControladorLeitorCartao import ControladorLeitorCartao

# Crie uma instância do controlador
controlador = ControladorLeitorCartao()

# Crie uma instância da tela e associe o controlador a ela
telaLeitorCartaoResposta = TelaLeitorCartao(controlador)
controlador.visaoLeitorCartaoResposta = telaLeitorCartaoResposta

# Inicie o loop de eventos da interface gráfica
telaLeitorCartaoResposta.Iniciar()
