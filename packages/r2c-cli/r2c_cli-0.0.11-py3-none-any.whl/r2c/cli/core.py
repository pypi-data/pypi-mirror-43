#!/usr/bin/env python3
import itertools
import json
import logging
import os
import shutil
import subprocess
import sys
import webbrowser
from pathlib import Path
from typing import Any, Dict, Iterator, Optional, Tuple

import click
import requests
from requests.models import HTTPError, Response
from semantic_version import Version

from r2c.cli import __version__
from r2c.cli.create_template import create_template_analyzer
from r2c.cli.errors import get_cli_error_for_api_error
from r2c.lib.manifest import AnalyzerManifest
from r2c.lib.registry import RegistryData
from r2c.lib.run import (
    build_docker,
    integration_test,
    run_analyzer_on_local_code,
    run_docker_unittest,
)
from r2c.lib.util import SymlinkNeedsElevationError, analyzer_name_from_manifest
from r2c.lib.versioned_analyzer import AnalyzerName, VersionedAnalyzer

logger = logging.getLogger(__name__)
LOCAL_CONFIG_DIR = os.path.join(Path.home(), ".r2c")
CONFIG_FILENAME = "config.json"
CREDS_FILENAME = "credentials.json"
DEFAULT_ORG_KEY = "defaultOrg"
LOCAL_DEV = os.getenv("LOCAL_DEV") == "True"
MAX_RETRIES = 3

DEFAULT_MANIFEST_TRAVERSAL_LIMIT = 50  # number of dirs to climb before giving up


class ManifestNotFoundError(Exception):
    """Couldn't find analyzer manifest on the local filesystem, even after traversal"""

    pass


def log_manifest_not_found_then_die():
    click.echo(
        "❌ Couldn't find an analyzer.json for this analyzer. Check that you're in an analyzer directory, or specify a path to your analyzer.json with --analyzer-directory.",
        err=True,
    )
    sys.exit(1)


def handle_request_with_error_message(r: Response) -> dict:
    """Handles the requests.response object. If the response
    code is anything other than success, CliError will be thrown.
    """
    try:
        r.raise_for_status()
    except HTTPError as e:
        json_response = r.json()
        api_error_code = json_response["error_type"]
        api_error_msg = f"{json_response['message']}. {json_response['next_steps']}"

        raise get_cli_error_for_api_error(api_error_code, api_error_msg)
    return r.json()


def get_version():
    """Get the current r2c-cli version based on __init__"""
    return __version__


def print_version(ctx, param, value):
    """Print the current r2c-cli version based on setuptools runtime"""
    if not value or ctx.resilient_parsing:
        return
    click.echo(f"r2c-cli/{get_version()}")
    ctx.exit()


def fetch_registry_data():
    org = get_default_org()
    url = f"{get_base_url()}/api/v1/analyzers/"
    r = auth_get(url)

    response_json = handle_request_with_error_message(r)
    if response_json["status"] == "success":
        return response_json["analyzers"]
    else:
        raise ValueError("Couldn't parse analyzer registry response")


def get_authentication_url(org):
    """Return URL for getting login authenticatio token"""
    return f"{get_base_url(org)}/settings/token"


def open_browser_login(org):
    url = get_authentication_url(org)
    click.echo(f"trying to open {url} in your browser...", err=True)
    try:
        webbrowser.open(url, new=0, autoraise=True)
    except Exception as e:
        click.echo(
            f"Unable to open a web browser. Please visit {url} and paste the token in here",
            err=True,
        )


def validate_token(org, token):
    try:
        r = auth_get(
            f"{get_base_url(org)}/api/users", token=token
        )  # TODO make this hit a dedicated url /api/check-token once the API endpoint is rolled out completely
        return r.status_code == requests.codes.ok
    except Exception as e:
        # TODO log exception
        return False


