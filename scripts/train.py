import tensorflow as tf
from tensorflow import keras
import numpy as np
import datetime
import os

# Vérifier et créer le dossier des logs
log_dir = "/app/logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
os.makedirs(log_dir, exist_ok=True)

# Génération de données aléatoires
X_train = np.random.rand(100, 10)
y_train = np.random.randint(0, 2, size=(100,))

# Définition d'un modèle simple
model = keras.Sequential([
    keras.layers.Dense(16, activation='relu', input_shape=(10,)),
    keras.layers.Dense(8, activation='relu'),
    keras.layers.Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Initialiser le callback TensorBoard
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)

# Entraîner le modèle
model.fit(X_train, y_train, epochs=5, batch_size=10, callbacks=[tensorboard_callback])

print(f"Training terminé, logs enregistrés dans {log_dir}")
