#!/bin/bash

echo "🔧 Actualizando pip..."
pip install --upgrade pip

echo "🔧 Instalando PyTorch y dependencias relacionadas..."
pip install torch==2.0.1+cpu torchvision==0.15.2+cpu torchaudio==2.0.1+cpu -f https://download.pytorch.org/whl/cpu

echo "🔧 Instalando dependencias generales..."
pip install gdown opencv-python-headless Pillow numpy streamlit fpdf

echo "🔧 Instalando Detectron2 desde GitHub..."
pip install --no-cache-dir git+https://github.com/facebookresearch/detectron2.git@v0.6

