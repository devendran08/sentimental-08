FROM python:3.9.1
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 80
RUN mkdir ~/.streamlit
WORKDIR /app
ENTRYPOINT ["streamlit", "run"]
CMD ["census_app.py"]