def abort_on_build_failure(build_status):
    if build_status != 0:
        logger.error(f"❌ Failed to build analyzer: {build_status}")
        raise click.Abort()


def save_json(obj: Any, filepath: str) -> None:
    """save object to filepath. Throws exceptions"""
    with open(filepath, "w") as fp:
        json.dump(obj, fp, indent=4, sort_keys=True)


def load_creds() -> Dict[str, str]:
    """return creds as a mapping from org to token"""
    cred_file = os.path.join(LOCAL_CONFIG_DIR, CREDS_FILENAME)
    try:
        with open(cred_file) as fp:
            return json.load(fp)
    except Exception as e:
        logger.info(f"unable to read token file from {cred_file}: {e}")
        return {}


def save_creds(creds: Dict[str, str]) -> bool:
    """save creds to disk. Return True if successful. False otherwise"""
    Path(LOCAL_CONFIG_DIR).mkdir(parents=True, exist_ok=True)
    cred_file = os.path.join(LOCAL_CONFIG_DIR, CREDS_FILENAME)
    try:
        save_json(creds, cred_file)
        return True
    except Exception as e:
        logger.info(f"unable to save cred file to {cred_file}: {e}")
        return False


def load_config() -> Dict[str, str]:
    """load config from disk"""
    config_file = os.path.join(LOCAL_CONFIG_DIR, CONFIG_FILENAME)
    try:
        with open(config_file) as fp:
            return json.load(fp)
    except Exception as e:
        logger.info(f"unable to read config from {config_file}: {e}")
        return {}


def save_config(config: Dict[str, str]) -> bool:
    """save config to disk. Return True if successful. False otherwise"""
    Path(LOCAL_CONFIG_DIR).mkdir(parents=True, exist_ok=True)
    config_file = os.path.join(LOCAL_CONFIG_DIR, CONFIG_FILENAME)
    try:
        save_json(config, config_file)
        return True
    except Exception as e:
        logger.info(f"unable to save config file to {config_file}: {e}")
        return False


def save_config_creds(org: str, token: str) -> bool:
    """save org as the new defaultOrg and store the token in the creds store. Return True if successful. False otherwise"""
    old_config = load_config()
    new_config = {**old_config, DEFAULT_ORG_KEY: org}
    saved_successfully = True
    saved_successfully = save_config(new_config) and saved_successfully
    old_creds = load_creds()
    new_creds = {**old_creds, org: token}
    return save_creds(new_creds) and saved_successfully


def delete_creds(org: Optional[str] = None) -> bool:
    """delete creds for a given org. If org is None, delete all creds. Return True if successful. False otherwise"""
    creds = load_creds()
    if org is None:
        # let's delete all creds since org is None
        return save_config({})
    if org in creds:
        del creds[org]
    return save_creds(creds)


def delete_default_org() -> bool:
    """delete the defaultOrg from the config. Return True if successful. False otherwise"""
    config = load_config()
    if DEFAULT_ORG_KEY in config:
        del config[DEFAULT_ORG_KEY]
    return save_config(config)


def get_token_for_org(org: str) -> Optional[str]:
    """Return the token for a given org. None if a token isn't found for that org"""
    creds = load_creds()
    return creds.get(org)


def get_org_from_analyzer_name(analyzer_name: str) -> str:
    """Given a '/' separated name of analyzer, e.g. r2c/typeflow, returns the org name which is 'r2c'
    """
    names = analyzer_name.split("/")
    assert (
        len(names) == 2
    ), f"Make sure you specified org and analyzer_name as `org/analyzer_name` in your analyzer.json"
    return names[0]


def get_default_org() -> Optional[str]:
    """Return the default org as stored in the config. Return None if not set."""
    config = load_config()
    return config.get(DEFAULT_ORG_KEY)


def get_default_token() -> Optional[str]:
    """Return the auth token for the default org as stored in the config. Return None if not found or default org is not set."""
    org = get_default_org()
    if org:
        return get_token_for_org(org)
    else:
        return None


