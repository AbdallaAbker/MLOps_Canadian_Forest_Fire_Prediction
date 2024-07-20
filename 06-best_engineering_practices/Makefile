MAGENTA=`tput setaf 5`
RESET=`tput sgr0`

setup-environment:
	@echo "Setup world"
	@conda env create -f environment.yaml
	@echo "${MAGENTA}Remember to activate your environment with these instructions ^${RESET}"

format:
	@echo "Running autopep8 and isort to fix any formatting issues in the code"
	@autopep8 --in-place --recursive .
	@isort .
