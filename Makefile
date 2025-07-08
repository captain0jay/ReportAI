.PHONY: all run-api run-processor run-all stop

# Install project dependencies
install:
	pip install -r requirements.txt

# Run the FastAPI server using uvicorn
run-api:
	uvicorn main:app --reload

# Run the processor server
run-processor:
	python processor.py

# Run both servers in parallel
run-all:
	@echo "Starting API server and Processor..."
	@tmux new-session -d -s myproject 'make run-api'
	@tmux split-window -h -t myproject 'make run-processor'
	@tmux select-layout -t myproject tiled
	@tmux attach -t myproject

# Optionally, stop all tmux sessions related to this project
stop:
	@tmux kill-session -t myproject || echo "No session to kill"