def get_base_url(
    org: Optional[str] = get_default_org(), local_dev: bool = LOCAL_DEV
) -> str:
    """Return the base url for an org or the public instance. Return a localhost url if local_dev is True"""
    if local_dev:
        return "http://localhost:5000"
    elif org:
        return f"https://{org}.massive.ret2.co"
    else:
        logger.info("No org set so going to use 'public' org")
        return f"https://public.massive.ret2.co"


def get_default_headers() -> Dict[str, str]:
    """Headers for all CLI http/s requests"""
    return {"X-R2C-CLI-VERSION": f"{get_version()}", "Accept": "application/json"}


def get_auth_header(token: Optional[str]) -> Dict[str, str]:
    """Return header object with 'Authorization' for a given token"""
    if token:
        return {"Authorization": f"Bearer {token}"}
    else:
        return {}


def auth_get(
    url: str,
    params: Dict[str, str] = {},
    headers: Dict[str, str] = {},
    token: Optional[str] = get_default_token(),
) -> requests.models.Response:
    """Perform a requests.get with Authorization and default headers set"""
    headers = {**get_default_headers(), **headers, **get_auth_header(token)}
    r = requests.get(url, headers=headers, params=params)
    return r


def auth_post(
    url: str,
    json: Any = {},
    params: Dict[str, str] = {},
    headers: Dict[str, str] = {},
    files: Dict[str, str] = {},
    token: Optional[str] = get_default_token(),
) -> requests.models.Response:
    """Perform a requests.post with Authorization and default headers set"""
    headers = {**get_default_headers(), **headers, **get_auth_header(token)}
    r = requests.post(url, headers=headers, params=params, json=json, files={})
    return r


def auth_put(
    url: str,
    json: Any = {},
    params: Dict[str, str] = {},
    headers: Dict[str, str] = {},
    files: Dict[str, str] = {},
    token: Optional[str] = get_default_token(),
) -> requests.models.Response:
    """Perform a requests.put with Authorization and default headers set"""
    headers = {**get_default_headers(), **headers, **get_auth_header(token)}
    r = requests.put(url, headers=headers, params=params, json=json, files={})
    return r


def auth_delete(
    url: str,
    json: Any = {},
    params: Dict[str, str] = {},
    headers: Dict[str, str] = {},
    files: Dict[str, str] = {},
    token: Optional[str] = get_default_token(),
) -> requests.models.Response:
    """Perform a requests.delete with Authorization and default headers set"""
    headers = {**get_default_headers(), **headers, **get_auth_header(token)}
    r = requests.delete(url, headers=headers, params=params, json=json, files={})
    return r


def climb_dir_tree(start_path: str) -> Iterator[str]:
    next_path = start_path
    current_path = None
    while next_path != current_path:
        current_path = next_path
        next_path = os.path.dirname(current_path)
        yield current_path


def find_analyzer_manifest(path: str, parent_limit: int) -> Tuple[str, str]:
    """Finds an analyzer manifest file starting at PATH and ascending up the dir tree.

    Arguments:
        path: where to start looking for analyzer.json
        parent_limit: limit on the number of directories to ascend

    Returns:
        (path to analyzer.json, path containing analyzer.json for Docker build)
    """
    for path in itertools.islice(climb_dir_tree(path), parent_limit):
        manifest_path = os.path.join(path, "analyzer.json")
        if os.path.exists(manifest_path):
            return manifest_path, os.path.dirname(manifest_path)

    raise ManifestNotFoundError()


def upload_analyzer_json(manifest_path):
    logger.info(f"Uploading analyzer.json from {manifest_path}")
    with open(manifest_path) as fp:
        analyzer_json = json.load(fp)
    r = auth_post(f"{get_base_url()}/api/v1/analyzers/", json=analyzer_json)
    data = handle_request_with_error_message(r)
    link = data.get("links", {}).get("artifact_url")
    return link


