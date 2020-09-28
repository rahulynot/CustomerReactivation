.PHONY:test
test:  ## Run unit and integration tests
	py.test test

.PHONY:build-image
build-image:  ## Build docker image for the flask app
	docker image build -t cust-react-voucher .


.PHONY:run-app
run-app:  ## Run Flask App
	docker run -p 5000:5000 cust-react-voucher:latest