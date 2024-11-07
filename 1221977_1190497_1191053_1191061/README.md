steps to get c&c password

# Projeto: Descoberta de Password no Arduino com Timing Attack

# Introdução

Este projeto tem como objetivo realizar a descoberta de uma password em um dispositivo Arduino através de um timing attack. Utilizando essa técnica, medimos o tempo de resposta do Arduino para diferentes tentativas de password e, com base nesses tempos, identificamos os caracteres corretos da password.

## Development password:

Timing attacks (ou ataques temporais) são uma técnica de análise em que se mede o tempo de execução de uma operação para obter informações sobre dados sensíveis. No caso deste projeto, estamos a explorar o tempo de resposta do Arduino para tentativas de password incorretas, com a finalidade de determinar a password correta. Sabemos que a password tem 13 caracteres e é composta apenas por letras minúsculas (de 'a' a 'z').

O desenvolvimento do projeto foi dividido em duas etapas principais:

-   Determinação do comprimento da password.
-   Descoberta dos caracteres da password, um a um.
-   Estrutura do Projeto

## Determinação do Comprimento da Password

Para encontrar o comprimento correto da password, desenvolvemos um script que envia strings de diferentes comprimentos para o Arduino e mede o tempo de resposta. O comprimento que apresenta o tempo de resposta mais longo é considerado o provável comprimento da password.

### Funcionamento do Código:

-   Configuração de Comunicação com o Arduino: Configuramos a comunicação serial com o Arduino através da porta COM6 (ou outra porta, conforme necessário), com uma taxa de transmissão de 115200 bps e um tempo limite (timeout) de 0.1 segundos.
-   Medição do Tempo de Resposta: Para cada comprimento de string (de 1 a 20 caracteres), o script envia uma sequência de letras 'a' ao Arduino e mede o tempo de resposta até receber uma resposta completa. Este processo é repetido várias vezes para cada comprimento, permitindo uma média mais precisa dos tempos
-   Filtragem de Outliers: Para aumentar a precisão, removemos os valores de tempo considerados atípicos, ou seja, os 5% mais altos e mais baixos. Esta filtragem ajuda a evitar que valores fora do normal distorçam a média.
-   Análise e Determinação do Comprimento: Após calcular as médias dos tempos para cada comprimento, comparamos os resultados. O comprimento que consistentemente apresenta o tempo mais longo de resposta é o que corresponde ao comprimento correto da password, que neste caso foi identificado como 13 caracteres.

### Visualização dos Resultados:

Para facilitar a análise, os resultados médios dos tempos de resposta para cada comprimento de string são plotados num gráfico. Este gráfico permite identificar rapidamente o comprimento de string que resulta nos tempos mais longos, ajudando-nos a validar o comprimento correto da password.

## Descoberta dos Caracteres da Password

Com o comprimento da password determinado, o próximo passo é identificar cada um dos 13 caracteres. Para isso, utilizamos outro script que testa cada letra ('a' a 'z') em cada posição da password, medindo o tempo de resposta para cada tentativa.

Funcionamento do Código

-   Tentativa de Caracteres: Para cada posição da password (de 1 a 13), o script testa todas as letras do alfabeto. Cada letra é enviada ao Arduino, e o tempo de resposta é medido.
-   Identificação do Carácter Correto: Para cada posição, a letra que resulta no maior tempo de resposta é considerada o carácter correto. O processo repete-se até que todos os 13 caracteres sejam descobertos, construindo assim a password completa.

Instruções para Utilização:
Pré-requisitos:
Certifique-se de que tem o Python 3.x instalado no seu sistema.
Instale as bibliotecas necessárias: PySerial e Matplotlib, usando os seguintes comandos:

pip install pyserial matplotlib

Conectar o Arduino:
Conecte o Arduino à porta correta (ex: COM6). Confirme a porta antes de executar o script.

Execução do Script para Determinação do Comprimento da Password:
Execute o primeiro script Python que mede os tempos de resposta para comprimentos de 1 a 20 caracteres.
O script apresentará no final o comprimento da password que provocou o maior tempo médio de resposta.

Execução do Script para Descoberta da Password:
Após determinar o comprimento, execute o segundo script para identificar os caracteres.
O script tentará cada letra do alfabeto em cada posição e determinará a letra correta baseada no tempo de resposta mais longo.

