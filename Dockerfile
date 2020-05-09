from ubuntu

RUN apt-get update && apt-get -y upgrade \
    && apt-get install -y python3-pip

RUN pip3 install redis \
    && pip3 install Django \
    && pip3 install djangorestframework \
    && pip3 install django-cors-headers

# Start server
CMD tail -f /dev/null