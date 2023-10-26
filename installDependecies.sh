#!/bin/bash

# Verifica se o pip está instalado
if ! command -v pip &> /dev/null; then
    echo "O comando 'pip' não foi encontrado. Certifique-se de que o Python e o pip estão instalados no seu sistema."
    exit 1
fi

# Instala as dependências usando o pip
pip install numpy matplotlib pandas seaborn

# Import math é uma biblioteca padrão do Python, não é necessário instalar

# Verifica a instalação de 'os' e 'importlib'
python -c "import os, importlib"
if [ $? -eq 0 ]; then
    echo "Os pacotes 'os' e 'importlib' estão disponíveis no Python padrão."
else
    echo "Não foi possível verificar a disponibilidade de 'os' e 'importlib'. Certifique-se de que o Python está instalado corretamente."
fi

# Exibe uma mensagem de conclusão
echo "Dependências instaladas com sucesso."

