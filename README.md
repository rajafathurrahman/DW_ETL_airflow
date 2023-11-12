# DW_ETL_airflow

Ini adalah script untuk perkuliahan Datawarehouse dimana menggunakan **Airflow** sebagai ETL tools

untuk menginstall Airflow di lokal maupun di server, hal yang pertama harus di lakukan adalah menginstall docker, kemudian harus menguasai setidaknya basic dari airflow seperti membuat Dags dan lainya.

[docker installations guide](https://docs.docker.com/engine/install/)
[airflow basic](https://airflow.apache.org/docs/apache-airflow/stable/index.html)


**langkah 1** : pastikan docker kalian sudah berjalan di local atau di server [check docker](https://docs.docker.com/config/daemon/troubleshoot/#:~:text=The%20operating%2Dsystem%20independent%20way,service%20status%20using%20Windows%20utilities.)

**langkah 2** : salin atau donwload script "docker-compose.yaml", "requirements.txt" dan "Dockerfile" yang di **Github**

**langkah 3** : kemudian jalankan `docker compose up -d` dan tunggu hingga process selesai

**langkah 4** : buka browser `http://localhost:8080` dan akan di arahkan ke halaman login *Airflow* selanjutnya masukan 
username = `airflow`
password = `airflow`
