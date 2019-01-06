FROM python:3.5

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install numpy
RUN pip install sympy
RUN pip install pandas
RUN pip install matplotlib
RUN pip install scikit-learn
RUN pip install tensorflow
RUN pip install pymongo
RUN pip install git+https://github.com/oanda/oandapy.git
RUN pip install workdays
RUN pip install schedule