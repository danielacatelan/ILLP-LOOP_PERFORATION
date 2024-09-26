Pass é onde fica os arquivos modificados do accept;
somadores.h é onde fica todas as funções somadores para substituir no loop;
script.py lê accept_config.txt e baseado nele cria um novo .c, onde os loops escolhidos tera seu incremento modificado para o somador escolhido;

- somadores.h vai na pasta: accept/include/
- script.py fica na pasta do accept: accept/
- O Makefile fica junto com o .c que vai ser perfurado

O makefile tem 4 regras além das padrões do accept: construir_addx, construir_accept, construir_accept_spike e limpar

Para usar o make, execute o seguinte comando: make REGRA;     - substituindo REGRA, por uma das 4 regras
