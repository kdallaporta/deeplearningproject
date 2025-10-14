# Set python image version to 3.11 slim
FROM python:3.11-slim
WORKDIR /app
ENV PIP_DISABLE_PIP_VERSION_CHECK=1 HF_HOME=/root/.cache/huggingface
COPY requirements.txt .

# Install requirements
RUN pip install --no-cache-dir -r requirements.txt
RUN python - <<'PY'

# Run bertweet one time to put it inside the image
from transformers import pipeline
pipeline("sentiment-analysis", model="finiteautomata/bertweet-base-sentiment-analysis")
PY

# Add a default version of files to image
COPY . .
CMD ["python", "runtime/main.py"]