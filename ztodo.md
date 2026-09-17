## Inicio de tudo
[] Fazer o menu principal
    - Música principal animada mas calmante(Lofi?), fundo animado(alguma animação scy-fi), efeitos sonoros simples de clique.
    - Botão de novo-jogo, carregar, créditos e sair.
        - *Botão de jogar* leva aos slots de save no *modo add*. O modo add vai *adicionar* um novo *save sem progresso* e *entrar na fase tutorial*
        - *Botão de carregar* leva aos slots de save no *modo load*. *Caso* o *player não tiver progresso* no save a fase *tutorial é carregada*, *depois* disso o modo load vai *entrar no início da última fase com progresso* e *popular as variáveis de progresso do jogo*, levando o player à última fase correspondente ao progresso salvo. *O jogo não deve salvar o progresso além da fase 3*, assim um player que completou o jogo pode repetir a luta final.
        - Slots preenchidos de saves tem a opção de deletar o save na parte de slots de saves. - Saves serão arquivos .csv com uma unica linha de 3 posições. Os marcadores 0 e 1 representam respectivamente a falta de progresso e progresso, colocados nas posições da linha do arquivo representam o progresso no jogo na fase que a posição corresponde da seguinte forma -> [tutorial, fase1, fase2]
        - Creditos mostra o nome do criador.
        - Sair fecha a janela do jogo.
[] Fazer o Mapa
    - O mapa deve ser um menu interativo(mouse) parecendo uma cidade, você interage com o mapa e ele te leva até a fase desejada no mapa desde que a fase esteja disponível. Fases deixam de ficar disponíveis quando o chefe final da fase correspondente é derrotado, então cada fase só pode ser jogada até o final uma única vez. Quando uma fase deixa de ficar disponível, indicado com o retorno de uma função fase, a dificuldade das outras aumenta em +1(a dificuldade deve ser uma variável do mapa que uma função fase recebe como input)

    o jogo será linear por falta de sprites e de tempo!!! ou seja sem mapa.



[] Fazer uma fase base
    - Uma fase base significa toda a estrutura comum para montar uma fase. Pra isso eu preciso de um ambiente que interage com sprites tangíveis, gravidade. Player que pula, anda e atira, inimigos que fazem o mesmo que o player menos pular, uma maneira de fazer um mapa que interage com as entidades tangíveis impedindo elas de avançar para baixo da tela, uma câmera que segue o player e impede que ele saia da tela.
[] Fazer a fase tutorial
    - Fase tutorial, nessa fase deve haver um curso de obstáculos que ensina os comandos básicos do jogo. Que são: Andar, pular, atirar.
[] Fazer a fase 1
    - Primeiro desafio, o player deve passar pelos inimigos da fase e prosseguir até o ultimo boss derrotando os inimigos no caminho e não caindo nos buracos, ao completar a fase o player ganha um upgrade de pulo, permitindo que ele tenha um pulo duplo
[] Fazer a fase 2
    -segundo desafio, o player deve passar pelos inimigos agora um pouco diferentes, um pouco mais perigosos, mais rápidos, mais tiros, mais inimigos. O ambiênte da fase deve estar um pouco mais diíficil também, espinhos mais buracos etc... o chefão da fase é estático mas perigoso, preparação para o chefe final. Ao derrotar essa fase o player escolhe entre uma melhora na cadência de tiros ou um dash que é bindado no shift. A escolha é feita e segue até a próxima fase
[] Fazer a fase 3(fase do boss)
    -Ao iniciar essa fase uma logo sinistra deve aparecer na tela e logo depois a musica muda, o ambiênte deve mudar drasticamente, a dificuldade também, inimigos agora são mortais, dão mais dano e se movem mais rápido, com bem mais inimigos. O chefe final desta fase demarca o final do jogo, a logo deve piscar de novo e a luta começa. Ao chefe final chegar em metade da vida ele se enfurece e sobem duas plataformas, o chão agora ganha a textura de lava(ou espinhos caso a animação da lava seja ruim)

    Ao derrotar o chefe um texto deve rolar demonstrando que o jogo acabou e deve voltar para o menu principal.
