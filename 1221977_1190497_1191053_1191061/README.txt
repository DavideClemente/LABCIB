README.txt - Projeto: Descoberta de Password no Arduino com Timing Attack
Introdução
Neste projeto, desenvolvemos um programa para descobrir a password de um dispositivo Arduino através de um timing attack. Sabemos que a password tem 13 caracteres e é composta por letras minúsculas (de 'a' a 'z'). O nosso objetivo foi medir o tempo de resposta do Arduino a diferentes tentativas de password e, com base nesses tempos, identificar os caracteres corretos da password.

Estrutura do Projeto
Este projeto foi desenvolvido em duas partes:

Determinar o Comprimento da Password: Usámos um script que mede os tempos de resposta do Arduino para strings de diferentes comprimentos (de 1 a 20 caracteres) e analisámos qual o comprimento que provoca o maior tempo de resposta. Descobrimos que a password tinha 13 caracteres, porque esse foi o comprimento que consistentemente apresentou o tempo mais longo.

Descoberta da Password: Depois de determinar que a password tinha 13 caracteres, desenvolvemos um segundo script para descobrir cada carácter individualmente. Testámos todas as letras ('a' a 'z') para cada posição da password e medimos os tempos de resposta. O carácter com o maior tempo de resposta foi considerado o correcto para cada posição.

Explicação do Código para Determinar o Comprimento da Password
O script que usamos para descobrir o comprimento da password realiza os seguintes passos:

Comunicação com o Arduino: Configurámos a comunicação serial através da porta COM6 (ou outra porta disponível) com uma taxa de transmissão (baud rate) de 115200 bps e um timeout de 0.1 segundos.

Medição do Tempo de Resposta: Para cada string de comprimento variável (de 1 a 20 caracteres), o script envia uma string composta por letras 'a' para o Arduino e mede o tempo de resposta até receber uma resposta completa. Fazemos isto várias vezes para cada comprimento, repetindo o processo em várias iterações para obter uma média mais fiável.

Filtragem de Outliers: Para melhorar a precisão, removemos os valores de tempo que são atípicos (os 5% mais altos e mais baixos), garantindo que a média final de tempos é mais representativa dos resultados reais.

Análise e Pontuação: Para cada comprimento de string, somamos a pontuação das suas iterações. Os comprimentos que apresentaram consistentemente tempos mais longos são considerados os mais prováveis para a password. Assim, descobrimos que o comprimento da password era 13 caracteres.

Plotagem dos Resultados: Os resultados finais são plotados num gráfico que mostra os tempos de resposta médios para cada comprimento de string. Isto ajuda a visualizar quais os comprimentos que provocam os tempos de resposta mais longos.

Como Usar o Código:

Ligar o Arduino: Certifique-se de que o Arduino está ligado e conectado à porta correta (neste caso, COM6).

Executar o Código: Basta correr o ficheiro Python. O código vai testar diferentes comprimentos de strings e, no final, determinar qual o comprimento mais lento (o que corresponde ao comprimento da password).

Dependências: O programa requer Python 3.x e as bibliotecas PySerial e Matplotlib. Pode instalá-las com os seguintes comandos:

pip install pyserial matplotlib

Explicação do Código para Descobrir a Password:
Depois de determinar o comprimento da password, usamos um segundo script para descobrir os caracteres. O funcionamento é semelhante ao anterior, mas desta vez o script tenta cada letra ('a' a 'z') em cada posição da password, medindo o tempo de resposta de cada tentativa.

Para cada posição, o carácter que provocou o maior tempo de resposta é assumido como correto, e o processo repete-se até que todos os 13 caracteres sejam descobertos.

