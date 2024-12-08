# Problema: Clasificación de Productos según su Aceptación por Clientes
Descripción del Problema
Una empresa desea predecir si un producto será aceptado o rechazado por los clientes basándose en las siguientes características:

Precio relativo: Precio del producto en comparación con productos similares (normalizado entre 0 y 1).
Calidad percibida: Opinión de los clientes sobre la calidad del producto en encuestas (normalizada entre 0 y 1).
Criterios de Clasificación:

Un producto se considera aceptado si cumple:
El precio relativo es menor o igual a 0.6.
La calidad percibida es mayor o igual a 0.7.
En caso contrario, será rechazado.
Entradas del Perceptrón:

`x1`: Precio relativo (0-1).
`x2`: Calidad percibida (0-1).
Salida del Perceptrón:

`1`: Aceptado.
`0`: Rechazado.
Conjunto de Datos de Entrenamiento

Precio relativo	Calidad percibida	Resultado
0.5	         0.8	            1
0.6	         0.9	            1
0.7	         0.6	            0
0.4 	    0.5	                0
0.3 	    0.9             	1
0.8 	    0.4	                0

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Clase Perceptrón
class Perceptron:
    def __init__(self, input_size):
        self.weights = np.random.rand(input_size + 1)  # +1 para el sesgo

    def activation_function(self, x):
        return 1 if x >= 0 else 0

    def predict(self, inputs):
        weighted_sum = np.dot(inputs, self.weights[1:]) + self.weights[0]  # sesgo
        return self.activation_function(weighted_sum)

    def fit(self, X, y, epochs, lr):
        for _ in range(epochs):
            for inputs, label in zip(X, y):
                prediction = self.predict(inputs)
                error = label - prediction
                self.weights[1:] += lr * error * inputs
                self.weights[0] += lr * error  # actualizar sesgo

# Función para generar datos de prueba
def generate_test_data(num_samples=20):
    # Generar precios relativos y calidades percibidas aleatorias
    precios_relativos = np.random.rand(num_samples)  # Valores entre 0 y 1
    calidades_percibidas = np.random.rand(num_samples)  # Valores entre 0 y 1

    # Inicializar una lista para las etiquetas
    resultados = []

    # Clasificar según los criterios establecidos
    for x1, x2 in zip(precios_relativos, calidades_percibidas):
        if x1 <= 0.6 and x2 >= 0.7:
            resultados.append(1)  # Aceptado
        else:
            resultados.append(0)  # Rechazado

    # Crear un DataFrame para almacenar los datos
    data = pd.DataFrame({
        'Precio Relativo': precios_relativos,
        'Calidad Percibida': calidades_percibidas,
        'Resultado': resultados
    })

    return data

# Generar los datos de prueba
test_data = generate_test_data(20)

# Mostrar las primeras filas del conjunto de datos generado
print("Datos de prueba generados:")
print(test_data)

# Preparar los datos para el entrenamiento del perceptrón
X_train = test_data[['Precio Relativo', 'Calidad Percibida']].values
y_train = test_data['Resultado'].values

# Entrenamiento del perceptrón
perceptron = Perceptron(input_size=2)
perceptron.fit(X_train, y_train, epochs=10, lr=0.1)

# Predicciones en los datos de prueba
predictions = [perceptron.predict(x) for x in X_train]
print("\nPredicciones:", predictions)

# Graficar la frontera de decisión
def plot_decision_boundary(perceptron, X):
    x_min, x_max = X[:, 0].min() - .1, X[:, 0].max() + .1
    y_min, y_max = X[:, 1].min() - .1, X[:, 1].max() + .1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, .01),
                         np.arange(y_min, y_max, .01))
    Z = np.array([perceptron.predict(np.array([xx.ravel()[i], yy.ravel()[i]])) for i in range(len(xx.ravel()))])
    Z = Z.reshape(xx.shape)
    
    plt.contourf(xx, yy, Z, alpha=0.8)
    plt.scatter(X[:, 0], X[:, 1], c=y_train)
    plt.xlabel('Precio Relativo')
    plt.ylabel('Calidad Percibida')
    plt.title('Frontera de Decisión del Perceptrón')
    plt.show()

plot_decision_boundary(perceptron, X_train)


```

# actividad
¿Son los datos linealmente separables?
si, lo son al contener solo valores de 0 y 1

Ajustes para Mejorar la Predicción
Jugar con los valores de learning rate y epocas


Clase Perceptron
Esta clase encapsula la lógica del algoritmo del perceptrón, incluyendo la inicialización de pesos, la función de activación, y los métodos para predecir y ajustar los pesos durante el entrenamiento.

Funcion de Activacion
Se utiliza una funcion escalonada que devuelve 1 si la suma ponderada es mayor o igual a cero, y 0 en caso contrario. Esto permite clasificar los datos en dos clases.

Metodo predict
Este metodo calcula la salida del perceptrón dada una entrada, utilizando los pesos actuales.

Metodo fit
Este metodo entrena al perceptrón ajustando los pesos basándose en los errores cometidos durante las predicciones sobre el conjunto de entrenamiento.

Generacion de Datos
La función generate_test_data crea un conjunto de datos aleatorios con características normalizadas y etiquetas basadas en los criterios establecidos para aceptación o rechazo.

Visualizacion
Se incluye una función para graficar la frontera de decisión generada por el perceptrón, lo que permite observar cómo clasifica los datos en función del precio relativo y la calidad percibida.


