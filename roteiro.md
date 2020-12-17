# Você está aprendendo a programar de forma errada


É muito comum quando estamos começando a aprender Python ou qualquer outra linguagem de programação utilizarmos um livro, site de referência ou algum outro tipo de material. E esses materiais geralmente possuem exercícios para praticar, o que é muito bom. No entanto, raramente alguma instrução de como estruturar o ambiente de estudo do ponto de vista de organização de código e organização dos seus arquivos é fornecida. E, especialmente, raramente se apresenta a linha de raciocínio mais eficiente para explorar um problema sem ter que rodar um script várias vezes para verificar se o mesmo funciona ou não.

Recentemente fiz um vídeo no canal abordando essa questão, mostrando como organizar um repositório git, criar uma estrutura de pastas que faça sentido e como desenvolver com testes.

/* Embbed do vídeo do canal https://www.youtube.com/watch?v=SB3yRNqP-U4 */

Hoje vou detalhar esse último ponto, explorando mais o procedimento conhecido como TDD *Test Driven Development*.  

## Definindo nosso problema

Vamos simular a resolução de um dos exercícios mais comuns em diversos materiais para iniciantes: escrever um programa que calcule o fatorial de um número inteiro.

Para quem não lembra, o fatorial de um número inteiro *n* é definido como:

$$
n! = n \times (n-1) \times \dots \times 2 \times 1
$$

havendo dois casos limites: os fatoriais dos números 0 e 1 são ambos iguais a 1.

Vamos começar vendo como NÃO devemos resolver o problema.

## Como NÃO resolver problemas

Pare e pense um pouco sobre sua relação com seu computador. Você possui formas de passar informações ao computador, geralmente via mouse ou teclado, e usualmente espera algo em troca, boa parte das vezes com informações em tela, embora possa ser também a impressão de algo, a reprodução de som, dentre outras cada vez mais diversas possibilidades. Mas a exibição de algo em tela ainda é a saída mais predominante. 

Essa relação está tão entranhada que raramente paramos para pensar nela e você pode estar achando estranho eu ter me dado ao trabalho de escrever "tamanha obviedade". Mas isso define muito de nossas expectativas e da maneira de pensar que adotamos ao programar. Identificar nossas próprias expectativas é algo importante, fica a dica.

Tanto é assim, que diversos materiais introdutórios focam em entrada/saída e criam um vício no estudante de sempre pensar em solicitar uma entrada a um usuário imaginário e retornar uma saída a esse usuário. Perceba, retornar não no sentido de `return` de uma função e, sim, no sentido de algo aparecendo na tela, retorno visual, usualmente um `print`.

Logo, a primeira etapa que muitos pensariam é "*Bom, preciso solicitar a entrada de um número inteiro por parte do usuário*". Algo como
```python
# fatorial.py

n = input('Forneça um número inteiro: ')
```

Obviamente que ao rodar tal script, não vai acontecer muita coisa, já que estamos apenas solicitando um input do usuário:
```shell
$ python fatorial.py
Forneça um número inteiro: 5

Process finished with exit code 0
```

No caso acima, o usuário passou o número 5 e o programa finalizou, já que efetivamente não há mais instrução alguma em nossa script.

Em uma segunda etapa passaríamos a tentar resolver o problema. Digamos que depois de pensar um pouco você chegou na seguinte linha de raciocínio: "*Como se trata de uma multiplicação, e o elemento neutro da multiplicação é o número 1, vou inicializar uma variável com esse valor e criar um loop para multiplicar essa variável por cada inteiro no intervalo de 1 até n*". Ah, e claro, exibir o resultado ao usuário com um `print`. É uma linha de raciocínio válida, o código de nosso arquivo `fatorial.py` seria algo do tipo:
```python
n = input('Forneça um número inteiro: ')

r = 1  # variável que armazenará o resultado
for i in range(1, n):
    r *= 1

print(r)
```

E aí? Esse código vai funcionar? Pense um pouco. Pensou? Vamos ver o resultado de rodar nosso arquivo:
```shell
$ python fatorial.py
Forneça um número inteiro: 5

Traceback (most recent call last):
  File "fatorial.py", line 4, in <module>
    for i in range(1, n):
TypeError: 'str' object cannot be interpreted as an integer

Process finished with exit code 1
```

Ora, ora... não funcionou. Por que? Simples, a função `input` por padrão retorna o que foi passado pelo usuário como *string* e não faz sentido utilizar uma string na função `range`. Aí você fica um pouco injuriado, mas percebe que pode resolver esse problema passando todo o input como parâmetro da função `int`, de forma a transformar a string em um tipo inteiro reconhecido pelo Python. Eis nosso arquivo `fatorial.py` novo:
```python
n = int(input('Forneça um número inteiro: '))

r = 1  # variável que armazenará o resultado
for i in range(1, n):
    r *= 1

print(r)
```

