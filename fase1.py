import matplotlib.pyplot as plt


class gruposangDescriptor:
    # Grupos sanguíneos válidos
    GRUPOS_VALIDOS = {"A", "B", "AB", "O"}

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self

        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        # Convertir a mayúsculas
        value = value.upper()

        # Permitir 0 como O
        if value == "0":
            value = "O"

        # Comprobar que el grupo es válido
        if value not in self.GRUPOS_VALIDOS:
            raise ValueError(
                "Grupo sanguíneo no válido. Usa A, B, AB u O."
            )

        instance.__dict__[self.name] = value


class Padres:

    # Descriptores de los grupos de los padres
    grupo_padre = gruposangDescriptor()
    grupo_madre = gruposangDescriptor()

    def __init__(self, padre, madre):
        self.grupo_padre = padre
        self.grupo_madre = madre


class Descendencia:

    # Genotipos posibles para cada grupo
    GENOTIPOS = {
        "A": ["AA", "AO"],
        "B": ["BB", "BO"],
        "AB": ["AB"],
        "O": ["OO"]
    }

    def __init__(self, padres):
        self.padres = padres

    def _gametos(self, genotipo):
        # Obtener los alelos
        return list(genotipo)

    def _resultado_genotipo(self, alelo1, alelo2):
        # Combinar los dos alelos
        genotipo = alelo1 + alelo2

        # A y B son codominantes
        if "A" in genotipo and "B" in genotipo:
            return "AB"

        # A domina sobre O
        elif "A" in genotipo:
            return "A"

        # B domina sobre O
        elif "B" in genotipo:
            return "B"

        # OO produce el grupo O
        else:
            return "O"

    def _cruzamiento(self, genotipo_padre, genotipo_madre):
        resultados = []

        # Obtener los alelos posibles
        gametos_padre = self._gametos(genotipo_padre)
        gametos_madre = self._gametos(genotipo_madre)

        # Combinar los alelos
        for alelo_padre in gametos_padre:
            for alelo_madre in gametos_madre:
                resultado = self._resultado_genotipo(
                    alelo_padre,
                    alelo_madre
                )

                resultados.append(resultado)

        return resultados

    def calcular_posibilidades(self):
        resultados = []

        # Obtener los genotipos posibles
        genotipos_padre = self.GENOTIPOS[self.padres.grupo_padre]
        genotipos_madre = self.GENOTIPOS[self.padres.grupo_madre]

        # Calcular las combinaciones
        for genotipo_padre in genotipos_padre:
            for genotipo_madre in genotipos_madre:
                resultados.extend(
                    self._cruzamiento(
                        genotipo_padre,
                        genotipo_madre
                    )
                )

        total = len(resultados)

        # Calcular los porcentajes
        porcentajes = {
            "A": resultados.count("A") / total * 100,
            "B": resultados.count("B") / total * 100,
            "AB": resultados.count("AB") / total * 100,
            "O": resultados.count("O") / total * 100
        }

        # Eliminar grupos con 0%
        return {
            grupo: porcentaje
            for grupo, porcentaje in porcentajes.items()
            if porcentaje > 0
        }

    def mostrar_resultados(self):
        resultados = self.calcular_posibilidades()

        print("\nPosibles grupos sanguíneos del descendiente:")

        # Mostrar los porcentajes
        for grupo, porcentaje in resultados.items():
            print(f"Grupo {grupo}: {porcentaje:.2f}%")

        self._mostrar_grafico(resultados)

    def _mostrar_grafico(self, resultados):
        grupos = list(resultados.keys())
        porcentajes = list(resultados.values())

        # Crear gráfico circular
        plt.figure(figsize=(7, 7))

        plt.pie(
            porcentajes,
            labels=grupos,
            autopct="%1.2f%%",
            startangle=90
        )

        plt.title(
            f"Posibles grupos sanguíneos\n"
            f"Padre: {self.padres.grupo_padre} - "
            f"Madre: {self.padres.grupo_madre}"
        )

        plt.show()


def main():
    print("HERENCIA DE GRUPOS SANGUÍNEOS")

    while True:
        try:
            padre = input(
                "Introduce el grupo sanguíneo del padre (A, B, AB, O/0): "
            )

            madre = input(
                "Introduce el grupo sanguíneo de la madre (A, B, AB, O/0): "
            )

            # Crear los padres
            padres = Padres(padre, madre)

            # Calcular la descendencia
            descendencia = Descendencia(padres)

            descendencia.mostrar_resultados()

            break

        except ValueError as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    main()