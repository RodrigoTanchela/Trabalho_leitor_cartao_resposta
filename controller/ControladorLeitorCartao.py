import json
import statistics

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
        qtdAlunos = configuracao['qtdAlunos']

        self.keypoints = configuracao['keypoints']
        keypoints = configuracao['keypoints']
        keypoint = keypoints[2]
        posicaoHorizontal = int(keypoint.pt[0])
        posicaoVertical = int(keypoint.pt[1])

        self.configuracaoQuestao = ConfiguracaoQuestao(espacamentoPerguntas, numeroPerguntas, margemSuperior, margemLateral, qtdAlunos, posicaoHorizontal, posicaoVertical)
        self.configuracaoOpcoes = ConfiguracoesOpcoes(espacamentoResposta, numeroOpcoes, larguraMarcador, alturaMarcador)


    def actionImportacao(self):
        self.telaGeracaoCartaoResposta = TelaGeracaoCartaoResposta(self)
        self.visaoLeitorCartaoResposta.abrirTelaImportacaoCartaoResposta()
        self.telaGeracaoCartaoResposta.setVisible()

    def tamahoAreaRecorte(self):
        largura = int(self.keypoints[3].pt[0]) - int(self.keypoints[2].pt[0])
        altura = int(self.keypoints[0].pt[1]) - int(self.keypoints[2].pt[1])
        return largura, altura

    def leituraRespostas(self, image, img_cinza, caminho_arquivo):
        workbook = Workbook()
        sheet = workbook.active
        sheet.cell(row=1, column=1, value = 'Alunos')
        for aluno in range(self.configuracaoQuestao.get_qtdAlunos()):
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
        # keypoint = self.keypoints[2]
        keypoints, img = self.identificandoPontos(image)
        configuracoes = self.configuracoesFolhaResposta(keypoints)
        print(configuracoes)

        x = int(keypoints[2].pt[0])
        y = int(keypoints[2].pt[1])

        # comprimento2, altura2 = self.calculaDimensaoKeypoins(keypoints)
        # print(comprimento2, altura2)
        retangulo_width = self.configuracaoOpcoes.get_largura()
        retangulo_height = self.configuracaoOpcoes.get_altura()

        distancia_horizontal = self.configuracaoOpcoes.get_espacamento()
        distancia_vertical = self.configuracaoQuestao.get_espacamento()

        start_x = int(x + self.configuracaoQuestao.get_margemLateral())
        start_y = int(y + self.configuracaoQuestao.get_margemSuperior())

        for i in range(self.configuracaoQuestao.get_numero()):
            for j in range(self.configuracaoOpcoes.get_numero()):
                x1, y1 = start_x, start_y
                x2, y2 = start_x + retangulo_width, start_y + retangulo_height
                retangulo = image[y1:y2, x1:x2]

                media_canais = cv2.mean(retangulo)
                if statistics.median(media_canais) < 190:
                    numero_retangulo = j+1
                    if(j < self.configuracaoOpcoes.get_numero()):
                        respostas_Questao.append(numero_retangulo)
                # elif sum(media_canais) < 200 and sum(media_canais) > 180:
                #         self.telaGeracaoCartaoResposta.popupInformativo('Verificando')

                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 1)

                start_x += retangulo_width + distancia_horizontal


            respostas.append(respostas_Questao)
            respostas_Questao = []
            start_x = int(x + self.configuracaoQuestao.get_margemLateral())
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
        params.minRepeatability = 12
        params.maxArea = 350

        img_cinza = cv2.cvtColor(np.array(imagem), cv2.COLOR_BGR2GRAY)

        detector = cv2.SimpleBlobDetector_create(params)
        keypoints = detector.detect(img_cinza)

        return keypoints, img_cinza

    def construcaoFormularioRetangular(self, keypoints, image):
        keypoint = keypoints[2]
        x, y = int(keypoint.pt[0]), int(keypoint.pt[1])
        largura, altura = self.visaoLeitorCartaoResposta.getLarguraMarcador(), self.visaoLeitorCartaoResposta.getAlturaMarcador()
        espacamento_resposta, espacamento_pergunta = self.visaoLeitorCartaoResposta.getEspacamentoResposta() , self.visaoLeitorCartaoResposta.getEspacamentoPergunta()
        x_inicio, y_inicio = int(x + self.visaoLeitorCartaoResposta.getMargemLateral()), int(y + self.visaoLeitorCartaoResposta.getMargemSuperior())
        color = (0, 255, 0)
        thickness = 1

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
            'espacamentoRespostas': espacamentoRespostas,
            'largura': largura,
            'margemLateral': margemLateral,
            'espacamentoPerguntas': espacamentoPerguntas,
            'altura': altura,
            'margemSuperior': margemSuperior
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

    def calculaDimensaoKeypoins(self, keypoints):
        comprimento = keypoints[3].pt[0] - keypoints[2].pt[0]
        altura = keypoints[0].pt[1] - keypoints[2].pt[1]
        return comprimento, altura