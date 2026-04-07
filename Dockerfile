FROM public.ecr.aws/docker/library/python:3.11-slim


WORKDIR /app

# 1. Install libraries directly to avoid 'pip install .' metadata errors
RUN pip install --no-cache-dir \
    openenv-core \
    fastapi \
    uvicorn \
    pydantic \
    openai

# 2. Copy EVERYTHING (including the server folder)
COPY . .

# 3. Expose the port
EXPOSE 7860

# 4. Start the server directly
CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]
