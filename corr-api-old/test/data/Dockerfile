FROM ubuntu:14.04
# Update packages
RUN apt-get update -y
# Install Python Setuptools
# Install pip
RUN easy_install pip
# Add and install Python modules
RUN cd ..
RUN cd /src; pip install -r requirements.txt
RUN cd ..
# Bundle app source
ADD . /src
# Run
CMD ["python","/src/run.py","--host=0.0.0.0","--port=5100"]
