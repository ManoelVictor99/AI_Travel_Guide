import sys

from vector_store import indexar_base_de_conhecimento


def main():
    print("\n🔍 Verificando/Indexando base de conhecimento no Pinecone...")

    # Garante que a base esteja indexada antes de carregar as chains
    indexar_base_de_conhecimento()

    # Importa as chains APÓS garantir que o índice existe no Pinecone
    from chains import processar_consulta

    print("\n" + "=" * 65)
    print("🌍 WELCOME TO AIGENTE-TURÍSTICO - SISTEMA INTELIGENTE DE VIAGENS 🏖️")
    print("=" * 65)

    while True:
        try:
            consulta = input(
                "\n✈️ Digite sua pergunta sobre a viagem (ou 'sair'): "
            ).strip()

            if consulta.lower() in ["sair", "exit", "quit", "s"]:
                print("\n👋 Até logo e boa viagem!")
                break

            if not consulta:
                continue

            categoria, cadeia_usada, resposta = processar_consulta(consulta)

            print("\n" + "=" * 65)
            print(f"📌 Módulo Ativado: {cadeia_usada}")
            print("=" * 65)
            print(resposta)
            print("=" * 65)

        except KeyboardInterrupt:
            print("\n👋 Sistema encerrado pelo usuário.")
            sys.exit(0)

        except Exception as e:
            print(f"❌ Erro ao processar solicitação: {e}")


if __name__ == "__main__":
    main()