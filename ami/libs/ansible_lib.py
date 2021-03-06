from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase
from ansible.executor.playbook_executor import PlaybookExecutor
from ami.libs import utils
import ansible.constants as C
import os
import json


class ResultCallback(CallbackBase):
    def v2_runner_on_ok(self, result, **kwargs):
        host = result._host
        print(json.dumps({host.name: result._result}, indent=4))


def play_book(playbook, passwords={}, inventory=None, extra_var={}):
    source = inventory
    if not inventory:
        source = '/etc/ansible/hosts'
    loader = DataLoader()
    inventory_data = InventoryManager(loader=loader, sources=[source])
    variable_manager = VariableManager(loader=loader, inventory=inventory_data)
    variable_manager.extra_vars = extra_var
    results_callback = ResultCallback()
    Options = namedtuple('Options',
                    ['connection',
                    'remote_user',
                    'ask_sudo_pass',
                    'verbosity',
                    'ack_pass',
                    'module_path',
                    'forks',
                    'become',
                    'become_method',
                    'become_user',
                    'check',
                    'listhosts',
                    'listtasks',
                    'listtags',
                    'syntax',
                    'sudo_user',
                    'sudo',
                    'diff'])
    options = Options(connection='smart',
                    remote_user=None,
                    ack_pass=None,
                    sudo_user=None,
                    forks=5,
                    sudo=True,
                    ask_sudo_pass=False,
                    verbosity=5,
                    module_path=None,
                    become=None,
                    become_method=None,
                    become_user=None,
                    check=False,
                    diff=False,
                    listhosts=None,
                    listtasks=None,
                    listtags=None,
                    syntax=None)

    play = Play().load(playbook, variable_manager=variable_manager, loader=loader)
    tqm = None

    try:
        tqm = TaskQueueManager(
                inventory=inventory_data,
                variable_manager=variable_manager,
                loader=loader,
                options=options,
                passwords=passwords,
                stdout_callback=results_callback,
            )
        tqm.run(play)
    except Exception as e:
        print(e)
    finally:
        if tqm is not None:
            tqm.cleanup()

def playbook_file(playbook, passwords={}, inventory=None, extra_var={}):
    source = inventory
    if not inventory:
        source = '/etc/ansible/hosts'
    loader = DataLoader()
    try:
        inventory_data = InventoryManager(loader=loader, sources=[source])
    except Exception as e:
        utils.log_err(e)
    try:
        variable_manager = VariableManager(loader=loader,
            inventory=inventory_data)
    except Exception as e:
        utils.log_err(e)
    variable_manager.extra_vars = extra_var
    results_callback = ResultCallback()
    Options = namedtuple('Options',
                    ['connection',
                    'remote_user',
                    'ask_sudo_pass',
                    'verbosity',
                    'ack_pass',
                    'module_path',
                    'forks',
                    'become',
                    'become_method',
                    'become_user',
                    'check',
                    'listhosts',
                    'listtasks',
                    'listtags',
                    'syntax',
                    'sudo_user',
                    'sudo',
                    'diff'])
    try:
        options = Options(connection='smart',
                    remote_user=None,
                    ack_pass=None,
                    sudo_user=None,
                    forks=5,
                    sudo=True,
                    ask_sudo_pass=False,
                    verbosity=5,
                    module_path=None,
                    become=None,
                    become_method=None,
                    become_user=None,
                    check=False,
                    diff=False,
                    listhosts=None,
                    listtasks=None,
                    listtags=None,
                    syntax=None)
    except Exception as e:
        utils.log_err(e)
    
    try:
        playbook = PlaybookExecutor(
            playbooks=[playbook],
            inventory=inventory_data,
            variable_manager=variable_manager,
            loader=loader,
            options=options,
            passwords=passwords)
    except Exception as e:
        utils.log_err(e)
    else:
        playbook.run()

