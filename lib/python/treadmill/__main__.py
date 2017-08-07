"""Treadmill module."""

from __future__ import absolute_import

import logging
import logging.config

try:
    from treadmill import dependencies  # pylint: disable=E0611,W0611
except ImportError:
    pass

import click

# pylint complains about imports from treadmill not grouped, but import
# dependencies need to come first.
#
# pylint: disable=C0412
from treadmill import cli


# pylint complains "No value passed for parameter 'ldap' in function call".
# This is ok, as these parameters come from click decorators.
#
# pylint: disable=E1120
#
# TODO: add options to configure logging.
@click.group(cls=cli.make_commands('treadmill.cli'))
@click.option('--dns-domain', required=False,
              envvar='TREADMILL_DNS_DOMAIN',
              callback=cli.handle_context_opt,
              is_eager=True,
              expose_value=False)
@click.option('--dns-server', required=False, envvar='TREADMILL_DNS_SERVER',
              callback=cli.handle_context_opt,
              is_eager=True,
              expose_value=False)
@click.option('--ldap', required=False, envvar='TREADMILL_LDAP',
              type=cli.LIST,
              callback=cli.handle_context_opt,
              is_eager=True,
              expose_value=False)
@click.option('--ldap-user', required=False, envvar='TREADMILL_LDAP_USER',
              callback=cli.handle_context_opt,
              is_eager=True,
              expose_value=False)
@click.option('--ldap-pwd', required=False, envvar='TREADMILL_LDAP_PWD',
              callback=cli.handle_context_opt,
              is_eager=True,
              expose_value=False)
@click.option('--ldap-suffix', required=False,
              envvar='TREADMILL_LDAP_SUFFIX',
              callback=cli.handle_context_opt,
              is_eager=True,
              expose_value=False)
@click.option('--profile', required=False,
              envvar='TREADMILL_PROFILE',
              callback=cli.handle_context_opt,
              is_eager=True,
              expose_value=False)
@click.option('--outfmt', type=click.Choice(['json', 'yaml']))
@click.option('--debug/--no-debug',
              help='Sets logging level to debug',
              is_flag=True, default=False)
@click.pass_context
def run(ctx, outfmt, debug):
    """Treadmill CLI."""
    ctx.obj = {}
    ctx.obj['logging.debug'] = False

    if outfmt:
        cli.OUTPUT_FORMAT = outfmt

    # Default logging to cli.conf, at CRITICAL, unless --debug
    cli.init_logger('cli.conf')
    if debug:
        ctx.obj['logging.debug'] = True
        logging.getLogger('treadmill').setLevel(logging.DEBUG)
        logging.getLogger().setLevel(logging.DEBUG)


run()