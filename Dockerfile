FROM tensorflow/tensorflow:latest

# Assurer la compatibilité avec architecture ARM
ENV TF_ENABLE_ONEDNN_OPTS=0

# Installation des dépendances supplémentaires
RUN apt-get update && apt-get install -y \
    git \
    wget \
    curl \
    python3-pip \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Installation des packages Python couramment utilisés
RUN pip3 install --upgrade pip
RUN pip3 install \
    matplotlib \
    tensorflow \
    pandas \
    scikit-learn \
    seaborn \
    opencv-python \
    jupyter \
    jupyterlab \
    tensorboard \
    protobuf

# Création et définition du répertoire de travail
WORKDIR /workspace

# Exposer les ports pour Jupyter et TensorBoard
EXPOSE 8888 6006

# Commande par défaut (remplacée par celle dans docker-compose)
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]