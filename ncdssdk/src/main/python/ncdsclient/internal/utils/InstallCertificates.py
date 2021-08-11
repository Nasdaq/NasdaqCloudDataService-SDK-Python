import os.path
import requests
from os import path


class InstallCertificates:
    """
    Gets a one-time-url from kafka_cert_url and downloads the kafka stream certificate from that url.

    Attributes:
       cert_dir (str):  The name of the directory where the certificate should be installed
    """

    def __init__(self, cert_dir):
        self.cert_dir = cert_dir
        self.cert_path = os.path.join(cert_dir, "ca.crt")
        self.kafka_cert_url = "https://tgbstk5716.execute-api.us-east-1.amazonaws.com/v1/get-certificate"

    def install(self):
        return self.__install_cert()

    def __install_cert(self):
        one_time_url = self.__get_one_time_url()

        response = requests.get(one_time_url)

        if not path.exists(self.cert_dir):
            raise Exception(f"Path was not found: {self.cert_dir}")

        with open(self.cert_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=128):
                f.write(chunk)

        return os.path.abspath(self.cert_path)

    def __get_one_time_url(self):
        response = requests.get(
            self.kafka_cert_url,
            headers={'Prama': 'no-cache', 'Cache-Control': 'no-cache'}
        )

        if response.status_code != 200:
            raise Exception("Internal Server Error")

        json_response = response.json()
        one_time_url = json_response['one_time_url']

        return one_time_url
