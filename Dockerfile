FROM python


COPY . /data
WORKDIR /data

# RUN pip install -r requirements.txt
RUN pip install --upgrade lxml && \
    pip install --upgrade firebase && \
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
# docker run -v $(pwd):/data -it my_image /bin/bash
# docker run -e MONGO_URI=<mongo_uri> -v $(pwd):/data -t my_image