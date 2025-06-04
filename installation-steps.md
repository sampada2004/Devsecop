# Installation Steps for RITBuddy CI/CD Tools

## Jest Installation

```
cd c:\College\RITBuddy\RITBuddy
npm install --save-dev jest supertest @babel/preset-env @babel/register babel-jest
cd TempBackend
npm install --save-dev jest supertest
```

## Prometheus Installation (Docker)

```
cd c:\College\RITBuddy\RITBuddy
docker run -d --name prometheus -p 9090:9090 -v ${PWD}/prometheus.yml:/etc/prometheus/prometheus.yml prom/prometheus
```

## Prometheus Installation (Windows)

- Download Prometheus from https://prometheus.io/download/
- Extract to desired location
- Copy your prometheus.yml to the extracted directory
- Run: prometheus.exe --config.file=prometheus.yml

## Grafana Installation (Docker)

```
cd c:\College\RITBuddy\RITBuddy
docker-compose -f docker-compose-monitoring.yml up -d
```

## Grafana Installation (Windows)

- Download Grafana from https://grafana.com/grafana/download
- Extract to desired location
- Run: grafana-server.exe from the bin directory

## Prometheus Configuration

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'ritbuddy'
    static_configs:
      - targets: ['localhost:3000']
```

## Grafana Configuration

- Access Grafana: http://localhost:3000 (admin/admin)
- Add Prometheus data source: http://localhost:9090
- Import dashboards for Node.js monitoring

## Running Tests

```
# Backend tests
cd c:\College\RITBuddy\RITBuddy\TempBackend
npm test

# Frontend tests
cd c:\College\RITBuddy\RITBuddy\Frontend
npm test
```

## CI/CD Integration Commands

```yaml
# Add to GitHub Actions workflow
- name: Run Backend Tests
  working-directory: ./TempBackend
  run: npm test
     
- name: Run Frontend Tests
  working-directory: ./Frontend
  run: npm test
     
- name: Upload Coverage Reports
  uses: actions/upload-artifact@v3
  with:
    name: coverage-reports
    path: |
      ./TempBackend/coverage
      ./Frontend/coverage
```
