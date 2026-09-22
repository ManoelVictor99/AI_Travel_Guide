import sys

from vector_store import indexar_base_de_conhecimento


def exibir_menu():
    print("\n" + "=" * 70)
    print("🌍 AIGENTE-TURÍSTICO - SISTEMA INTELIGENTE DE VIAGENS")
    print("=" * 70)

    print("\nExemplos de perguntas:")

    print(" • Monte um roteiro de 3 dias em Paris.")
    print(" • Quais são os melhores restaurantes veganos do Rio de Janeiro?")
    print(" • Como ir do aeroporto Charles de Gaulle ao centro de Paris?")
    print(' • Como dizer "Onde fica o banheiro?" em francês?')

    print("\nDigite 'sair' para encerrar.")

    print("=" * 70)


def imprimir_resposta(cadeia_usada: str, resposta: str):
    print("\n" + "=" * 70)
    print(f"📌 Módulo Ativado: {cadeia_usada}")
    print("=" * 70)
    print()

    print(resposta.strip())

    print("\n" + "=" * 70)


def main():

    print("\n🔍 Verificando e indexando a base de conhecimento...")

    try:
        indexar_base_de_conhecimento()

    except Exception as e:
        print(f"\n❌ Erro durante a indexação:\n{e}")
        return

    # Importa somente após garantir que o índice existe
    from chains import processar_consulta

    exibir_menu()

    while True:

        try:

            consulta = input(
                "\n✈️ Digite sua pergunta sobre a viagem: "
            ).strip()

            if not consulta:
                continue

            if consulta.lower() in (
                "sair",
                "exit",
                "quit",
                "q",
                "s",
            ):
                print("\n👋 Obrigado por utilizar o AIgente-Turístico!")
                print("Boa viagem! 🌎")
                break

            categoria, cadeia_usada, resposta = processar_consulta(
                consulta
            )

            imprimir_resposta(cadeia_usada, resposta)

        except KeyboardInterrupt:

            print("\n\n👋 Encerrando o sistema...")
            sys.exit(0)

        except Exception as e:

            print("\n❌ Ocorreu um erro durante o processamento.")
            print(e)


if __name__ == "__main__":
    main()
