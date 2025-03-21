# Run tracker

Ideas of things to implement, from least to most crazy:
* Start from me, a user, going for a run and uploading data
* Uses GarminDB to get running data, maybe have this running in a Lambda every day
* Store new run results in an S3 bucket
* Extract only the intervals and report on those in a nice table too
* Use GPT-4 to predict 5k, 10k, and HM times
* Use GPT-4 to suggest my next workout
* Have different coach personas (old fashioned Pete who's all about slow running, modern Steve who loves strength and conditioning, and crazy Jack who insists on an even number of kilometers per day and as a weekly total)
* Use Terraform to deploy the infrastructure to do the above, with a CI/CD pipeline



# Architecture diagram

Maybe this container/lambda process could be run each day

![architecture](images/architecture.png)


# Set up

See GarminDB readme [here](https://github.com/tcgoetz/GarminDB).

* Different options for OpenAI API key - requires env variables set in `.env` file.


## Engineering bits

* Package and dependency management with `poetry`
* Automation using `Makefile` and a precommit

Testing:
* Unit tests with `pytest`, set `pythonpath="src"` under `[tool.pytest.ini_options]` in `pyproject.toml`
* BDD testing using `pytest-bdd`
