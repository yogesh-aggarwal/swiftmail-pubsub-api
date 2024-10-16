PRODUCTION_BRANCH=production

server:
	clear
	@poetry run server

seed_db:
	clear
	@poetry run seed_db

experiment:
	clear
	@poetry run experiment

setup:
	clear
	@poetry install

clean:
	@find . -type d -name "__pycache__" -exec rm -r {} +

deploy:
	@git push origin main
	@git update-ref -d refs/heads/$(PRODUCTION_BRANCH)
	@git checkout -b $(PRODUCTION_BRANCH)
	@git push origin $(PRODUCTION_BRANCH) -f
	@git checkout main
