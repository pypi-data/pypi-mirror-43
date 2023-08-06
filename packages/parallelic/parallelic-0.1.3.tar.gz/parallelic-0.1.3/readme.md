# Parallelic
Parallelic is a hyperparallel multi-node task execution engine with shared data and wokspace capabilities.

## Note of warning
Parallelic is not a containerization/sandboxing engine. It does not constitute a full task isolation, and provides no guarantee of such. That may change in the future, and feel free to contribute your code towards that goal, but in the mean time, keep this in consideration when giving access to a Parallelic system to third parties.

## Installation
### From git
  1. Clone the git repo locally.
  2. Download python3(.7) and corresponding pip
  3. Install [Poetry](https://poetry.eustace.io)
  4. Run `poetry install` to create a virtualenv and install dependencies  
  At this point, you can use parallelic through   
  `poetry run parallelic`
  5. Run `poetry build` to build a wheel
  6. Run `pip install dist/parallelic-[version]-py3-none-any.whl`  
  Now you can use parallelic without poetry:  
  `python -m parallelic`
### From pip
  1. Run `pip install parallelic`

## Usage
### Running a task
To run an already defined task, you upload the task package (a zipped up task root directory) via the Parallelic WebUI, or Parallelic CLI client, to the Parallelic manager instance.   
You may need to provide access credentials before being allowed to upload the task package, as per your Parallelic system configuration.  
From there, the Parallelic manager instance will take care of everything else.

### Defining a task
The task root contains a `task.toml` file, that contains metadata required for the manager to set up and prepare resources for the compute nodes in order to run the particullar task.  
If the task requires no additional files, the task definition can be only the `task.toml` file.

The directory tree doesn't follow a particullar convention, and can be different from task to task. The task definition file should contain a section where the entrypoint and working directory are defined. Both the entrypoint and the working directory have to be relative to the task root.

## Credits
Package maintained by Trickster Animations