coverage:
	py.test --cov sgbackend --cov-report term-missing tests/

test:
	py.test
