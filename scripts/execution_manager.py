from execution_manager.executors.generic_cli_tool_executor import generic_cli_executor
from model_translator.models import CREvent, CRSystemEvent, ThreatEmulationTacticalAbilityEvent, SwaksEmail, \
    CRSystemEventType, CREventType
from test_environments.sprint4_tests.test_event_driven_attack.executors.caldera_executor import caldera_executor
from execution_manager.executors.swaks_executor import swaks_executor




def execution_manager(cr_event_id, instance_id):
    print("Event with id received -> "+str(cr_event_id))
    cr_event = CREvent.objects.get(creventid=cr_event_id)
    print(cr_event.creventtype)
    # 1 for user event
    # 2 for system event
    cr_event_type = CREventType.objects.get(creventtypeid=cr_event.creventtype)
    if cr_event_type.name == 'SystemEvent':
        print('check what type of system event it is')
        cr_system_event = CRSystemEvent.objects.get(crevent=cr_event_id)
        cr_system_event_type_id = cr_system_event.systemeventtype
        print("[DEBUG] system event id ",cr_system_event_type_id)
        cr_system_event_type = CRSystemEventType.objects.get(crsystemeventtypeid=cr_system_event_type_id)
        print(cr_system_event_type.name)
        print("[DEBUG] cr_system_event_type ", cr_system_event_type.name)
        # 1 for tactical ability event - caldera single action event
        if cr_system_event_type.name == 'TacticalEvent':
            te_tactical_ability_event = ThreatEmulationTacticalAbilityEvent.objects.\
                get(crsystemeventid=cr_system_event.crsystemeventid)
            caldera_executor(te_tactical_ability_event, cr_event, cr_system_event)
        # 3 for swaks  email event
        if cr_system_event_type.name == 'SwaksEmail':
            swaks_email_event = SwaksEmail.objects.get(crsystemeventid=cr_system_event.crsystemeventid)
            swaks_executor(swaks_email_event)
        # 4 for CLI event
        if cr_system_event_type.name == 'CliEvent':
            generic_cli_executor(instance_id, cr_system_event)
    else:
        # event is not a system event
        print('FSM send to executor a user event or event not properly defined')

