FROM python:3.9-slim

# Variables d'environnement pour Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Installation des dépendances système
RUN apt-get update && apt-get install -y \
    git \
    wget \
    curl \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Installation des packages Python
RUN pip3 install --upgrade pip
RUN pip3 install \
    tensorflow \
    matplotlib \
    pandas \
    scikit-learn \
    seaborn \
    opencv-python \
    jupyter \
    jupyterlab \
    tensorboard \
    protobuf

# Vérification que TensorFlow est bien installé
RUN python -c "import tensorflow as tf; print(tf.__version__)"

# Création et définition du répertoire de travail
WORKDIR /workspace

# Exposer les ports pour Jupyter et TensorBoard
EXPOSE 8888 6006

# Commande par défaut
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token=''", "--NotebookApp.password=''"]