def get_docker_creds(artifact_link):
    if LOCAL_DEV:
        return {}
    r = auth_get(artifact_link)
    if r.status_code == requests.codes.ok:
        data = r.json()
        return data.get("credentials")
    else:
        return None


def docker_login(creds, debug=False):
    docker_login_cmd = [
        "docker",
        "login",
        "-u",
        creds.get("login"),
        "-p",
        creds.get("password"),
        creds.get("endpoint"),
    ]
    if LOCAL_DEV:
        logger.info(f"Using ecr credentials in .aws during development")
        try:
            erc_login = subprocess.check_output(
                [
                    "aws",
                    "ecr",
                    "get-login",
                    "--no-include-email",
                    "--region",
                    "us-west-2",
                ]
            )
            docker_login_cmd = erc_login.decode("utf-8").strip().split(" ")
        except Exception as e:
            logger.info(f"Docker login failed with {e}")
            return True
    with open(os.devnull, "w") as FNULL:
        if debug:
            return_code = subprocess.call(
                docker_login_cmd, stdout=FNULL, stderr=subprocess.STDOUT
            )
        else:
            return_code = subprocess.call(docker_login_cmd, stdout=FNULL, stderr=FNULL)
    return return_code == 0


def docker_push(image_id):
    docker_push_cmd = ["docker", "push", image_id]
    logger.info(f"Running push with {' '.join(docker_push_cmd)}")
    return_code = subprocess.call(docker_push_cmd)
    return return_code == 0


def get_git_author():
    try:
        git_name = (
            subprocess.check_output(["git", "config", "--get", "user.name"])
            .decode("utf-8")
            .strip()
        )
        git_email = (
            subprocess.check_output(["git", "config", "--get", "user.email"])
            .decode("utf-8")
            .strip()
        )
        return (git_name, git_email)
    except Exception as e:
        logger.info(e)
        return (None, None)


def get_manifest_traversal_limit(ctx):
    return 1 if ctx.obj["NO_TRAVERSE_MANIFEST"] else DEFAULT_MANIFEST_TRAVERSAL_LIMIT


@click.group()
@click.option(
    "--debug",
    is_flag=True,
    help="Show extra output, error messages, and exception stack traces",
    default=False,
)
@click.option(
    "--version",
    is_flag=True,
    help="Show current version of r2c cli.",
    callback=print_version,
    expose_value=False,
    is_eager=True,
)
@click.option(
    "--no-traverse-manifest",
    is_flag=True,
    help="Don't attempt to find an analyzer.json if it doesn't exist in the current or specified directory",
    default=False,
)
@click.pass_context
def cli(ctx, debug, no_traverse_manifest):
    ctx.ensure_object(dict)
    set_debug_flag(ctx, debug)
    ctx.obj["NO_TRAVERSE_MANIFEST"] = no_traverse_manifest
    os.environ["DEBUG"] = str(debug)


def set_debug_flag(ctx, debug):
    if debug:
        logging.basicConfig(level=logging.INFO)
    ctx.obj["DEBUG"] = debug


@cli.command()
@click.option(
    "--org",
    help="org to sign into. Ask R2C if you have questions about this",
    required=False,
)
def login(org=None):
    """
    Log in to the R2C analysis platform.

    Logging in will grant you access to private analyzers published to
    your org. After logging in, you can locally run analyzers that depend
    on these privately published analyzers.
    """

    # ensure org
    if org is None:
        org = get_default_org()
        if org is None:
            org = click.prompt("Please enter your group name")
    if click.confirm(
        "Opening web browser to get login token. Do you want to continue?", default=True
    ):
        open_browser_login(org)
    else:
        url = get_authentication_url(org)
        click.echo(f"Visit {url} and enter the token below")
    # prompt for token
    for attempt in range(MAX_RETRIES):
        token = click.prompt("Please enter the API token")
        # validate token
        valid_token = validate_token(org, token)
        if valid_token:
            # save to ~/.r2c
            save_config_creds(org, token)
            click.echo("✅You are now logged in 🎉", err=True)
            break
        else:
            click.echo(
                "❌ Couldn't log you in with that token. Please try logging in again.",
                err=True,
            )


