FROM python:3.13.7-alpine
COPY ./api_iva.py /app/api_iva.py
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "api_iva.py"]
CMD ["api_iva.py"]
EXPOSE 5000