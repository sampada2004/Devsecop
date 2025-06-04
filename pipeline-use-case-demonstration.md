# RITBuddy CI/CD Pipeline: Use Case Demonstration

This document demonstrates practical use cases of the CI/CD pipeline for the RITBuddy project, showing how the pipeline handles different scenarios from code commit to production deployment.

## Use Case 1: Feature Development Workflow

### Scenario
A developer is implementing a new feature to add course schedule integration to RITBuddy.

### Step-by-Step Demonstration

#### 1. Local Development
```bash
# Create a feature branch
git checkout -b feature/course-schedule

# Make changes to the codebase
# Add new component in Frontend/src/components/CourseSchedule.jsx
# Add new API endpoint in TempBackend/Routes/ScheduleRoute.js
# Add tests for new components and endpoints

# Run tests locally
cd Frontend
npm test
cd ../TempBackend
npm test
```

#### 2. Push Changes and Create Pull Request
```bash
git add .
git commit -m "feat: add course schedule integration"
git push origin feature/course-schedule
```

The developer creates a pull request on GitHub from `feature/course-schedule` to `develop`.

#### 3. CI Pipeline Execution

**GitHub Actions CI Workflow Triggered:**

```
RITBuddy CI Workflow
✓ Set up Node.js
✓ Install Backend Dependencies
✓ Install Frontend Dependencies
✓ Set up Python
✓ Install Python Dependencies
✓ Lint Backend
✓ Lint Frontend
✓ Run Backend Tests
✓ Run Frontend Tests
✓ Upload Coverage Reports
```

**Test Results:**
- Backend Tests: 45 passed, 0 failed
- Frontend Tests: 32 passed, 0 failed
- Coverage: Backend 82%, Frontend 78%

#### 4. Code Review and Merge
After successful CI pipeline execution and code review, the pull request is approved and merged into the `develop` branch.

#### 5. Develop Branch Deployment
The changes are automatically deployed to the staging environment for further testing.

#### 6. Production Deployment
After validation in staging, a pull request is created from `develop` to `main`.

Once merged to `main`, the CD pipeline is triggered:

```
RITBuddy CD Workflow
✓ Set up Docker Buildx
✓ Login to Docker Hub
✓ Build and Push Docker Image
  - Tags: yourusername/ritbuddy:latest, yourusername/ritbuddy:a1b2c3d
✓ Deploy to Production Server
✓ Verify Deployment
```

#### 7. Monitoring
After deployment, Grafana dashboards show:
- API response times for the new endpoint
- User engagement with the new feature
- System resource utilization

## Use Case 2: Bug Fix Workflow

### Scenario
A critical bug is discovered in the chat functionality where certain queries cause the application to crash.

### Step-by-Step Demonstration

#### 1. Create Bug Fix Branch
```bash
git checkout -b fix/chat-crash
```

#### 2. Reproduce and Fix the Bug
```bash
# Add a test case that reproduces the bug
cd TempBackend/__tests__
# Create test-chat-edge-cases.js

# Fix the bug in QueryRoute.js
cd ../Routes
# Edit QueryRoute.js to handle edge cases properly

# Run tests to verify the fix
cd ..
npm test
```

#### 3. Push Changes and Create Pull Request
```bash
git add .
git commit -m "fix: handle edge cases in chat queries"
git push origin fix/chat-crash
```

Create a pull request directly to `main` since this is a critical bug fix.

#### 4. CI Pipeline Execution

**GitHub Actions CI Workflow:**
```
RITBuddy CI Workflow
✓ Set up Node.js
✓ Install Backend Dependencies
✓ Install Frontend Dependencies
✓ Set up Python
✓ Install Python Dependencies
✓ Lint Backend
✓ Lint Frontend
✓ Run Backend Tests
✓ Run Frontend Tests
✓ Upload Coverage Reports
```

**Test Results:**
- Backend Tests: 46 passed, 0 failed (new test added)
- Frontend Tests: 32 passed, 0 failed
- Coverage: Backend 83%, Frontend 78%

#### 5. Expedited Review and Merge
Due to the critical nature of the bug, the pull request receives expedited review and is merged to `main`.

#### 6. CD Pipeline Execution
```
RITBuddy CD Workflow
✓ Set up Docker Buildx
✓ Login to Docker Hub
✓ Build and Push Docker Image
  - Tags: yourusername/ritbuddy:latest, yourusername/ritbuddy:e5f6g7h
✓ Deploy to Production Server
✓ Verify Deployment
```

#### 7. Monitoring and Verification
- Error rate metrics in Grafana show immediate reduction
- Support team verifies the fix by testing previously problematic queries

## Use Case 3: Performance Optimization

### Scenario
Monitoring shows that the application is experiencing slow response times during peak usage.

### Step-by-Step Demonstration

#### 1. Analyze Performance Metrics
Review Grafana dashboards to identify bottlenecks:
- API response time graphs show slowdown in `/api/ask` endpoint
- CPU and memory utilization spikes during peak hours

