import json
import statistics
import math
from ProjetoPin3.model.ConfiguracaoQuestao import ConfiguracaoQuestao
from ProjetoPin3.model.ConfiguracaoOpcoes import ConfiguracoesOpcoes
from ProjetoPin3.View.TelaGeracaoCartaoResposta import TelaGeracaoCartaoResposta
import cv2
import numpy as np
from openpyxl import Workbook

class ControladorLeitorCartao:
    def __init__(self):
        self.visaoLeitorCartaoResposta = None
        self.aluno = None
        self.cartaoResposta = None
        self.configuracaoOpcoes = None
        self.configuracaoQuestao = None
        self.geracaoPlanilha = None
        self.questoes = None
        self.keypoints = None

    def abrir_explorador_de_arquivos(self, arquivo_selecionado):
        # self.modelo.arquivo_selecionado = arquivo_selecionado
        self.visaoLeitorCartaoResposta.atualizar_label(arquivo_selecionado)

    def actionPreview(self):
        img = self.visaoLeitorCartaoResposta.getImage()
        keypoints, img_cinza = self.identificandoPontos(img)
        image = self.construcaoFormularioRetangular(keypoints, img_cinza)
        self.visaoLeitorCartaoResposta.previewConfiguracoes(image)

    def importar_cartao_resposta(self,  arquivo_selecionado):
        self.telaGeracaoCartaoResposta.atualizar_label(arquivo_selecionado)

    def salvarKeypoints(self, keypoints):
        pass

    def definirConfiguracao(self, configuracao):
        numeroPerguntas = configuracao['numeroPerguntas']
        numeroOpcoes = configuracao['numeroOpcoes']
        margemLateral = configuracao['margemLateral']
        margemSuperior = configuracao['margemSuperior']
        larguraMarcador = configuracao['larguraMarcador']
        alturaMarcador = configuracao['alturaMarcador']
        espacamentoPerguntas = configuracao['espacamentoPerguntas']
        espacamentoResposta = configuracao['espacamentoResposta']
        # qtdAlunos = configuracao['qtdAlunos']

        self.keypoints = configuracao['keypoints']
        keypoints = configuracao['keypoints']
        keypoint = keypoints[2]
        posicaoHorizontal = int(keypoint.pt[0])
        posicaoVertical = int(keypoint.pt[1])

        self.configuracaoQuestao = ConfiguracaoQuestao(espacamentoPerguntas, numeroPerguntas, margemSuperior, margemLateral, posicaoHorizontal, posicaoVertical)
        self.configuracaoOpcoes = ConfiguracoesOpcoes(espacamentoResposta, numeroOpcoes, larguraMarcador, alturaMarcador)


    def actionImportacao(self):
        self.telaGeracaoCartaoResposta = TelaGeracaoCartaoResposta(self)
        self.visaoLeitorCartaoResposta.abrirTelaImportacaoCartaoResposta()
        self.telaGeracaoCartaoResposta.iniciar()

    def tamahoAreaRecorte(self):
        largura = int(self.keypoints[3].pt[0]) - int(self.keypoints[2].pt[0])
        altura = int(self.keypoints[0].pt[1]) - int(self.keypoints[2].pt[1])
        return largura, altura

    def leituraRespostas(self, image, img_cinza, caminho_arquivo):
        workbook = Workbook()
        sheet = workbook.active
        sheet.cell(row=1, column=1, value = 'Alunos')
        for aluno in range(len(image)):
            sheet.cell(row=aluno+2, column = 1, value=f'Aluno{aluno+1}')
            # print(respostas[2])
            respostas_alunos = self.identificar_respostas(image[aluno])
            for questao in range (1,15):
                sheet.cell(row=1, column= questao+1, value=f'Questão {questao}')
                respostas = str(respostas_alunos[questao-1]).strip('[]')
                sheet.cell(row=aluno+2, column=questao+1, value=respostas)

        workbook.save(caminho_arquivo)
        self.visaoLeitorCartaoResposta.popupInformativo(f'Dados salvos em {caminho_arquivo}')

    def salvandoDadosTela(self, dados, nome_arquivo):
        with open(nome_arquivo, 'w') as arquivo:
            json.dump(dados, arquivo, indent=4)

    def identificar_respostas(self, image):
        respostas = []
        respostas_Questao = []
        keypoints, img = self.identificandoPontos(image)
        configuracoes = self.configuracoesFolhaResposta(keypoints)
        angulo = self.verificaPosicaoKeyPoint(keypoints)
        print(angulo)
        image = self.rotacionar_imagem(image, angulo)

        x = int(keypoints[2].pt[0])
        y = int(keypoints[2].pt[1])

        # pontos_quina = np.float32([[20, 60], [60, 60], [20, 150], [5000, 4500]])
        # image = self.endireitar_imagem(image, pontos_quina)
        # comprimento2, altura2 = self.calculaDimensaoKeypoins(keypoints)
        # print(comprimento2, altura2)
        retangulo_width = configuracoes['largura']
        retangulo_height = configuracoes['altura']

        distancia_horizontal = configuracoes['espacamentoPerguntas']
        distancia_vertical = configuracoes['espacamentoRespostas']

        start_x = int(x + configuracoes['margemLateral'])
        start_y = int(y + configuracoes['margemSuperior'])

        for i in range(self.configuracaoQuestao.get_numero()):
            for j in range(self.configuracaoOpcoes.get_numero()):
                x1, y1 = start_x, start_y
                x2, y2 = start_x + retangulo_width, start_y + retangulo_height
                retangulo = image[y1:y2, x1:x2]

                media_canais = cv2.mean(retangulo)
                valorCanais = statistics.mean(media_canais)
                if valorCanais < 145:
                    numero_retangulo = j+1
                    if(j < self.configuracaoOpcoes.get_numero()):
                        letra = self.numero_para_letra(numero_retangulo)
                        respostas_Questao.append(letra)
                elif valorCanais > 150 and valorCanais < 155:
                        letra = self.telaGeracaoCartaoResposta.popupTeste(f'Houve dificuldade em identificar opção correta na questão{i} verifique e digite a opção correta abaixo')
                        respostas_Questao.append(letra)

                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 1)

                start_x += retangulo_width + distancia_horizontal


            respostas.append(respostas_Questao)
            respostas_Questao = []
            start_x = int(x + configuracoes['margemLateral'])
            start_y += retangulo_height + distancia_vertical
        self.telaGeracaoCartaoResposta.testeApagar(image)
        return respostas


    def verificar_cor(area, cor):
        # 4. Verifique se a área contém a cor especificada
        area_bgr = cv2.cvtColor(area, cv2.COLOR_BGR2RGB)
        cor_bgr = np.array(cor, dtype=np.uint8)
        return np.any(np.all(area_bgr == cor_bgr, axis=-1))

    def identificandoPontos(self, imagem):
        params = cv2.SimpleBlobDetector_Params()
        params.filterByColor = True
        params.blobColor = 0
        params.filterByArea = True
        params.minRepeatability = 16
        params.maxArea = 350
        angulo = 5

        img_cinza = cv2.cvtColor(np.array(imagem), cv2.COLOR_BGR2GRAY)

        detector = cv2.SimpleBlobDetector_create(params)
        keypoints = detector.detect(img_cinza)
        # Desenhar os keypoints na imagem
        imagem_com_keypoints = cv2.drawKeypoints(img_cinza, keypoints, None)
        keypoints = self.ordenarKeyPoints(keypoints)

        return keypoints, img_cinza

    def construcaoFormularioRetangular(self, keypoints, image):
        keypoint = keypoints[2]
        x, y = int(keypoint.pt[0]), int(keypoint.pt[1])
        largura, altura = self.visaoLeitorCartaoResposta.getLarguraMarcador(), self.visaoLeitorCartaoResposta.getAlturaMarcador()
        espacamento_resposta, espacamento_pergunta = self.visaoLeitorCartaoResposta.getEspacamentoResposta() , self.visaoLeitorCartaoResposta.getEspacamentoPergunta()
        x_inicio, y_inicio = int(x + self.visaoLeitorCartaoResposta.getMargemLateral()), int(y + self.visaoLeitorCartaoResposta.getMargemSuperior())
        color = (0, 255, 0)
        thickness = 1
        # angulo = keypoints[2].angle/-1
        # angulo = self.encontrar_angulo_rotacao_com_keypoints(image, keypoints)
        # image = self.rotacionar_imagem(image, angulo)
        x = x_inicio
        y = y_inicio
        for _ in range(self.visaoLeitorCartaoResposta.getNumeroPerguntas()):
            for _ in range(self.visaoLeitorCartaoResposta.getNumeroOpcoes()):
                x2, y2 = x + largura, y + altura
                cv2.rectangle(image, (x, y), (x2, y2), color, thickness)
                x += largura + espacamento_resposta
            x = x_inicio
            y += altura + espacamento_pergunta

        # comprimento2, altura2 = self.calculaDimensaoKeypoins(keypoints)
        # print(comprimento2, altura2)

        return image

    def configuracoesFolhaResposta(self, keypoints):
        escala = self.calculaEscala(keypoints)

        espacamentoRespostas = self.calcularedimensaoNecessaria(self.configuracaoOpcoes.get_espacamento(), escala['comprimentoConfiguracao'], escala['comprimentoRespostas'])
        largura = self.calcularedimensaoNecessaria(self.configuracaoOpcoes.get_largura(), escala['comprimentoConfiguracao'], escala['comprimentoRespostas'])
        margemLateral = self.calcularedimensaoNecessaria(self.configuracaoQuestao.get_margemLateral(), escala['comprimentoConfiguracao'], escala['comprimentoRespostas'])

        espacamentoPerguntas = self.calcularedimensaoNecessaria(self.configuracaoOpcoes.get_espacamento(), escala['alturaCofiguracao'], escala['alturaRespostas'])
        altura = self.calcularedimensaoNecessaria(self.configuracaoOpcoes.get_altura(), escala['alturaCofiguracao'], escala['alturaRespostas'])
        margemSuperior = self.calcularedimensaoNecessaria(self.configuracaoQuestao.get_margemSuperior(), escala['alturaCofiguracao'], escala['alturaRespostas'])

        return {
            'espacamentoRespostas': int(round(espacamentoRespostas)),
            'largura': int(round(largura)),
            'margemLateral': int(math.ceil(margemLateral)),
            'espacamentoPerguntas': int(round(espacamentoPerguntas)),
            'altura': int(round(altura)),
            'margemSuperior': int(math.ceil(margemSuperior))
        }

    def calcularedimensaoNecessaria(self, valorConfiguracao, keypointConfiguracao, keypointResposta):
        return (keypointResposta * valorConfiguracao) / keypointConfiguracao


    def calculaEscala(self, keypoints):
        comprimentoConfiguracao, alturaCofiguracao = self.calculaDimensaoKeypoins(self.keypoints)
        comprimentoRespostas, alturaRespostas = self.calculaDimensaoKeypoins(keypoints)
        comprimento = alturaCofiguracao - alturaRespostas
        altura = comprimentoConfiguracao - comprimentoRespostas
        return {
            'comprimentoConfiguracao': comprimentoConfiguracao,
            'alturaCofiguracao': alturaCofiguracao,
            'comprimentoRespostas': comprimentoRespostas,
            'alturaRespostas': alturaRespostas,
            'comprimento': comprimento,
            'altura': altura

        }

    # def verificaPosicaoKeyPoint(self, keypoints):
    #     delta_y = self.keypoints[2].pt[0] - keypoints[2].pt[0]
    #     delta_x = self.keypoints[2].pt[1] - keypoints[2].pt[1]
    #     angulo_radianos = math.atan2(delta_y, delta_x)
    #
    #     # Converta para graus, se necessário
    #     angulo_graus = math.degrees(angulo_radianos)
    #
    #     print("Ângulo em radianos:", angulo_radianos)
    #     print("Ângulo em graus:", angulo_graus)

    def calculaDimensaoKeypoins(self, keypoints):
        comprimento = keypoints[0].pt[0] - keypoints[2].pt[0]
        altura = keypoints[2].pt[1] - keypoints[3].pt[1]
        return comprimento, altura

    def numero_para_letra(self, numero):
        if 1 <= numero <= 26:
            return chr(ord('a') + numero - 1)
        else:
            return '?'

    def ordenarKeyPoints(self, keypoints):
        keypoints_ordenados = sorted(keypoints, key=lambda keypoint: (keypoint.pt[0], keypoint.pt[1]), reverse=True)
        return keypoints_ordenados

    def rotacionar_imagem(self, imagem, angulo):
        # Obter as dimensões da imagem
        altura, largura = imagem.shape[:2]

        # Calcular o ponto central da imagem
        ponto_central = (largura // 2, altura // 2)

        # Criar a matriz de rotação
        matriz_rotacao = cv2.getRotationMatrix2D(ponto_central, angulo, 1.0)

        # Aplicar a rotação na imagem
        imagem_rotacionada = cv2.warpAffine(imagem, matriz_rotacao, (largura, altura), flags=cv2.INTER_LINEAR)

        return imagem_rotacionada

    def encontrar_angulo_rotacao_com_keypoints(self, imagem, keypoints):
        # Inicializar o detector ORB
        orb = cv2.ORB_create()

        # Calcular a média dos ângulos dos keypoints
        angulo_total = 0
        if keypoints:
            for keypoint in keypoints:
                angulo_total += keypoint.angle

            angulo_medio = angulo_total / len(keypoints)
            angulo_rotacao = angulo_medio

            return angulo_rotacao

        return None

    def verificaPosicaoKeyPoint(self, keypoints):
        desvio = math.floor(keypoints[2].pt[0] - keypoints[3].pt[0])
        self.calculaAnguloInterno(keypoints)
        if(desvio > 90):
            return -1
        else:
            return +1

    def calculaAnguloInterno(self, keypoints):
        xfictio, yficticio = keypoints[2].pt[0], keypoints[3].pt[1]
        y = yficticio -  keypoints[2].pt[1]
        x = xfictio - keypoints[3].pt[0]
        h = math.sqrt(((y ** 2) + (x ** 2)))
        print(y, x, h)
        cos_theta = y / h
        sen_theta = x / h
        # Calcular o ângulo em radianos
        theta_radianos = math.acos(cos_theta)
        sen_theta_radianos = math.acos(sen_theta)
        # Converter para graus
        theta_graus = math.degrees(theta_radianos)
        sen_graus = math.degrees(sen_theta_radianos)
        print(theta_graus, sen_graus)
        # return theta_graus
