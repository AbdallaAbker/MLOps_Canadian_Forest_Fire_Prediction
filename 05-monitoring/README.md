## Section 5: Welcome to the Monitoring (Model & Data Drift) :smiley:

![alt text](<../artifacts/images/eveidently.png>)

- Navigate your terminal into directory into Dir: cd ./model_monitoring
- Activate the virtual enviroment in one terminal and run: docker-compose up -build
- Make sure the 3 services are up and running:
    grafana: localhost:3000
    Adminer DB: localhost:8080
    Postgress db: running in the backend
- Make sure to stay in the correct directory Dir: cd ./05-model_monitoring and Run: python metrics_calculation.py
- After the script starts running, it sends data into the Postgress DB, verify the data has been stored in Posgres DB and evidently metrics are visualized in Grafana dashboard
