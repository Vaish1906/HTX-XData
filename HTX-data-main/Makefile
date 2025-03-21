local-api:
	uvicorn asr.asr_api:app --reload --port 8001 --host "0.0.0.0" --log-level "debug"
.PHONY: local-api

install:
	pip install -r requirements.txt
.PHONY: install

freeze:
	pip freeze > requirements.txt
.PHONY: freeze

transcribe:
	python -m cv-data.cv-decode
.PHONY: transcribe

index:
	python -m elastic-backend.cv-index
.PHONY: index

deploy-api:
	docker compose -f docker-compose.api.yml run asr_api
.PHONY: deploy-api

deploy-search:
	docker compose -f elastic-backend/docker-compose.yml --env-file elastic-backend/.env up
.PHONY: deploy-search

