import json
import subprocess
import time
import logging
import smtplib
from email.message import EmailMessage


logger = logging.getLogger(__name__)
logging.basicConfig(format='[%(levelname)s %(asctime)s] %(message)s', filename='monitor.log', encoding='utf-8', level=logging.INFO)

class State:
    def __init__(self):
        self.last_status = "ok"
        self.one_service_down = False
        self.email_sent = False

class MonitorConfig:
    def __init__(self, config_path):
        self.from_email = ""
        self.from_email_pwd = ""
        self.email_subject = ""
        self.recipient = ""
        self.smtp_server = ""
        self.wait_time = ""
        self.containers = []
        self.config_path = config_path

    # TODO: Fix some of these should be environment variables
    def load_config(self):
        with open(self.config_path, "r") as infile:
            for line in infile:
                sine = line.split(":")
                key = sine[0].strip()
                val = sine[1].strip()
                if key == "from_email":
                    self.from_email = val
                elif key == "from_email_pwd":
                    self.from_email_pwd = val
                elif key == "email_subject":
                    self.email_subject = val
                elif key == "recipient":
                    self.recipient = val
                elif key == "smtp_server":
                    self.smtp_server = val
                elif key == "wait_time":
                    self.wait_time = int(val)
                elif key == "containers":
                    sval = val.split(",")
                    for el in sval:
                        self.containers.append(el)

def send_email(config, body):
    em = EmailMessage()
    em.set_content(body)
    em['To'] = config.recipient
    em['From'] = config.from_email
    em['Subject'] = config.email_subject
    EMAIL_SENT = False
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(config.from_email, config.from_email_pwd)
        server.send_message(em)
        server.close()
        logger.info("Sent alarm email")
        EMAIL_SENT = True
    except:
        logger.info("Failed to send alarm email", exc_info=True)
    return EMAIL_SENT

def act_on_status(config, state, email_body):
    if state.one_service_down and (state.last_status == "ok"):
        state.last_status = "alarm"
        state.email_sent = send_email(config, email_body)
    elif not state.one_service_down:
        state.last_status = "ok"
        state.email_sent = False
    return state

def get_container_status(container):
    FRONTEND_CMD = "docker inspect --format='{{json .State.Health}}' " + container
    output = subprocess.check_output(FRONTEND_CMD, shell=True, text=True)
    output = json.loads(output)
    return output["Status"]

def run_monitor(config, test=False):
    state = State()
    while True:
        time.sleep(config.wait_time)
        state.one_service_down = False
        email_body = ""
        for container in config.containers:
            container_status = get_container_status(container)
            log_str = container + ": " + container_status
            logger.info(log_str)
            print(log_str)

            if container_status != "healthy":
                state.one_service_down = True
                if len(email_body) > 0:
                    email_body += ", "
                email_body += log_str

        state = act_on_status(config, state, email_body)
        if test:
            break
    return state

#####################################################################
if __name__ == "__main__":
    config = MonitorConfig("config.txt")
    config.load_config()
    run_monitor(config)
