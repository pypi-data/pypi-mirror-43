import os
import sys
import subprocess
import click
import toml
import colorful

from .fanciness import log, click_verbosity, ColorfulCommand
from . import builtin


def get_config(filename):
    try:
        with open(filename) as f:
            data = toml.load(f)
            if "base" in data:
                data = {**get_config(data["base"]), **data}
        return data
    except FileNotFoundError:
        raise click.BadOptionUsage(
            option_name="--config",
            message=colorful.red(f"Configuration file {filename} not found."),
        )


def make_options(ctx):
    options = {}
    remaining = list(ctx.args)
    while remaining:
        option = remaining.pop(0)
        if not option.startswith("--"):  # only options are allowed
            raise click.BadParameter(option)
        if "=" in option:
            option, value = option.split("=", maxsplit=1)
        else:
            try:
                maybe_value = remaining.pop(0)
                if maybe_value.startswith("--"):
                    remaining.insert(0, maybe_value)  # place back option
                    raise IndexError
                value = maybe_value
            except IndexError:
                # no next value or next value is an option -> we have a flag
                value = True

        options[option[2:]] = value
    return options


def get_job(config, label):
    log.debug("Getting label %s", label)
    if label in config:
        if isinstance(config[label]["command"], list):
            log.debug("Making new pipeline %s", label)
            return Pipeline(config, label)
        else:
            log.debug("Making new config job %s", label)
            return ConfigJob(config, label)
    elif label.startswith("_"):
        log.debug("Making new builtin job %s", label)
        return BuiltinJob(config, label)
    log.critical("No job called %s was found", label)
    sys.exit(3)


class Job:
    def __init__(self, config, label):
        self.label = label
        self.options = {}
        self.settings = config[label] if label in config else {}


class Pipeline(Job):
    def __init__(self, config, label):
        super().__init__(config, label)
        self.jobs = [get_job(config, lab) for lab in self.settings["command"]]

    def run(self):
        for job in self.jobs:
            for opt in self.options:
                if opt.startswith(f"{job.label}."):
                    job.options[opt[len(job.label) + 1 :]] = self.options[opt]
            job.run()


class ConfigJob(Job):
    def __init__(self, config, label):
        super().__init__(config, label)
        self.cmd = self.settings["command"]
        self.options = {
            key: val for key, val in self.settings.get("options", {})
        }
        self.env = os.environ.copy()
        self.env.update(
            {key: val for key, val in self.settings.get("environment", {})}
        )

    def bake_options(self):
        if self.options:
            return " {}".format(
                " ".join(
                    (f"--{key}" if val is True else f"--{key}={val}")
                    for (key, val) in self.options.items()
                )
            )
        else:
            return ""

    def run(self):
        cmd = "{}{}".format(self.cmd, self.bake_options())
        log.info("Running command %s", self.label)
        try:
            subprocess.run(cmd, env=self.env, shell=True, check=True)
            return log.info("Command %s finished", self.label)
        except subprocess.CalledProcessError as e:
            if self.settings.get("fail_ok", False):
                return log.info("Command %s finished", self.label)
            log.error(
                "Command %s returned with non-zero exit code %s",
                self.label,
                e.returncode,
            )
            raise e


class BuiltinJob(Job):
    def __init__(self, config, label):
        super().__init__(config, label)
        self.fn = getattr(builtin, label[1:])
    def run(self):
        self.fn(self.label, self.options, self.settings)


@click.command(
    cls=ColorfulCommand,
    context_settings={"ignore_unknown_options": True, "allow_extra_args": True},
)
@click.option("--config", "-c", type=click.Path(), default="project.toml")
@click_verbosity
@click.argument("label", type=str, required=False)
@click.pass_context
def cli(ctx, config, label):
    log.debug("Loading config")
    config = get_config(config)
    label = label or config.get("default_command")

    if not label:
        log.echo("Available jobs:")
        for key in config:
            if isinstance(config[key], dict):
                log.echo("\t%s", key)
        return
    job = get_job(config, label)

    log.debug("Applying overrides from options")
    job.options.update(make_options(ctx))
    try:
        job.run()
    except ValueError as e:
        log.critical(e.args[0])
        sys.exit(2)
    except subprocess.CalledProcessError:
        log.critical("Exiting due to error in command")
        sys.exit(1)


if __name__ == "__main__":
    cli()  # pylint: disable=no-value-for-parameter
