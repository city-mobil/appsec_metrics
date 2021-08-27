FROM python:3.9.5-slim
#suppress warining https://stackoverflow.com/questions/67244301/warning-messages-when-i-update-pip-or-install-packages
RUN pip3 install PyGithub pytz requests pymongo defectdojo_api|| true
CMD mkdir -p /appsec_metrics/logs/
COPY ./ /appsec_metrics/
WORKDIR /appsec_metrics/