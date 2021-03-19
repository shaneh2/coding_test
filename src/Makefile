make_report: ../data/full_data_csv.csv ../data/full_data_feather.feather
	pweave report.pmd
	open report.html

../data/full_data_csv.csv:
	curl http://prod.publicdata.landregistry.gov.uk.s3-website-eu-west-1.amazonaws.com/pp-complete.csv -L -o ../data/full_data_csv.csv

../data/full_data_feather.feather:
	python3 0prepare_data.py

install_required_pip_packages:
	pip3 install -r requirements.txt
	@echo "If pip is not installed, try make install_pip"

install_pip:
	sudo -H python3 -m ensurepip

code_quality_metrics:
	@echo "Codeclimate is available from: https://github.com/codeclimate/codeclimate"
	codeclimate analyze