@cli.command()
@click.option(
    "--org",
    help="The org to sign into. Ask R2C if you have questions about this",
    required=False,
)
def logout(org=None):
    """Log out of the R2C analysis platform.

    Logging out will remove all authentication tokens.
    If --org is specified, you will only log out of that org.
    """
    try:
        delete_creds(org)
        # remove default org
        delete_default_org()
        if org:
            click.echo(f"\n✅ logged out of {org}", err=True)
        else:
            click.echo("\n✅ logged out of all orgs", err=True)
    except Exception as e:
        click.echo(f"❌ Unexpected error. Please contact us", err=True)
        logger.exception(e)
        sys.exit(1)


@cli.command()
@click.option("--analyzer-directory", default=os.getcwd())
@click.argument("env-args-string", nargs=-1, type=click.Path())
@click.pass_context
def unittest(ctx, analyzer_directory, env_args_string):
    """
    Locally unit tests for the current analyzer directory.

    You can define how to run your unit tests in `src/unittest.sh`.

    You may have to login if your analyzer depends on privately
    published analyzers.
    """
    debug = ctx.obj["DEBUG"]
    env_args_dict = parse_remaining(env_args_string)

    try:
        manifest_path, analyzer_directory = find_analyzer_manifest(
            analyzer_directory, parent_limit=get_manifest_traversal_limit(ctx)
        )
    except ManifestNotFoundError:
        log_manifest_not_found_then_die()

    logger.info(f"Found analyzer.json at {manifest_path}")
    analyzer_name = AnalyzerName(analyzer_name_from_manifest(manifest_path))

    with open(manifest_path) as fp:
        version = Version(json.load(fp)["version"])
        # TODO(@ulzii): please handle the case where no version field exists gracefully with an error

    abort_on_build_failure(
        build_docker(
            analyzer_name,
            version,
            os.path.relpath(analyzer_directory, os.getcwd()),
            env_args_dict=env_args_dict,
            verbose=debug,
        )
    )

    image_id = VersionedAnalyzer(analyzer_name, version).image_id

    status = run_docker_unittest(
        analyzer_directory=analyzer_directory,
        analyzer_name=analyzer_name,
        docker_image=image_id,
        verbose=debug,
        env_args_dict=env_args_dict,
    )
    if status == 0:
        logger.info(f"\n✅ unit tests passed")
        sys.exit(0)
    else:
        logger.error(f"\n❌ unit tests failed with status {status}")
        sys.exit(-1)


@cli.command()
@click.option("-d", "--analyzer-directory", default=".")
@click.argument("env-args-string", nargs=-1, type=click.Path())
@click.pass_context
def test(ctx, analyzer_directory, env_args_string):
    """
    Locally run integration tests for the current analyzer.

    You can add integration test files to the `examples/` directory.
    For more information, refer to the integration test section of the README.

    You may have to login if your analyzer depends on privately
    published analyzers.
    """

    debug = ctx.obj["DEBUG"]
    env_args_dict = parse_remaining(env_args_string)
    click.echo(
        f"Running integration tests for analyzer with debug mode {'on' if ctx.obj['DEBUG'] else 'off'}",
        err=True,
    )

    try:
        manifest_path, analyzer_directory = find_analyzer_manifest(
            analyzer_directory, parent_limit=get_manifest_traversal_limit(ctx)
        )
    except ManifestNotFoundError:
        log_manifest_not_found_then_die()

    logger.info(f"Found analyzer.json at {manifest_path}")
    analyzer_name = AnalyzerName(analyzer_name_from_manifest(manifest_path))

    with open(manifest_path) as fp:
        version = json.load(fp)["version"]
        # TODO(@ulzii): please handle the case where no version field exists gracefully with an error

    abort_on_build_failure(
        build_docker(
            analyzer_name,
            Version(version),
            os.path.relpath(analyzer_directory, os.getcwd()),
            env_args_dict=env_args_dict,
            verbose=debug,
        )
    )

    try:
        integration_test(
            analyzer_directory,
            workdir=None,
            env_args_dict=env_args_dict,
            registry_data=RegistryData.from_json(fetch_registry_data()),
        )
    except SymlinkNeedsElevationError as sym:
        click.echo(
            f"❌ Error setting up integration tests. {sym}. Try again as an admin.",
            err=True,
        )
        sys.exit(1)


