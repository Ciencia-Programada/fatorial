from functools import reduce
from operator import mul


def fatorial(numero):
    return reduce(mul, range(1, numero + 1)) if numero >= 1 else 1


if __name__ == '__main__':
    while True:
        try:
            n = int(input('Forneça um número inteiro: '))
        except ValueError:
            print('ERRO: Forneça um número inteiro positivo.')
        except KeyboardInterrupt:
            print(' Excecução finalizada pelo usuário.')
            break
        else:
            print(fatorial(n))
