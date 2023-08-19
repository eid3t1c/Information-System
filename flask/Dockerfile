FROM ubuntu:20.04 
RUN apt-get update
RUN apt-get install -y python3 python3-pip 
RUN pip3 install --upgrade pip 
RUN pip3 install flask pymongo click
RUN mkdir /app
RUN mkdir -p /app/data
COPY end.py /app/end.py  
COPY Default_Admin.json /app/Default_Admin.json
CMD mongoimport --host mongodb --db DigitalNotes --collection Admins --file /app/Default_Admin.json --batchSize 1
EXPOSE 5000
WORKDIR /app
ENTRYPOINT [ "python3","-u", "end.py" ]