@cli.command()
@click.option("-d", "--analyzer-directory", default=os.getcwd())
@click.argument("env_args_string", nargs=-1, type=click.Path())
@click.pass_context
def push(ctx, analyzer_directory, env_args_string):
    """
    Push the analyzer in the current directory to the R2C platform.

    You must log in to push analyzers.

    This command will validate your analyzer and privately publish your analyzer
    to your org with the name specified in analyzer.json.

    Your analyzer name must follow {org}/{name}.
    """
    debug = ctx.obj["DEBUG"]
    env_args_dict = parse_remaining(env_args_string)

    try:
        manifest_path, analyzer_directory = find_analyzer_manifest(
            analyzer_directory, parent_limit=get_manifest_traversal_limit(ctx)
        )
    except ManifestNotFoundError:
        log_manifest_not_found_then_die()

    logger.info(f"Found analyzer.json at {manifest_path}")
    analyzer_name = analyzer_name_from_manifest(manifest_path)

    with open(manifest_path, encoding="utf-8") as f:
        analyzer_json = json.load(f)
        version = analyzer_json.get("version")
        analyzer_name = analyzer_json.get("analyzer_name")
        analyzer_org = get_org_from_analyzer_name(analyzer_name)

    # TODO(ulzii): let's decide which source of truth we're using for analyzer_name above and/or check consistency.
    # can't have both dir name and what's in analyzer.json
    analyzer_name = AnalyzerName(analyzer_name)
    click.echo(f"Pushing analyzer in {analyzer_directory}...", err=True)

    default_org = get_default_org()
    if default_org != analyzer_org:
        click.echo(
            f"❌ Attempting to push to organization: `{default_org}`. However, the org specified as the prefix of the analyzer name in `analyzer.json` does not match it. "
            + f"Replace `{analyzer_org}` with `{default_org}` and try again."
            + "Please ask for help from R2C support"
        )
        sys.exit(1)

    # upload analyzer.json
    artifact_link = upload_analyzer_json(manifest_path)
    if artifact_link is None:
        click.echo(
            "❌ there was an error uploading your analyzer. Please ask for help from R2C support",
            err=True,
        )
        sys.exit(1)
    # get docker login creds
    creds = get_docker_creds(artifact_link)
    if creds is None:
        click.echo(
            "❌ there was an error getting Docker credentials. Please ask for help from R2C support",
            err=True,
        )
        sys.exit(1)
    # docker login
    successful_login = docker_login(creds)
    if not successful_login:
        click.echo(
            "❌ there was an error logging into Docker. Please ask for help from R2C support",
            err=True,
        )
        sys.exit(1)
    # docker build and tag
    abort_on_build_failure(
        build_docker(
            analyzer_name,
            Version(version),
            os.path.relpath(analyzer_directory, os.getcwd()),
            env_args_dict=env_args_dict,
            verbose=debug,
        )
    )
    # docker push
    image_id = VersionedAnalyzer(analyzer_name, Version(version)).image_id
    successful_push = docker_push(image_id)
    if not successful_push:
        click.echo(
            "❌ there was an error pushing the Docker image. Please ask for help from R2C support",
            err=True,
        )
        sys.exit(1)
    # mark uploaded with API
    # TODO figure out how to determine org from analyzer.json
    uploaded_url = (
        f"{get_base_url()}/api/v1/analyzers/{analyzer_name}/{version}/uploaded"
    )
    r = auth_put(uploaded_url)
    data = handle_request_with_error_message(r)
    if data.get("status") == "uploaded":
        web_url = data["links"]["web_url"]
        # display status to user and give link to view in web UI
        click.echo(f"✅ Successfully uploaded analyzer! Visit: {web_url}", err=True)
    else:
        click.echo(
            "❌ Error confirming analyzer was successfully uploaded. Please contact us with the following information: failed to confirm analyzer finished uploading.",
            err=True,
        )
        sys.exit(1)


