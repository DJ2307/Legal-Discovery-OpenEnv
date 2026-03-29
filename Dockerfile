# 1. Use a lightweight Python image
FROM python:3.10-slim

# 2. Set the folder where our code lives
WORKDIR /app

# 3. Install the required tools (Now including FastAPI for the Meta Ping)
RUN pip install --no-cache-dir pydantic openai openenv-core fastapi uvicorn

# 4. Copy your files into the container
COPY env.py .
COPY inference.py .
COPY openenv.yaml .

# 5. Tell the container to run your evaluation script
CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]
