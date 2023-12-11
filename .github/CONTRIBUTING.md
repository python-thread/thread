# **Contributing**

When contributing to this repository, please first discuss the change you wish to make via issue,
email, or any other method with the owners of this repository before making a change.

Please note we have a [code of conduct](CODE_OF_CONDUCT.md); please follow it in all your interactions with the project.

## Build Instructions
This project utilizes [Poetry](https://python-poetry.org/) to manage and install dependencies. You can install Poetry using [pipx](https://pipx.pypa.io/stable/)
which allows Poetry to run in an isolated environment which ensures that Poetry's own dependencies are not accidentally deleted or upgraded. pipx is the easiest
method to install Poetry, but for more advanced installation options refer to Poetry's [documentation](https://python-poetry.org/docs/).

```
pipx install poetry
```

After poetry is installed, in the project's root directory run the following the install the project's dependencies.

```
poetry install
```

That's it! you can now run thread using

```
poetry run python src/thread
```

## Pull Request Process

1. Ensure any install or build dependencies are removed before the end of the layer when doing a
   build.
2. Update the README.md with details of changes to the interface; this includes new environment variables, exposed ports, valid file locations and container parameters.
3. Increase the version numbers in any examples files and the README.md to the new version that this
   Pull Request would represent. The versioning scheme we use is [SemVer](http://semver.org/).
4. You may merge the Pull Request once you have the sign-off of two other developers, or if you
   do not have permission to do that, you may request the second reviewer to merge it for you.


## Issue Report Process

1. Go to the project's issues.
2. Select the template that better fits your issue.
3. Read the instructions carefully and write within the template guidelines.
4. Submit it and wait for support.