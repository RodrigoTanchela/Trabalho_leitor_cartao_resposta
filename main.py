from View.TelaLeitorCartao import TelaLeitorCartao
from controller.ControladorLeitorCartao import ControladorLeitorCartao


controlador = ControladorLeitorCartao()
TelaLeitorCartao = TelaLeitorCartao(controlador)
controlador.visao = TelaLeitorCartao

# Inicia o loop de eventos da interface gráfica
TelaLeitorCartao.Iniciar()