Explicação do Código:
Código para Determinação do Comprimento da Password:
Este script realiza as seguintes tarefas:
-Estabelece a comunicação serial com o Arduino.
-Envia strings de diferentes comprimentos e mede os tempos de resposta.
-Filtra tempos de resposta atípicos e calcula a média para cada comprimento.
-Gera um gráfico com os tempos médios, permitindo identificar o comprimento mais provável da password.

Código para Descobrir a Password
Este script realiza as seguintes tarefas:
-Envia uma tentativa de cada letra ('a' a 'z') para cada posição da password de 13 caracteres.
-Mede o tempo de resposta para cada tentativa.
-Seleciona o carácter correto para cada posição com base no maior tempo de resposta.

Notas Importantes:
Timing Attack e Precisão: Este método depende da consistência do timing do Arduino para diferentes tentativas. O projeto filtra valores atípicos para melhorar a precisão, mas interferências de comunicação ou variabilidade podem afetar os resultados.
Limitações: A técnica é eficaz para descobrir passwords em sistemas que apresentam timings perceptíveis para operações de validação. Contudo, pode ser menos eficaz em sistemas que utilizam técnicas para mascarar tempos de resposta.

Conclusão
Este projeto exemplifica como timing attacks podem ser usados para descobrir uma password em um dispositivo Arduino, tirando proveito de tempos de resposta ligeiramente diferentes para diferentes caracteres e comprimentos de string. O timing attack é uma técnica poderosa, especialmente em sistemas sem proteção contra tais ataques, mostrando a importância de implementar medidas de segurança robustas em sistemas com dados sensíveis.

## Firmware

### Memory Dump

Após a descoberta da password, foi possível listar as regiões de memória do arduino, bem como aceder ao seu conteúdo.
Através do script `dump_mem.py` foi possível extrair a memória das três regiões (EEPROM, PROGMEM, SRAM) para ficheiros binários.

## Confidential Information

Tendo acesso aos conteúdos em memória da máquina, em específico da região PROGMEM, foi possível identificar algumas credenciais expostas:

-   Username e password do Dan (Developer): dankmlacoguqo
-   Username e password do Alan (Admin): alancusxrgsmqehqnjoowytbultpxchcmjguerwsiabwskptfiqcls

Com a descoberta da password do administrador foi possível aceder à consola de admin, levando ao próximo desafio: descobrir a password do C&C.

## Identify Cryptographic Assets

Ainda relativamente aos conteúdos expostos da região PROGMEM, foi também possível identificar dois registos criptográficos que poderiam ser relevantes para o processo de acesso ao C&C.

Assim, após alguma análise, concluímos que se tratavam de uma chave privada e de uma mensagem cifrada relativo a um protocolo de criptografia de chaves públicas (criptografia assimétrica), mais específicamente o protocolo RSA.

## Find the pot of gold

Tendo descoberto estas informações, iniciamos uma pesquisa acerca de ferramentas que permitissem a desencriptação da mensagem aproveitando a chave privada.
Assim, concluímos que a ferramenta **openssl**, presente na maioria das distribuições _linux-based_, permitiria obter a mensagem desencriptada.
Para isso foi necessário executar os passos seguintes:

-   Criar um ficheiro `.pem` contendo a chave privada e adicionando o cabeçalho e rodapé existentes numa chave RSA.
-   Criar um ficheiro `.txt` contendo o conteudo encriptado da mensagem
-   Executar os comandos seguintes:

    -   `openssl base64 -d -in encrypted.txt -out encrypted.bin`

    -   `openssl rsautl -decrypt -inkey private_key.pem -in encrypted.bin -out decrypted.txt`

Após a execução dos comandos, foi possível obter uma hash (mensagem desencriptada). Fazendo uso da _rainbow table_ fornecida pelos professores, retirámos a mensagem original correspondente à hash.
Esta mensagem revelou-se ser a password do C&C.

## Crack the code

O último obstáculo para descobrir o segredo final era descobrir um código de uso único.
Segundo o enunciado, a equipa de reverse engineering tinha encontrado um bug no qual os códigos se começavam a repetir ao fim de algumas tentativas.
Sendo que essa era a nossa única _hint_, decidimos seguir essa abordagem e criar um script `otpCracker.py`.
Este script regista todos os códigos que vão sendo gerados pela máquina, e quando deteta uma repetição, significa que já sabemos qual será o próximo código.
Esta etapa revelou-se bastante aleatória em termos temporais, podendo a repetição acontecer ao fim de 10, 15 ou até 20 minutos.

## Connect to the C&C

Com o código de uso único descoberto foi então possível aceder ao segredo final **sailducknailisland**!
