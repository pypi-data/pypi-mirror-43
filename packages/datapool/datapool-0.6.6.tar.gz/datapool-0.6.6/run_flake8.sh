if python -c "import flake8"; then
    python -m flake8 --max-line-length 88 datapool tests/
else
    echo run 'pip install flake8' first
fi
