FROM python
WORKDIR /app
RUN pip install --trusted-host pypi.python.org -r requirements.txt
EXPOSE 8080
ENV web-app
CMD ["python", "app.py"]