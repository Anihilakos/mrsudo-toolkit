import os
import subprocess

from event_capturing.notify_fsm import notify_fsm
from event_capturing.util_funtions import fetch_progression_link
from model_translator.models import CLIEvent, CLIEventType, CrAssetEmulationAssetJoin, PalEmulationSoftwareModel, \
    CRSystemEventCRAssetModelJoin, CREventCRAssetModelJoin, EmulationAssetModel, CRAssetInstance, \
    TrainingScenarioInstance, CRAssetModel

TARGET_USER = 'vagrant'
CYBER_RANGE_PORT = 22
CYBER_RANGE_KEYFILE = '/home/dev/code/sshkeys/deployment_key'

def generic_cli_executor(instance_id, cr_system_event):
    # TODO Support execution FROM any asset, rather than the execution manager
    # TODO Support execution FROM multiple assets?
    # TODO work with public/private keys instead of passwd
    # TODO Support tool execution
    # TODO Support file upload
    # TODO For local execution, support different users than root
    # TODO Replace subprocess with paramiko for ssh connections?
    print("[DEBUG] ---------------------- Calling CLI executor-> " + cr_system_event.__str__())
    cr_event = cr_system_event.crevent
    # ------- Fetch IP and root key of asset/s that need to be send the event
    # Event will be executed FROM this asset/s
    executed_from_cr_asset = CRSystemEventCRAssetModelJoin.objects.values('crassetmodelid').filter(
        crsystemeventid=cr_system_event.crsystemeventid).first()
    # Event will be execute TO this asset/s
    executed_to_cr_asset_list = CREventCRAssetModelJoin.objects.filter(crevent=cr_event).all()
    cr_training_instance = TrainingScenarioInstance.objects.get(trainingscenarioinstanceid=instance_id)

    execution_list = []

    for executed_to_cr_asset in executed_to_cr_asset_list:
        # emulation_asset = EmulationAssetModel.objects.filter(
        # crassetid=executed_to_cr_asset.crassetmodelid.crassetmodelid).first() pal_asset =
        # PalEmulationSoftwareModel.objects.\ filter(
        # emulationassetmodelid=emulation_asset.emulationassetmodelid).first()
        executed_to_cr_asset_model = executed_to_cr_asset.crassetmodel
        executed_from_cr_asset_model = executed_from_cr_asset['crassetmodelid']
        to_cr_asset_instance = CRAssetInstance.objects.filter(trainingscenarioinstance=cr_training_instance,
                                                              instanceofcrasset=executed_to_cr_asset_model).first()
        from_cr_asset_instance = CRAssetInstance.objects.filter(trainingscenarioinstance=cr_training_instance,
                                                                instanceofcrasset=executed_from_cr_asset_model).first()
        print("[DEBUG] Executing from -> ",from_cr_asset_instance.trainingip)
        print("[DEBUG] Executing to -> ",to_cr_asset_instance.trainingip)

        executed_to_asset_dict = {'asset_id': executed_to_cr_asset_model,
                                  'ip': to_cr_asset_instance.trainingip,
                                  'username': 'vagrant',
                                  'password': 'vagrant',
                                  'port': "22",
                                   # 'key_location': '/home/dev/.ssh/id_rsa',
                                  'key_location': '/home/dev/code/sshkeys/deployment_key',
                                  'from': from_cr_asset_instance.trainingip, }
        execution_list.append(executed_to_asset_dict)

    # Fetch generic cli event
    cli_event = CLIEvent.objects.filter(crsystemeventid=cr_system_event.crsystemeventid).first()

    # Check cli event type
    cli_event_type = cli_event.clieventtypename

    if cli_event_type == "raw":
        # Send RAW type clie event FROM Execution Manager TO 1..* Assets
        for execution_item in execution_list:
            #command = 'cd ~ ;' + cli_event.command + str(to_cr_asset_instance.managementip)
            command = 'cd ~ ;' + cli_event.command + str(execution_item['ip']) + " >> /home/vagrant/history.log"
            print("[DEBUG]: Execution of " + command +
                  "\n[DEBUG]: FROM " + execution_item['from'] +
                  "\n[DEBUG]: TO asset with id " + str(execution_item['asset_id']) +
                  "\n[DEBUG]: IP " + execution_item['ip'])
            ssh_output=ssh_command(command, TARGET_USER, execution_item['from'], CYBER_RANGE_KEYFILE)
            try:
                ssh_output = bytes.decode(ssh_output.strip())
                print(ssh_output)
            except AttributeError:
                pass
            notify_fsm(cr_event.creventid, fetch_progression_link(instance_id))

def ssh_command(command, TARGET_USER, TARGET_CONNECTION, CYBER_RANGE_KEYFILE):
    try:
        out = subprocess.check_output(
            ["ssh", "-o", "StrictHostKeyChecking=no", "-i", CYBER_RANGE_KEYFILE,
             "{}@{}".format(TARGET_USER, TARGET_CONNECTION),
             command])
        print('[DEBUG]: SSH command output ')
        print(out)
        print('[DEBUG]: SSH command executed successfully')
        return out
    except subprocess.CalledProcessError as e:
        pass
