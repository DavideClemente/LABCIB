# **LAB1: Avaliação e ataque de segurança a um Arduino (Máquina 14)**

# Introdução

O desenvolvimento deste projeto tem como objetivo a avaliar o conteúdo e realizar ataques de segurança a um Arduino.
O exercício encontra-se dividido em duas partes distintas:

-   **Parte 1**, envolvendo as seguintes etapas:
    -   **Development Password**: Ataque ao arduino, com o intuito de descobrir a password de acesso;
    -   **Firmware**: _Dump_ das várias partes da memória para ficheiros binários;
    -   **Confidential Information**: Análise do conteúdo da memória do arduino, com o objetivo de identificar informações confidenciais.
-   **Parte 2**, na qual se pretendia descobrir e descodificar a password que concede acesso ao C&C:
    -   **Identify Cryptographic Assets**: Análise do conteúdo dos ficheiros binários;
    -   **Find the pot of gold**: Utilização do `openssl` para extrair a _hash_;
    -   **Crach the code**: Descoberta de código de utilização única;
    -   **Connect to the C&C**: Descoberta do segredo final e conexão com o C&C.

# Parte 1

## Development password:

Os **_Timing attacks_** permitem avaliar o tempo de execução de uma determinada operação, de forma a ser possível retirar conclusões relevantes acerca do seu conteúdo. Tendo em conta o desafio deste projeto, a aplicação deste tipo de ataque mostrou-se bastante relevante sendo que permitiu a obtenção do comprimento da password e, ainda, do seu conetúdo.

### Determinação do Comprimento da Password

Para encontrar o comprimento correto da password, foi desenvolvido um _script_ que enviava _strings_ (constituídas por vários carateres iguais) de diferentes comprimentos para o Arduino, de forma a simular uma tentativa de _login_. Após receber a resposta do Arduino a indicar que a tentativa de _login_ tinha sido falhada, o _script_ imprimia os tempos de execução de cada uma das tentativas, de modo a ser possível avaliar qual dos _inputs_ despoletava um maior tempo de execução.

Após algumas tentativas, foi possível concluir que o Arduino demorarav mais tempo a enviar resposta quando o input podduía **13 carateres**, sendo esse o comprimento da password.

#### Funcionamento do Código:

-   **Comunicação com o Arduino**: a comunicação com o dispositivo foi configurada através da porta correta, com uma tax; de transmissão de _115200 bps_ e um _timeout_ de **0.1 segundos**.
-   **Medição do Tempo de Resposta**: para cada _input_ enviado (com comprimento ente 1 e 20 caracteres), o _script_ avalia o tempo de execução de cada iteração. Repetiu-se o processo várias vezes com comprimentos diferentes, para descobrir o comprimento da password;
-   **Filtragem de Outliers**: de forma a alcançar resultados mais precisos, foram removidos valores de tempo considerados atípicos: os **5% mais altos e mais baixos**.
-   **Determinação do Comprimento**: após o cálculo dos tempos de execução, foram analisados os resultados de forma a identificar os valores mais elevados. O comprimento que apresentava um valor mais elevado o maior número de vezes, foi o valor **13**, sendo este o comprimento da password. De forma a facilitar a validação dos resultados, foi gerado o seguite gráfico:
    []

### Descoberta dos Caracteres da Password

Com o comprimento da password determinado, o próximo passo consiste na identificação dos carateres. Para isso, foi desenvolvido outro _Timing Attack_, no qual eram injetados inputs com 13 carateres de "a" a "z" em várias posições, medindo os tempos de resposta.

#### Funcionamento do Código

-   **Construção do _input_**: o _script_ formula vários _inputs_ para cada letra do alfabeto, contendo a letra em poisções diferentes da password em cada execução.
-   **Medição dos tempos**: para cada uma das execuções foi calculado o tempo de execução;
-   **Identificação do carater correto**: para cada posição, a letra que apresenta o maior tempo de resposta é considerada o carater correto. Rpetiu-se este processo várias vezes até se descobrir todos os 13 carateres, obtendo a password completa.

## Memory Dump

Após a descoberta da password, foi possível listar as regiões de memória do arduino, bem como aceder ao seu conteúdo.
Através do script `dump_mem.py` foi possível extrair a memória das três regiões (EEPROM, PROGMEM, SRAM) para ficheiros binários.

## Confidential Information

Tendo acesso aos conteúdos em memória da máquina, em específico da região PROGMEM, foi possível identificar algumas credenciais expostas:

-   **Username e password do Dan (_Developer_):** dankmlacoguqo
-   **Username e password do Alan (_Admin_):** alancusxrgsmqehqnjoowytbultpxchcmjguerwsiabwskptfiqcls

Com a descoberta da password do administrador foi possível aceder à consola de admin, levando ao próximo desafio: descobrir a password do C&C.

# Parte 2

## Identify Cryptographic Assets

Ainda relativamente aos conteúdos expostos da região **PROGMEM**, foi também possível identificar dois registos criptográficos que poderiam ser relevantes para o processo de acesso ao C&C.

Assim, após alguma análise, concluímos que se tratavam de um conjunto de chave privada e mensagem cifrada, relativos ao
protocolo de criptografia de chaves públicas (criptografia assimétrica) **RSA**.

## Find the pot of gold

Tendo descoberto estas informações, iniciamos uma pesquisa acerca de ferramentas que permitissem a desencriptação da mensagem aproveitando a chave privada.
Assim, concluímos que a ferramenta **openssl**, uma ferramenta de código _open source_, permitiria obter a mensagem desencriptada.
Para isso foi necessário executar os passos seguintes:

-   Criar um ficheiro `.pem` contendo o conteúdo da chave privada, adicionando o cabeçalho e rodapé obrigatórios numa
    chave privada RSA (`private_key.pem`).
-   Criar um ficheiro `.txt` contendo o conteudo encriptado da mensagem (`encrypted.txt`)
-   Executar os comandos seguintes:

    -   `openssl base64 -d -in encrypted.txt -out encrypted.bin`

    -   `openssl rsautl -decrypt -inkey private_key.pem -in encrypted.bin -out decrypted.txt`

Após a execução dos comandos, foi possível concluir que o conteúdo original se tratava de uma hash
(`{"hash": "210e076a4ffb6080feedb411af7b20ac"}`).
Fazendo uso da _rainbow table_ fornecida pelos professores, encontrámos a mensagem original correspondente à hash (`cncsgnczxkvywinoldnbpjfjlcnsxjiqrabdfycuqsrsgslzuhpaq`).
Esta _string_ revelou-se ser a password do C&C.

## Crack the code

O último obstáculo para descobrir o segredo final era descobrir um código de uso único.
Segundo o enunciado, a equipa de _reverse engineering_ tinha encontrado um bug no qual os códigos se começavam a repetir ao fim de algumas tentativas.
Sendo que essa era a nossa única _hint_, decidimos seguir essa abordagem e criar um script `otpCracker.py`.
Este script regista todos os códigos que vão sendo gerados pela máquina, e quando deteta uma repetição, significa que já sabemos qual será o próximo código.
Esta etapa revelou-se bastante aleatória em termos temporais, podendo a repetição acontecer ao fim de 10, 15 ou até 20 minutos.

## Connect to the C&C

Com o código de uso único descoberto foi então possível aceder ao segredo final **sailducknailisland**!
