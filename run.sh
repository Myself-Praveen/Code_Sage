#!/bin/bash

if [ ! -f ".env" ]; then
    echo "Enter your OpenAI API key:"
    read -r key
    echo "OPENAI_API_KEY=$key" > .env
fi

pip install -r requirements.txt --quiet

echo ""
echo "Enter the path to the project you want to analyze:"
read -r project_path

echo "Enter your question (or press Enter for default analysis):"
read -r question

if [ -z "$question" ]; then
    python main.py "$project_path"
else
    python main.py "$project_path" --ask "$question"
fi
