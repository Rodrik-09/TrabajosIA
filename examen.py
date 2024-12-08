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
