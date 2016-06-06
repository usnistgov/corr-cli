import click
from click.testing import CliRunner
from corr.main import cli

# class TestCli:
 
#     def test_config(self):
#         runner = CliRunner()
#         config_result = runner.invoke(cli, ['--config', '--host', '0.0.0.0', 'port', 5100, '--key', '8c27a5c8d508cc10da0ea91412d726479996bdcad05421a6fc815d974ae22ade'])
#         print config_result.exit_code
#         print 'Config response: {0}'.format(config_result.output)

#         result_conx = runner.invoke(cli, ['--conx'])
#         print result_conx.exit_code
#         print 'Conx response: {0}'.format(result_conx.output)

#     def test_align(self):
#         runner = CliRunner()
#         result_align = runner.invoke(cli, ['--align'])
#         print result_align.exit_code
#         print 'Align response: {0}'.format(result_align.output)
 