def parse_remaining(pairs):
    """
    Given a string of remaining arguments (after the "--"), that looks like "['x=y', 'a=b'] return a dict of { 'x': 'y' }
    """
    return {pair.split("=")[0]: pair.split("=")[1] for pair in pairs}


@cli.command()
@click.argument("analyzer_input")
@click.option(
    "-d",
    "--analyzer-directory",
    default=os.getcwd(),
    help="The directory where the analyzer is located, defaulting to the current directory.",
)
@click.option("-o", "--output-path", help="OU")
@click.option(
    "-q",
    "--quiet",
    is_flag=True,
    default=False,
    help="Don't print analyzer output to stdout after it completes",
)
@click.option(
    "--analyzer-quiet",
    is_flag=True,
    default=False,
    help="Don't print analyzer logging to stdout or stderr while it runs",
)
@click.option(
    "--no-login",
    is_flag=True,
    default=False,
    help="Do not run `docker login` command during run.",
)
@click.option(
    "--debug",
    is_flag=True,
    help="Show extra output, error messages, and exception stack traces",
    default=False,
)
@click.option(
    "--wait",
    is_flag=True,
    default=False,
    help="Don't start the container, wait for user.",
)
@click.argument("env-args-string", nargs=-1, type=click.Path())
@click.pass_context
def run(
    ctx,
    analyzer_directory,
    analyzer_input,
    output_path,
    quiet,
    analyzer_quiet,
    no_login,
    wait,
    debug,
    env_args_string,
):
    """
    Run the analyzer in the current directory over a code directory.

    You may have to log in if your analyzer depends on privately
    published analyzers.
    """
    if debug == True:  # allow passing --debug to run as well as globally
        set_debug_flag(ctx, True)

    debug_mode = ctx.obj["DEBUG"]
    click.echo(
        f"🏃 Running analyzer...{'with debug mode' if debug_mode else ''}", err=True
    )
    env_args_dict = parse_remaining(env_args_string)

    try:
        manifest_path, analyzer_directory = find_analyzer_manifest(
            analyzer_directory, parent_limit=get_manifest_traversal_limit(ctx)
        )
    except ManifestNotFoundError:
        log_manifest_not_found_then_die()

    logger.info(f"Found analyzer.json at {manifest_path}")
    analyzer_name = AnalyzerName(analyzer_name_from_manifest(manifest_path))

    with open(manifest_path, encoding="utf-8") as f:
        manifest = AnalyzerManifest.from_json_str(f.read())

    dependencies = manifest.dependencies
    logger.info(f"Parsing and resolving dependencies: {dependencies}")

    registry_data = RegistryData.from_json(fetch_registry_data())
    if dependencies:

        for analyzer_dep in dependencies:
            dep_name = analyzer_dep.name
            dep_semver_version = analyzer_dep.wildcard_version
            dep_version = registry_data._resolve(
                AnalyzerName(analyzer_dep.name), dep_semver_version
            )
            if not dep_version:
                click.echo(
                    f"❌ Error resolving dependency {dep_name} at version {dep_semver_version}. Check that you're using the right version of this dependency and try again."
                )
                sys.exit(1)
            logger.info(f"Resolved dependency {dep_name}:{dep_semver_version}")

        if not no_login:
            # we need at least one dep and its version to get credentials when the user isn't logged in
            dep_name = dependencies[0].name
            dep_semver_version = dependencies[0].wildcard_version
            dep_version = registry_data._resolve(
                AnalyzerName(dep_name), dep_semver_version
            )

            artifact_link = (
                f"{get_base_url()}/api/v1/artifacts/{dep_name}/{dep_version}"
            )
            logger.info(f"Getting credential from {artifact_link}")

            # TODO (ulzii) use proper auth credential once its done
            creds = get_docker_creds(artifact_link)
            if creds is None:
                click.echo(
                    "❌ Error getting dependency credentials. Please contact us with the following information: failed to get Docker credentials."
                )
                sys.exit(1)
            # docker login
            successful_login = docker_login(creds)
            if not successful_login:
                click.echo(
                    "❌ Error validating dependency credentials. Please contact us with the following information: failed to log in to Docker."
                )
                sys.exit(1)
    else:
        click.echo(
            "⚠️ No dependencies found; are dependencies intentionally omitted in analyzer.json? Most analyzers are expected to have 1 or more dependencies (e.g. for taking source code as input)."
        )

    abort_on_build_failure(
        build_docker(
            analyzer_name,
            manifest.version,
            os.path.relpath(analyzer_directory, os.getcwd()),
            env_args_dict=env_args_dict,
            verbose=debug_mode,
        )
    )

    try:
        run_analyzer_on_local_code(
            registry_data=registry_data,
            manifest=manifest,
            workdir=None,
            code_dir=analyzer_input.strip(
                '"'
            ),  # idk why this is happening for quoted paths
            output_path=output_path,
            wait=wait,
            show_output_on_stdout=not quiet,
            pass_analyzer_output=not analyzer_quiet,
            no_preserve_workdir=True,
            env_args_dict=env_args_dict,
        )
    except SymlinkNeedsElevationError as sym:
        click.echo(
            f"❌ Error setting up local analysis. {sym}. Try again as an admin.",
            err=True,
        )
        sys.exit(1)


