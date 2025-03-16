# ML-PROJECT-HEALTH_INSURANCE
# Step 1:
## Install Cookiecutter-Data-science
!pip install cookiecutter-data-science or ccds
## Define the Project Architecture
Run ccds (cookiecutter-data-science)
You've downloaded C:\Users\user\.cookiecutters\cookiecutter-data-science before. Is it okay to delete and re-download it? [y/n] (y):y
project_name (project_name): health insurance
repo_name (health_insurance): health_insurance
module_name (health_insurance): module_insurance
author_name (Your name (or your organization/company/team)): sundar
description (A short description of the project.): Calculate the Health Insurance Premium
python_version_number (3.10): 3.12
Select dataset_storage
    1 - none
    2 - azure
    3 - s3
    4 - gcs
    Choose from [1/2/3/4] (1): 1
Select environment_manager
    1 - virtualenv        
    2 - conda
    3 - pipenv
    4 - none
    Choose from [1/2/3/4] (1): 2
Select dependency_file
    1 - requirements.txt
    2 - environment.yml
    3 - Pipfile
    Choose from [1/2/3] (1): 1
Select pydata_packages
    1 - none
    2 - basic
    Choose from [1/2] (1): 2
Select open_source_license
    1 - No license file
    2 - MIT
    3 - BSD-3-Clause
    Choose from [1/2/3] (1): 2
Select docs
    1 - mkdocs
    2 - none
    Choose from [1/2] (1): 1
Select include_code_scaffold
    1 - Yes
    2 - No
    Choose from [1/2] (1): 1

# Step 2:
  Create an Python Virtual Environment
  python -m venv .venv
