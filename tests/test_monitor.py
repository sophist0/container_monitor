from pytest_mock import mocker

from monitor import act_on_status, MonitorConfig, run_monitor, State

def test_MonitorConfig():

    config = MonitorConfig("config.txt")
    config.load_config()

    assert isinstance(config.from_email, str)
    assert len(config.from_email) > 0

    assert isinstance(config.from_email_pwd, str)
    assert len(config.from_email_pwd) > 0

    assert isinstance(config.recipient, str)
    assert len(config.recipient) > 0

    assert isinstance(config.smtp_server, str)
    assert len(config.smtp_server) > 0

    assert isinstance(config.wait_time, int)

    assert isinstance(config.containers, list)
    assert len(config.containers) > 0


def test_act_on_status(mocker):

    state = State()
    config = MonitorConfig("config.txt")
    config.load_config()

    mocker.patch('monitor.send_email', return_value=None)
    email_body = "This is a test."

    state.one_service_down = False
    state.last_status = "ok"
    state = act_on_status(config, state, email_body)
    assert state.last_status == "ok"

    state.one_service_down = False
    state.last_status = "alarm"
    state = act_on_status(config, state, email_body)
    assert state.last_status == "ok"

    state.one_service_down = True
    state.last_status = "alarm"
    state = act_on_status(config, state, email_body)
    assert state.last_status == "alarm"

    state.one_service_down = True
    state.last_status = "ok"
    state = act_on_status(config, state, email_body)
    assert state.last_status == "alarm"


def test_run_monitor(mocker):

    config = MonitorConfig("config.txt")
    config.load_config()
    config.wait_time = 0

    mocker.patch('monitor.get_container_status', return_value="healthy")
    mocker.patch('monitor.send_email', return_value=False)
    state = run_monitor(config, test=True)
    assert state.one_service_down == False
    assert state.email_sent == False

    mocker.patch('monitor.get_container_status', return_value="unhealthy")
    mocker.patch('monitor.send_email', return_value=True)
    state = run_monitor(config, test=True)
    assert state.one_service_down == True
    assert state.email_sent == True

