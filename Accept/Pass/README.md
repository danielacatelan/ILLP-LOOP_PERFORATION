accept.h:

Foi adicionado uma nova variavel para guardar o valor da escolha da perfuração:
Linha 173:   std::map<std::string, int> doIt;

 
loopperf.cpp

Foi modificado a instrução que decide qual loop sera perfurado considerando o parametro, para tambem considerar o valor de escolha da perfuração.
Linha 132:   if (param && (!condi)) {


transform.cpp

Foi adicionado uma nova varialvel '1' no arquivo accept_config.txt que sera a escolha de perfuração, como tambem instruções para ler e salvar essa variavel.
Linha 158:   configFile << i->second << " " << "1" << " " << i->first << "\n";
Linha 179:   configFile >> var;
Linha 180:   configFile.ignore();
Linha 183:   doIt[ident] = var;

Após modificar esse arquivos, vá até a pasta do accept: accept/ e executa o seguinte comando:
    sudo make accept