Agora vai, né? Não... Experimente rodar esse código, e passe o número 5 como entrada. O resultado deveria ser 120, mas você irá obter 24. Ou seja, o código está errado.

Mas antes de resolver o problema corretamente, vamos avaliar as etapas de nosso método de resolução e verificar quantas vezes efetivamente buscamos resolver o problema do fatorial:

1) solicitar input do usuário;
2) pensar em algoritmo de resolução;
3) exibir o resultado para o usuário (`print`);
4) resolver problema de converter string para int;
5) corrigir o algoritmo.

Veja que, de cinco etapas, apenas em duas (2 e 5) efetivamente estávamos pensando em como resolver o problema do fatorial. Nas demais etapas são problemas paralelos que surgem pela preocupação com entrada e saída, não relacionados com a resolução do problema em si.

Além disso, há outros problemas no método:

- variáveis com nomes ruins. Afinal, o que é `r`? É fácil reconhecer o significado sem ler o comentário?
- o código trata dos casos limite (fatoriais dos números 0 e 1)? Como saber olhando apenas o código?
- baixa capacidade de integração, de reusabilidade. Se você quiser utilizar esse cálculo em outro programa, após corrigir a conta obviamente, terá dificuldade de importar já que a conta não está encapsulada em uma função ou classe.
- e, o principal problema, **você tem que rodar o código e passar um número toda vez que deseja verificar se o programa está funcionando corretamente**!

Esse último ponto deveria saltar aos seus olhos. Século XXI, homem já foi à Lua, já mandou sonda além das fronteiras do sistema solar, você provavelmente tem um celular magnífico ao seu alcance que pode te conectar virtualmente a qualquer pessoa do outro lado do planeta... mas você não está utilizando o computador para aquilo que ele faz de melhor: **automatizar tarefas repetitivas!**.

Imagine que você demore um certo tempo até perceber o erro do código. Quantas vezes você irá rodá-lo para ir testando suas alterações, cada vez que roda tendo que passar um número inteiro? E, claro, por segurança você, ao encontrar o valor correto para um número inteiro de escolha, ainda terá que rodar novamente seu código para ver se ele funciona para os casos limite. Sério, é muita repetição manual. E olha que estamos falando de um problema relativamente simples. Imagine problemas mais complexos, problemas reais onde provavelmente quebraremos um problema em etapas menores. Testar manualmente cada uma... no dicionário esse tipo de situação é definida como *trabalho de corno*.

Vamos então ver a forma mais eficiente de abordar problemas em programação.

## As bibliotecas de teste

Coloque uma coisa na cabeça: se você como iniciante está passando por algum problema, é muito provável que diversas pessoas antes de você já passaram pelo mesmo e alguma solução foi desenvolvida. Logo, se o problema é ter que repetir testes manualmente, alguém já deve ter parado para desenvolver formas de fazer testes automatizados. E, sim, atualmente todas as linguagens mais conhecidas possuem uma ou mais ferramentas para essa finalidade.

