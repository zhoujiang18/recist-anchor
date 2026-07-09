FROM mrigroupopbg/mri-python3:latest

ENV PYTHONUNBUFFERED=1 \
    CUDA_VISIBLE_DEVICES="" \
    OMP_NUM_THREADS=6 \
    MKL_NUM_THREADS=6 \
    OPENBLAS_NUM_THREADS=6

WORKDIR /workspace/app

COPY requirements.txt /workspace/app/requirements.txt
RUN python -m pip install --upgrade pip setuptools wheel && \
    python -m pip install --no-cache-dir -r /workspace/app/requirements.txt

COPY src/ /workspace/app/src/
COPY predict.py /workspace/app/predict.py
COPY predict.sh /workspace/app/predict.sh
COPY weights.pth /workspace/weights.pth

RUN mkdir -p /workspace/inputs /workspace/outputs && chmod +x /workspace/app/predict.sh

CMD ["sleep", "infinity"]
