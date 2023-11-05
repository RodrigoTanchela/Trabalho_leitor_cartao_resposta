import json
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

        self.configuracaoQuestao = ConfiguracaoQuestao(numeroPerguntas, espacamentoPerguntas, margemSuperior, margemLateral, qtdAlunos, posicaoHorizontal, posicaoVertical)
        self.configuracaoOpcoes = ConfiguracoesOpcoes(numeroOpcoes, espacamentoResposta, larguraMarcador, alturaMarcador)


    def actionImportacao(self):
        self.telaGeracaoCartaoResposta = TelaGeracaoCartaoResposta(self)
        self.visaoLeitorCartaoResposta.abrirTelaImportacaoCartaoResposta()
        self.telaGeracaoCartaoResposta.setVisible()

    def tamahoAreaRecorte(self):
        largura = int(self.keypoints[3].pt[0]) - int(self.keypoints[2].pt[0])
        altura = int(self.keypoints[0].pt[1]) - int(self.keypoints[2].pt[1])
        return largura, altura

    def leituraRespostas(self, image):
        workbook = Workbook()
        sheet = workbook.active
        sheet.cell(row=1, column=1, value = 'Alunos')
        for aluno in range(0,3):
            sheet.cell(row=aluno+2, column = 1, value=f'Aluno{aluno+1}')
            # print(respostas[2])
            respostas_alunos = self.identificar_respostas(image[aluno])
            for questao in range (1,15):
                sheet.cell(row=1, column= questao+1, value=f'Questão {questao}')
                respostas = str(respostas_alunos[questao-1]).strip('[]')
                sheet.cell(row=aluno+2, column=questao+1, value=respostas)

        workbook.save('exemplo17.xlsx')

    def salvandoDadosTela(self, dados, nome_arquivo):
        try:
            with open(nome_arquivo, 'w') as arquivo:
                json.dump(dados, arquivo, indent=4)
            print(f'Dados salvos em {nome_arquivo}')
        except Exception as e:
            print(f"Ocorreu um erro ao salvar os dados: {str(e)}")

    def identificar_respostas(self, image):
        respostas = []
        respostas_Questao = []
        keypoint = self.keypoints[2]
        x = int(keypoint.pt[0])
        y = int(keypoint.pt[1])

        retangulo_width = self.visaoLeitorCartaoResposta.getLarguraMarcador()
        retangulo_height = self.visaoLeitorCartaoResposta.getAlturaMarcador()

        distancia_horizontal = self.visaoLeitorCartaoResposta.getEspacamentoResposta()
        distancia_vertical = self.visaoLeitorCartaoResposta.getEspacamentoPergunta()

        start_x = int(x + self.visaoLeitorCartaoResposta.getMargemLateral())
        start_y = int(y + self.visaoLeitorCartaoResposta.getMargemSuperior())

        linhas_limite = self.visaoLeitorCartaoResposta.getNumeroPerguntas()
        retangulos_por_linha = self.visaoLeitorCartaoResposta.getNumeroOpcoes()

        for i in range(linhas_limite):
            for j in range(retangulos_por_linha):
                x1, y1 = start_x, start_y
                x2, y2 = start_x + retangulo_width, start_y + retangulo_height
                retangulo = image[y1:y2, x1:x2]

                # 1. Verificar se há preenchimento no retângulo (um exemplo simples)
                # Neste exemplo, estamos verificando se a média dos valores dos canais é maior que 0
                media_canais = cv2.mean(retangulo)
                if sum(media_canais) < 200:
                    numero_retangulo = j+1
                    if(j < retangulos_por_linha):
                        respostas_Questao.append(numero_retangulo)

                # Desenhe o retângulo na imagem (para visualização)
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 1)

                start_x += retangulo_width + distancia_horizontal


            respostas.append(respostas_Questao)
            respostas_Questao = []
            start_x = int(x + self.visaoLeitorCartaoResposta.getMargemLateral())
            start_y += retangulo_height + distancia_vertical

            # Exiba a imagem com os retângulos desenhados
        # cv2.imshow('Retângulos', image)

        # Aguarde uma tecla ser pressionada para continuar
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # print(respostas_alunos)
        return respostas


    def verificar_cor(area, cor):
        # 4. Verifique se a área contém a cor especificada
        area_bgr = cv2.cvtColor(area, cv2.COLOR_BGR2RGB)
        cor_bgr = np.array(cor, dtype=np.uint8)
        return np.any(np.all(area_bgr == cor_bgr, axis=-1))

    def identificandoPontos(self, imagem):
        #imagem = self.extraindoImagem()

        params = cv2.SimpleBlobDetector_Params()
        params.filterByColor = True
        params.blobColor = 0
        params.filterByArea = True
        params.minRepeatability = 12
        # params.minArea = 300
        params.maxArea = 350

        img_cinza = cv2.cvtColor(np.array(imagem), cv2.COLOR_BGR2GRAY)

        detector = cv2.SimpleBlobDetector_create(params)
        keypoints = detector.detect(img_cinza)

        imagem_com_keypoints = cv2.drawKeypoints(img_cinza, keypoints, None)

        # cv2.imshow("Imagem com Keypoints", imagem_com_keypoints)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        return keypoints, img_cinza
        #self.construcaoFormularioRetangular(keypoints, img_cinza)

    def construcaoFormularioRetangular(self, keypoints, image):
        indice = 2
        keypoint = keypoints[indice]
        x = int(keypoint.pt[0])
        y = int(keypoint.pt[1])

        # Tamanho dos retângulos
        retangulo_width = self.visaoLeitorCartaoResposta.getLarguraMarcador()
        retangulo_height = self.visaoLeitorCartaoResposta.getAlturaMarcador()

        distancia_horizontal = self.visaoLeitorCartaoResposta.getEspacamentoResposta()
        distancia_vertical = self.visaoLeitorCartaoResposta.getEspacamentoPergunta()

        # Posição inicial a partir da qual começar a desenhar
        start_x = int(x + self.visaoLeitorCartaoResposta.getMargemLateral())
        start_y = int(y + self.visaoLeitorCartaoResposta.getMargemSuperior())

        # Cor dos retângulos (em BGR)
        color = (0, 255, 0)  # Verde

        thickness = 1
        linhas_limite = self.visaoLeitorCartaoResposta.getNumeroPerguntas()
        linha_atual = 1
        retangulos_desenhados = 0
        retangulos_por_linha = self.visaoLeitorCartaoResposta.getNumeroOpcoes()

        # Desenhe os retângulos na imagem com a posição inicial
        x = start_x
        y = start_y
        for _ in range(linhas_limite):
            for _ in range(retangulos_por_linha):
                x1, y1 = x, y
                x2, y2 = x + retangulo_width, y + retangulo_height
                cv2.rectangle(image, (x1, y1), (x2, y2), color, thickness)
                x += retangulo_width + distancia_horizontal

            # Mover para a próxima linha
            x = start_x
            y += retangulo_height + distancia_vertical

        # cv2.imshow('Retângulos', image)
        #
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        return image

