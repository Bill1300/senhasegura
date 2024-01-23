<div align="center">
    <img  width="240"  src="https://i.imgur.com/fJ0Ku5x.png">
</div>

<span>Versão: 24.1.3 <a href="https://bill1300.github.io/senhasegura-docs/">Documentação ➜</a></span>

Este obra está licenciado com uma <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/">Licença Creative Commons Atribuição-NãoComercial-CompartilhaIgual 4.0 Internacional</a>.

A SenhaSegura é uma ferramenta open-source de cofre de senhas pessoais projetada para proporcionar máxima segurança e simplicidade na gestão de suas credenciais digitais. Desenvolvida com ênfase na privacidade e no controle do usuário, essa aplicação utiliza criptografia avançada para garantir a proteção robusta de suas senhas sensíveis.

Ao optar pela SenhaSegura, você escolhe uma solução de gerenciamento de senhas que coloca a segurança em primeiro lugar.


### Instalação ➜

Para instalar o programa execute o comando:

>$ bash installer&#46;sh

(É necessário a inserir a senha de super-usuário)

### Execução ➜

#### Como usar a plataforma ➜

Para inserir uma senha, insira as seguintes informações na seção de cadastro:

- **Título:** Utilizado para filtrar com a barra de pesquisa entre todas as senhas armazenadas.
- **Descrição:** Utilizado para fornecer informações adicionais abertas.
- **Usuário:** Utilizado para registrar informações do usuário, se necessário.
- **Senha:** Utilizado para armazenar a senha gerada ou não pela SenhaSegura.

<div align="center">
    <img  width="600"  src="https://i.imgur.com/ttGB9sd.png">
</div>

##### Mostrar/Ocultar ➜
A senha armazenada possui o título como a informação principal, facilitando a pesquisa na lista de senhas armazenadas, além de contar com uma descrição. As informações de usuário e senha estão ocultas e podem ser reveladas usando o botão "Mostrar".

##### Copiar ➜
Para copiar a senha para a área de transferência, utilize o botão "Copiar", mesmo quando a senha está oculta.

##### Editar ➜
Para alterar nas informações da senha, utilize o botão "Editar", que abrirá um formulário com seções editáveis. Após realizar as edições desejadas, utilize o botão "Salvar".

##### Deletar ➜
Para excluir uma senha, utilize o botão "Deletar", e em seguida, confirme a remoção clicando em "Confirmar" (ou pressionando a tecla **ENTER**) ou cancele a operação clicando em "Cancelar" (ou pressionando a tecla **ESC**). 

<div align="center">
    <img  width="600"  src="https://i.imgur.com/szRaT9c.png">
</div>

#### Parâmetros ➜
Para utilizar os parâmetros, inclua-os após a chamada do comando SenhaSegura, como no exemplo: senhasegura --ajuda.

| Comando | Descrição |
|---------|-----------|
| **-a** ou **--ajuda**         | **Apresentar ajuda:** Apresenta alguns parâmetros e funcionalidades, além do link para a documentação online da ferramenta.   |
| **-e** ou **--editar**        | **Editar senha:** Inicia a função de editar a senha de entrada da ferramenta. É necessária a senha atual.                     |
| **-h** ou **--historico**     | **Apresentar histórico:** Apresenta um breve histórico das últimas vezes que a ferramenta foi utilizada.                      |
| **-m** ou **--mostrar**       | **Mostrar senha:** Com este parâmetro as senhas são visíveis ao inserir. Pode ser combinada** c**om outros parâmetros de funções. |
| **-p** ou **--panico**        | **Definir pânico:** Inicia a função de definir uma senha pânico. A senha pânico quando inserida deleta todo o banco de dados com as senhas salvas de modo permanente. É necessária a senha atual. |
| **-x** ou **--exportar**      | **Exportar senhas:** Inicia a função de exportação de banco de dados com as senhas salvas, mas este arquivo não é criptografado. É necessário a senha atual.|
| **-v** ou **--versao**        | **Apresentar versão:** Apresenta a versão instalada.|

#### Editar senha ➜
O processo de edição da senha de entrada no sistema SenhaSegura é conduzido mediante a utilização dos parâmetros -e ou --editar. Após autenticar-se, é necessário inserir uma senha composta por 12 caracteres, abrangendo números, caracteres especiais, além de letras maiúsculas e minúsculas.

Toda essa informação é armazenada de maneira segura e criptografada no arquivo gerado denominado 'profile.json'. Este procedimento de armazenamento criptografado é fundamental para resguardar a integridade e confidencialidade. Após executar é apresentado:

>Senha alterada.

#### Apresentar histórico ➜

Para apresentar o histórico é essencial utilizar o parâmetro -h ou --historico. É apresentado uma lista com as seguintes informações:

>Data | Hora | Acesso

A data e a hora serão registradas conforme o horário da internet, caso haja uma conexão disponível. No entanto, na ausência de conexão, as informações locais do computador serão empregadas. No que diz respeito ao registro de acesso, se a autenticação for bem-sucedida, será registrado como "Permitido". Em contrapartida, se a autenticação for recusada devido a erros na inserção da senha, será registrado como "Recusado (erro ao inserir senha)".

#### Definir 'Pânico' ➜

O modo 'pânico' tem o objetivo de eliminar de maneira permanente todas as senhas armazenadas no arquivo db.sqlite3. Para configurar essa função, é necessário empregar o parâmetro -p ou --panico e entrar com a senha de acesso da SenhaSegura. Após autenticar-se, é necessário inserir uma senha composta por 12 caracteres, abrangendo números, caracteres especiais, além de letras maiúsculas e minúsculas. Uma vez estabelecida a senha, não é possível alterar esta senha.

Dessa maneira, ao inserir a senha 'pânico' ao invés senha correta, ocorre uma reinicialização do banco de dados, com todos as informações deletadas. Após executar é apresentado:

>Todas as senhas foram apagadas.

#### Exportar senhas ➜

Para realizar a exportação das senhas, é essencial utilizar o parâmetro **-x** ou **--exportar**, seguido da inserção da senha de acesso a SenhaSegura. Após a autenticação correta, é fundamental indicar o diretório de destino onde o arquivo será salvo. Ressalta-se que este arquivo não possui criptografia, portanto, é imprescindível exercer cuidado ao determinar o local de compartilhamento. Após executar é apresentado:

>O arquivo exportado para [endereço] **NÃO** está criptografado.

### Estrutura de arquivos ➜

<div align="center">
    <img  width="600"  src="https://i.imgur.com/JvleeID.png">
</div>

### *Feedback* ➜
Você teve algum problema ao executar? Alguma ideia de funcionalidade nova?
[Escreva aqui  ➜](https://forms.gle/r15EZ2fjyhTE44y2A)