#### 2. Create Optimization Branch
```bash
git checkout -b perf/optimize-query-processing
```

#### 3. Implement Optimizations
```bash
# Optimize database queries
# Implement caching for frequently accessed data
# Add performance tests

# Run performance benchmarks
cd TempBackend
npm run benchmark
```

#### 4. Push Changes and Create Pull Request
```bash
git add .
git commit -m "perf: optimize query processing and add caching"
git push origin perf/optimize-query-processing
```

Create a pull request to the `develop` branch.

#### 5. CI Pipeline with Performance Testing
Add a performance testing step to the CI workflow:

```yaml
- name: Run Performance Tests
  working-directory: ./TempBackend
  run: npm run benchmark
```

**CI Results:**
- All tests pass
- Performance tests show 40% improvement in response time
- Coverage remains above thresholds

#### 6. Merge and Deploy to Staging
After approval, changes are merged to `develop` and deployed to staging.

#### 7. Validate Performance in Staging
```bash
# Run load tests against staging
npm run load-test -- --target=https://staging.ritbuddy.com
```

#### 8. Production Deployment
Create a pull request from `develop` to `main`, which triggers the CD pipeline after approval.

#### 9. Monitor Production Performance
Grafana dashboards show:
- 35% reduction in average response time
- 50% reduction in p95 response time
- 25% reduction in CPU utilization

## Use Case 4: Dependency Update

### Scenario
Security scan identifies vulnerable dependencies that need to be updated.

### Step-by-Step Demonstration

#### 1. Create Update Branch
```bash
git checkout -b chore/update-dependencies
```

#### 2. Update Dependencies
```bash
# Update npm packages
cd Frontend
npm update
npm audit fix

cd ../TempBackend
npm update
npm audit fix

# Update Python packages
pip install --upgrade -r requirements.txt
```

#### 3. Run Tests Locally
```bash
cd Frontend
npm test

cd ../TempBackend
npm test
```

#### 4. Push Changes and Create Pull Request
```bash
git add .
git commit -m "chore: update dependencies to fix security vulnerabilities"
git push origin chore/update-dependencies
```

#### 5. CI Pipeline Execution
The CI pipeline runs and identifies a regression in one test due to API changes in an updated package.

#### 6. Fix Regression and Push Again
```bash
# Fix the failing test
git add .
git commit -m "fix: update test to work with new API"
git push origin chore/update-dependencies
```

#### 7. CI Pipeline Success
The CI pipeline runs successfully after the fix.

#### 8. Merge and Deploy
After approval, changes are merged to `develop`, tested in staging, and then deployed to production through the standard pipeline.

## Use Case 5: Rollback Scenario

### Scenario
A deployment causes unexpected issues in production that weren't caught in testing.

### Step-by-Step Demonstration

#### 1. Identify the Issue
Monitoring alerts show increased error rates after a recent deployment.

#### 2. Initiate Rollback
```bash
# Option 1: Revert the commit
git revert abc1234
git push origin main

# Option 2: Use the CD pipeline to deploy the previous version
# Trigger CD workflow with previous image tag
```

#### 3. Automated Rollback Process
The CD pipeline includes rollback capability:

```yaml
- name: Rollback Deployment
  if: failure()
  uses: appleboy/ssh-action@master
  with:
    host: ${{ secrets.PRODUCTION_HOST }}
    username: ${{ secrets.PRODUCTION_USERNAME }}
    key: ${{ secrets.PRODUCTION_SSH_KEY }}
    script: |
      cd /path/to/deployment
      docker-compose stop
      docker pull yourusername/ritbuddy:previous-stable-tag
      docker tag yourusername/ritbuddy:previous-stable-tag yourusername/ritbuddy:latest
      docker-compose up -d
```

#### 4. Verify Rollback
- Monitoring shows error rates returning to normal
- Manual testing confirms the application is functioning correctly

#### 5. Post-Mortem and Fix
```bash
# Create a fix branch from the stable version
git checkout -b fix/production-issue

# Implement and test the fix
# ...

# Push the fix through the normal CI/CD process
```

## Summary of Benefits Demonstrated

1. **Quality Assurance**
   - Automated testing catches bugs before they reach production
   - Code coverage requirements ensure comprehensive test coverage
   - Linting enforces code style and quality standards

2. **Efficiency**
   - Developers focus on code while automation handles testing and deployment
   - Rapid feedback on code quality and test results
   - Streamlined deployment process

3. **Reliability**
   - Consistent build and deployment process
   - Automated rollback capabilities
   - Comprehensive monitoring and alerting

4. **Security**
   - Regular dependency updates
   - Automated security scanning
   - Controlled deployment process

5. **Visibility**
   - Transparent CI/CD process visible to all team members
   - Comprehensive monitoring dashboards
   - Clear audit trail of all changes and deployments
