import re
import click

def validate_IP(ctx, param, value):
    if bool(re.match(r"^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$", value)) is False:
        raise click.BadParameter("Invalid host IP provided.")
    return value