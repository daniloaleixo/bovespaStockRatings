FROM python


COPY fundamentus.py /data/fundamentus.py
COPY waitingbar.py /data/waitingbar.py
WORKDIR /data

# RUN pip install -r requirements.txt
RUN pip install --upgrade lxml && \
    pip install --upgrade python_jwt && \
    pip install --upgrade gcloud && \
    pip install --upgrade sseclient && \
    pip install --upgrade Crypto && \
    pip install --upgrade pycryptodome==3.4.3 && \
    pip install --upgrade requests_toolbelt && \
    pip install --upgrade pymongo && \
    pip install sendgrid && \
    python -m pip install pymongo[srv]

CMD python3 fundamentus.py