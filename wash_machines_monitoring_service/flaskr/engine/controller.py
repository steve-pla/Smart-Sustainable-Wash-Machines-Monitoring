from datetime import datetime
from wash_machines_monitoring_service.flaskr.utils.configurator import read_config


def process_wash_topic(topic, topic1, topic2, payload, static_counter_complete_wash_1,
        flag1, static_counter_complete_wash_2, flag2, wash_state1, wash_state2,
                       start_wash_timestamp_state1, end_wash_timestamp_state1,
                       start_wash_timestamp_state2, end_wash_timestamp_state2 ):
    val = float(payload)

    if topic == topic1:
        if 0.16 >= val > 0.01:
            if flag1:
                if static_counter_complete_wash_1 == 12:
                    flag1 = False
                    static_counter_complete_wash_1 = 0
                    end_wash_timestamp_state1 = datetime.now().strftime("%H:%M:%S")
                    wash_state1 = False
                else:
                    static_counter_complete_wash_1 += 1
        elif val >= 0.17:
            if not flag1:
                if static_counter_complete_wash_1 == 5:
                    flag1 = True
                    static_counter_complete_wash = 0
                    start_wash_timestamp_state1 = datetime.now().strftime("%H:%M:%S")
                    wash_state1 = True
                else:
                    static_counter_complete_wash_1 += 1
    if topic == topic2:
        if 0.16 >= val > 0.01:
            if flag2:
                if static_counter_complete_wash_2 == 12:
                    flag2 = False
                    static_counter_complete_wash_2 = 0
                    end_wash_timestamp_state2 = datetime.now().strftime("%H:%M:%S")
                    wash_state2 = False
                else:
                    static_counter_complete_wash_2 += 1
        elif val >= 0.17:
            if not flag2:
                if static_counter_complete_wash_2 == 5:
                    flag2 = True
                    static_counter_complete_wash_2 = 0
                    start_wash_timestamp_state2 = datetime.now().strftime("%H:%M:%S")
                    wash_state2 = True
                else:
                    static_counter_complete_wash_2 += 1