@cli.command()
@click.option("--analyzer-name")
@click.option("--author-name")
@click.option("--author-email")
@click.option("--run-on")
@click.option("--output-type")
@click.pass_context
def init(ctx, analyzer_name, author_name, author_email, run_on, output_type):
    """
    Creates an example analyzer for analyzing JavaScript/TypeScript.

    You may use any language to write your analysis and run it from `src/analyze.sh`.

    Once you create your analyzer, you can navigate to your analyzer directory
    and run 'r2c' commands inside that directory.

    Type `r2c -—help` to see all of the commands available.
    """
    debug = ctx.obj["DEBUG"]
    default_name, default_email = get_git_author()
    if not analyzer_name:
        analyzer_name = click.prompt("Analyzer name", default="example")
    if not author_name:
        author_name = click.prompt("Author name", default=default_name)
    if not author_email:
        author_email = click.prompt("Author email", default=default_email)
    if not run_on:
        run_on = click.prompt(
            "Will your analyzer produce: \n"
            + "- output for a particular `git` repository\n"
            + "- output for a particular git `commit` in a repo\n"
            + "- the same `constant` output regardless of commit or repo?",
            default="commit",
            type=click.Choice(["git", "commit", "constant"]),
        )
    if not output_type:
        output_type = click.prompt(
            "Does your analyzer output \n"
            + "- a single schema-compliant JSON file \n"
            + "- a full filesystem output?",
            default="json",
            type=click.Choice(["json", "filesystem"]),
        )
    create_template_analyzer(
        get_default_org(), analyzer_name, author_name, author_email, run_on, output_type
    )
    click.echo(
        f"✅ done. Your analyzer can be found in the {analyzer_name} directory", err=True
    )
