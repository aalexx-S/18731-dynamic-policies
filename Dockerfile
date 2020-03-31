from ubuntu

RUN apt-get update && apt-get -y upgrade \
    && apt-get install -y python3-pip

RUN pip3 install redis

# Start server
CMD tail -f /dev/null