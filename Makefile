up:
	@echo "Building images and starting containers in detached mode..."
	docker-compose up --build -d

down:
	@echo "Stopping and removing containers..."
	docker-compose down

restart:
	@echo "Restarting services..."
	docker-compose restart

logs:
	@echo "Following logs..."
	docker-compose logs -f