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
    python -m pip install pymongo[srv]

CMD python3 fundamentus.py

# docker build -t my_image .
# docker run -it my_image /bin/bash
# docker run -e MONGO_URI=$MONGO_URI -t my_image