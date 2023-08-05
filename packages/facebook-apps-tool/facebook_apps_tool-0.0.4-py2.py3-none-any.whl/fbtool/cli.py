import json
import os

import click
from facebook_sdk.exceptions import FacebookResponseException
from facebook_sdk.facebook import Facebook
from facebook_sdk.request import FacebookRequest
import yaml


config_path = "~/.config/fbtool/config.yaml"
current_app_path = "~/.config/fbtool/current_app"


class CreateFacebookTestUser(FacebookRequest):
    def __init__(
        self, app_id, access_token, installed=False, permissions=None, name=None
    ):
        params = {"installed": installed}
        if name:
            params["name"] = name
        if permissions:
            params["permissions"] = permissions

        super(CreateFacebookTestUser, self).__init__(
            access_token=access_token,
            method="POST",
            endpoint="{app_id}/accounts/test-users".format(app_id=app_id),
            params=params,
        )


class AppConfig(object):
    data = {}

    def __init__(self, debug, out_format, app_id, app_secret):
        """

        """
        self.debug = debug
        self.out_format = out_format
        self.app_id = app_id
        self.app_secret = app_secret

    def load_config(self):

        if self.app_id and self.app_secret:
            current_app = {"app_id": self.app_id, "app_secret": self.app_secret}
        else:
            current_app = self.load_config_file()

        self.current_app = current_app

        self.facebook = Facebook(
            app_id=self.current_app.get("app_id"),
            app_secret=self.current_app.get("app_secret"),
            default_graph_version="v2.12",
        )

    def load_config_file(self):

        config = self.get_config_file()

        current_app = self.get_current_app_from_file()

        if current_app not in config.get("apps", {}):
            raise click.ClickException(
                """
                Invalid app selected. Please select one of {}
                fbtool config use_app [app]
                """.format(
                    list(config.get("apps", {}).keys())
                )
            )
        return config["apps"][current_app]

    def get_config_file(self):
        user_config_path = os.path.expanduser(config_path)
        if not os.path.isfile(user_config_path):
            raise click.ClickException(
                """
                No config file
                """
            )

        with open(user_config_path, "r") as f:
            config = yaml.load(f.read())

        return config

    def get_current_app_from_file(self):
        user_current_app_path = os.path.expanduser(current_app_path)

        if not os.path.isfile(user_current_app_path):
            raise click.ClickException(
                """
                No current app selected. Please select one of {}
                fbtool config use_app [app]
                """.format(
                    list(config.get("apps", {}).keys())
                )
            )

        with open(user_current_app_path, "r") as f:
            current_app = f.read()

        return current_app


@click.group()
@click.option("--debug/--no-debug", default=False)
@click.option(
    "--out_format",
    default="raw",
    show_default=True,
    type=click.Choice(["raw", "json"]),
    help="Output format.",
)
@click.option("--app_id", type=str, help="The Facebook Application Id.")
@click.option("--app_secret", type=str, help="The Facebook Application Secret.")
@click.pass_context
def cli(ctx, debug, out_format, app_id, app_secret):
    ctx.obj = AppConfig(debug, out_format, app_id, app_secret)


@cli.group()
@click.pass_context
def config(ctx):
    pass


@cli.group()
@click.pass_context
def test_users(ctx):
    ctx.obj.load_config()


@test_users.command(help="You can create new test users")
@click.option(
    "--quantity",
    "--qty",
    type=int,
    default=1,
    show_default=True,
    help="The quantity of tests users to create. (max 50)",
)
@click.option(
    "--installed",
    default=False,
    is_flag=True,
    help="Automatically installs the app for the test user once it is created or associated.",
)
@click.option(
    "--name",
    "-n",
    type=str,
    help="The name for the test user. When left blank, a random name will be automatically generated.",
)
@click.option(
    "--permissions",
    "-perm",
    type=str,
    help="List of permissions that are automatically granted for the app when it is created or associated.",
)
@click.pass_context
def create(ctx, permissions, name, installed, quantity):
    if quantity > 50:
        raise click.BadParameter("quantity should be lower than 50")

    batch = [
        CreateFacebookTestUser(
            app_id=ctx.obj.facebook.app.app_id,
            access_token=ctx.obj.facebook.app.access_token(),
            installed=installed,
            name=name,
            permissions=permissions,
        ) for _ in range(quantity)
    ]

    try:
        responses = ctx.obj.facebook.send_batch_request(
            requests=batch, access_token=ctx.obj.facebook.app.access_token()
        )
    except FacebookResponseException as e:
        raise click.ClickException(e.message)

    for fb_response in responses.responses:
        click.echo(json.dumps(fb_response['response'].json_body, indent=4, sort_keys=True))


@config.command()
@click.argument("app_name")
@click.pass_context
def use_app(ctx, app_name):
    config = ctx.obj.get_config_file()

    if app_name not in config.get("apps", {}).keys():
        raise click.ClickException(
            """
            Invalid app selected. Please select one of {}
            fbtool config use_app [app]
            """.format(
                list(config.get("apps", {}).keys())
            )
        )

    user_current_app_path = os.path.expanduser(current_app_path)
    with open(user_current_app_path, "w") as f:
        f.write(app_name)

if __name__ == "__main__":
    cli(obj={})
