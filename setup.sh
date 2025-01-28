#!/bin/bash

echo "🔧 Actualizando pip..."
pip install --upgrade pip

echo "🔧 Instalando PyTorch y dependencias relacionadas..."
pip install --no-cache-dir torch==2.0.1+cpu torchvision==0.15.2+cpu torchaudio==2.0.1+cpu -f https://download.pytorch.org/whl/cpu

echo "🔧 Instalando dependencias generales..."
pip install --no-cache-dir gdown opencv-python==4.8.0.76 Pillow numpy streamlit fpdf

echo "🔧 Instalando Detectron2 desde GitHub (versión compatible con PyTorch 2.0.1)..."
pip install --no-cache-dir git+https://github.com/facebookresearch/detectron2.git@v0.6