Inclusive, em Python, há uma biblioteca que vem por padrão chamada `unittest`, cuja documentação se encontra [aqui](https://docs.python.org/3/library/unittest.html). Veja, não precisa nem instalar, indicando que os desenvolvedores da linguagem consideram o assunto importante o suficiente para fazer parte da instalação padrão. No entanto, a `unittest` é um pouco burocrática e verbosa de forma que a comunidade acabou por desenvolver o `pytest`.

O [pytest](https://docs.pytest.org/en/stable/) é mais simples de compreender e escala bem em casos complexos, sendo muito utilizado. A instalação é bem simples, utilizando `pip` ou `conda` a depender do [gerenciamento de ambiente](https://cienciaprogramada.com.br/2020/08/ambiente-virtual-projeto-python/) que você está utilizando.

Se rodarmos o comando `pytest` na linha de comando no diretório de nosso arquivo, veremos algo parecido com o seguinte:
```shell
$ pytest
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-6.x.y, py-1.x.y, pluggy-0.x.y
rootdir: /fatorial
collected 0 items

=========================== no tests run in 0.00s ==========================
```

O comando não encontrou teste algum, já que não escrevemos testes ainda. Vamos agora conhecer o famigerado TDD.

## TDD - Test Driven Development

Vamos apagar todo o conteúdo de nosso arquivo `fatorial.py` e começar a escrever nosso primeiro teste. Por padrão, o pytest irá reconhecer como teste qualquer função que comece com o padrão `test*`. Assim, vamos fazer um teste do caso limite do inteiro 0:
```python
def test_fatorial_zero():
    assert fatorial(0) == 1
```

Vamos entender o que acabamos de escrever. Criamos uma função para testar o fatorial de 0 (perceba a importância de nomear adequadamente). Essa função busca se assegurar (papel do `assert`) de que quando o número 0 for passado para uma função `fatorial` (já fomos direcionados a encapsular nosso código em uma função) o resultado seja igual (`==`) ao número inteiro 1. O resultado de um comando `assert` em Python é booleano (`True` ou `False`). Assim, o pytest irá prosseguir se o resultado for `True` e irá nos informar se for `False`, indicando qual o motivo de o teste não ter passado. Ao rodar o comando `pytest` em nosso diretório de trabalho:
```shell
$ pytest
============================== test session starts ===============================
platform linux -- Python 3.x.y, pytest-6.x.y, py-1.x.y, pluggy-0.x.y
rootdir: /fatorial
collected 1 item

fatorial.py F                                                               [100%]

==================================== FAILURES ====================================
_______________________________ test_fatorial_zero _______________________________

    def test_fatorial_zero():
>       assert fatorial(0) == 1
E       NameError: name `fatorial` is not defined 

fatorial.py:2: NameError
============================ short test summary info =============================
FAILED fatorial.py::test_fatorial_zero - NameError: name `fatorial` is not defined
=============================== 1 failed in 0.06s ================================
```

Observe que o pytest nos mostra um relatório bem completo indicando que nosso teste falhou. O motivo de ter falhado? Bem óbvio, não existe nenhuma função chamada `fatorial`. Assim, já sabemos qual nosso próximo passo, criar uma função chamada fatorial.

Perceba como o mecanismo de resolução mudou. Agora nós começamos pensando no resultado que queremos obter, escrevemos um teste para automatizar a verificação do resultado e fomos direcionados a encapsular nossa resolução numa função. E a falha do teste já nos indica qual a próxima etapa a ser feita. Estamos sendo guiados pelo teste, a essência do TDD.

Vamos adicionar ao início de nosso arquivo a seguinte função:
```python
def fatorial(numero):
    pass
```

Veja, não fizemos o corpo da função ainda, apenas a criamos. Afinal, esse é o mínimo necessário para corrigir a mensagem de erro do teste. Vamos novamente rodar o pytest:
```shell
$ pytest
============================== test session starts ===============================
platform linux -- Python 3.x.y, pytest-6.x.y, py-1.x.y, pluggy-0.x.y
rootdir: /fatorial
collected 1 item

fatorial.py F                                                               [100%]

==================================== FAILURES ====================================
_______________________________ test_fatorial_zero _______________________________

    def test_fatorial_zero():
>       assert fatorial(0) == 1
E       assert None == 1
E        + where None = fatorial(0)

fatorial.py:6: AssertionError
============================ short test summary info =============================
FAILED fatorial.py::test_fatorial_zero - assert None == 1
=============================== 1 failed in 0.06s ================================
```

**O erro mudou. E isso é ótimo, indica que evoluímos.** Agora o erro indica que `None` não é igual a 1. Toda função em Python retorna algo. Quando não definimos o que é para retornar, por padrão o retorno é `None`. Assim, faz sentido a mensagem de erro, pois não definimos o retorno de nossa função. Qual a forma mais fácil de resolver a mensagem de erro? Ora:
```python
def fatorial(numero):
    return 1
```

Rodando o pytest novamente:
```shell
$ pytest
============================== test session starts ===============================
platform linux -- Python 3.x.y, pytest-6.x.y, py-1.x.y, pluggy-0.x.y
rootdir: /fatorial
collected 1 item

fatorial.py .                                                               [100%]

=============================== 1 passed in 0.01s ================================
```

O teste passou.

Mas você pode estar pensando "*Tá, mas o problema do fatorial não foi resolvido, a função retorna 1 sempre*". Sim, evidente. Mas como podemos resolver o problema? Criando mais testes até que um conjunto mínimo de casos esteja coberto e os testes desses casos estejam passando. E, veja, o caso do fatorial de 0 já possui um teste que sempre será executado. Não preciso futuramente me preocupar com esse caso, nem preciso testá-lo manualmente. Está automatizado.

O próximo teste mais óbvio é o do número 1, vamos adicionar ao final de nosso arquivo:
```python
def test_fatorial_um():
    assert fatorial(1) == 1
```

Nesse caso, ao rodar o comando pytest, teremos dois testes passando, já que nossa função sempre retorna 1.
```shell
$ pytest
============================== test session starts ===============================
platform linux -- Python 3.x.y, pytest-6.x.y, py-1.x.y, pluggy-0.x.y
rootdir: /fatorial
collected 2 items

fatorial.py ..                                                              [100%]

=============================== 2 passed in 0.01s ================================
```

Qual o próximo passo? Criar um teste para fatorial de 2 e fazê-lo passar. 
```python
def test_fatorial_dois():
    assert fatorial(2) == 2
```

A seguinte alteração na função é suficiente:
```python
def fatorial(numero):
    if numero in (0, 1):
        return 1
    else:
        return numero
```

Consegue enteder por que essa alteração funciona? Rode os testes e verifique que todos os testes passam.

E depois? Escreva um teste para o número 3 e modifique a função `fatorial` até que todos os testes passem. Depois? O mesmo para o número 4. Depois? Bom, provavelmente sua lógica já está correta, já que os casos dos números 3 e 4 já são suficientes para verificar a multiplicação. Seu problema está resolvido! Fica de exercício para você escrever os casos de teste. Lembre-se de dar nomes adequados para as funções de teste.
 
Vou deixar aqui quatro formas de definir a função fatorial, todas passam. Mas tente fazer sua resolução antes de olhar as minhas, OK? Fiz e expliquei todas no vídeo linkado no início do artigo, veja o vídeo caso tenha dúvidas.
```python
def fatorial(numero):
    resultado = 1

    for n in range(1, numero + 1):
        resultado *= n
    return resultado
```
```python
def fatorial(numero):
    resultado = 1
    while numero > 1:
        resultado *= numero
        numero -= 1
    return resultado
```
```python
def fatorial(numero):
    if numero in (0, 1):
        return 1
    else:
        return numero * fatorial(numero - 1)
```
```python
def fatorial(numero):
    return reduce(mul, range(1, numero + 1)) if numero > 1 else 1
```

E agora que todos os testes passam e o problema está resolvido? O que fazer?

## O pós TDD

Uma vez que há casos de teste bem definidos e que cobrem o as situações previstas, sua liberdade aumenta.

### Versione seu código

Você pode buscar formas diferentes de resolver o problema, sabendo que se fizer alguma besteira um ou mais testes irão falhar e basta retornar ao código que estava passando. E para retornar? Bom, utilize versionamento de código. Com [git](https://git-scm.com/), por exemplo. Assim, recomendo que quando o código estiver estabilizado você faça um commit para ter um ponto de retorno. Novamente, o vídeo no início do artigo trata também de repositórios git e como se trabalha com controle de versão.

### Separe seu(s) arquivo(s) de teste

Aqui, por simplicidade, coloquei os testes no mesmo arquivo do código da função em si. No entanto, em projetos maiores, é mais conveniente separar os testes do código operacional. No nosso exemplo, uma estrutura poderia ser:

.
|--- fatorial.py
|--- test_fatorial.py

Essa é a estrutura que pode ser vista no [repositório desse artigo](https://github.com/Ciencia-Programada/fatorial). Em casos mais complexos, uma pasta para testes onde haveria um arquivo de testes para cada módulo do projeto pode ser interessante. Tudo depende de seu contexto e necessidade. O pytest é bem eficiente em encontrar testes no projeto.

### Busque a forma mais eficiente

Pode ser que aconteça como no nosso exemplo aqui e você encontre diversas formas distintas de resolver o problema. Qual usar? Depende do seu contexto. Sua necessidade é velocidade? Verifique o tempo de execução das diferentes formas com `timeit` do IPython, sobre o qual já fiz [vídeo e escrevi aqui](https://cienciaprogramada.com.br/2020/09/aprenda-python-interpretador-interativo/). Sua necessidade é escalabilidade? É suportar múltiplos acessos? A forma mais eficiente vai depender da sua necessidade, você pode inclusive criar testes que simulem sua situação utilizando o [`mock` do pytest](https://github.com/pytest-dev/pytest-mock/), por exemplo.

### Automatize mais ainda os testes com sua IDE

Boa parte dos editores e IDEs modernos possuem ferramentas de teste integradas. O PyCharm e o VSCode, por exemplo, podem ser configurados para se integrarem com o Pytest de forma que você não precisa mais rodar o comando pytest no terminal. Assim, rodar os testes fica ao alcance de um simples atalho. 

### Faça sua interface com o usuário

Começamos o artigo mostrando como é ineficiente usar input manual para testar código e como isso gera problemas paralelos que nos afastam do cerne da resolução. Porém, depois de resolvido, nada impede que você crie sua interface com o usuário. No [repositório desse artigo](https://github.com/Ciencia-Programada/fatorial) você encontra uma versão do `fatorial.py` onde uma interface de linha de comando foi desenvolvida.

## Conclusão

E aí? Curtiu TDD? Espero que tenha percebido a importância do assunto e como ele pode melhorar seu fluxo de trabalho com código. Caso tenha algo a acrescentar, deixe um comentário. Compartilhe o artigo com pessoas que desejam melhorar a forma de programar e, de quebra, ainda ajude a divulgar o Ciência Programada.

Até o próximo artigo.
