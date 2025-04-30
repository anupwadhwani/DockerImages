#!/bin/sh

# Start Ollama server in background
ollama serve &
OLLAMA_PID=$!

# Wait for server to be up
echo "Waiting for Ollama server to become available..."
until curl -s http://localhost:11434/ > /dev/null; do
  echo "Ollama not up yet... waiting 3 seconds"
  sleep 3
done

echo "Ollama server is up! Starting to pull models..."

ollama run mistral

echo "✅ Done pulling all models."

# Bring ollama serve back to foreground
wait $OLLAMA_PID
