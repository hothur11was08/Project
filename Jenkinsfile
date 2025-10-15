pipeline {
    agent any
    
    options {
        timeout(time: 30, unit: 'MINUTES')
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
                sh 'echo "Checked out code from GitHub"'
            }
        }
        
        stage('Validate Files') {
            steps {
                sh '''
                    echo "Checking if required files exist..."
                    ls -la
                    [ -f "test.py" ] || exit 1
                    [ -f "app.py" ] || exit 1
                    [ -f "requirements.txt" ] || exit 1
                    [ -f "Dockerfile" ] || exit 1
                    echo "All required files present!"
                '''
            }
        }
        
        stage('Test Python Code') {
            steps {
                sh '''
                    echo "Testing Python syntax..."
                    python -c "from test import process_data; print('test.py imports successfully')"
                    python -c "from app import app; print('app.py imports successfully')"
                    echo "Running basic function test..."
                    python -c "
from test import process_data
result = process_data('test')
print(f'Function test result: {result}')
assert 'result' in result
assert result['status'] == 'success'
"
                    echo "Python tests passed!"
                '''
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    // Use commit hash as version tag
                    def commitHash = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
                    def imageName = "python-test-api:${commitHash}"
                    
                    echo "Building Docker image: ${imageName}"
                    docker.build(imageName)
                    
                    // Store image name for later stages
                    env.DOCKER_IMAGE = imageName
                }
            }
        }
        
        stage('Test Docker Image') {
            steps {
                script {
                    sh """
                    echo "Testing Docker image: ${env.DOCKER_IMAGE}"
                    docker run -d --name test-container -p 5000:5000 ${env.DOCKER_IMAGE} &
                    sleep 10
                    
                    echo "Testing health endpoint..."
                    curl -f http://localhost:5000/health || exit 1
                    
                    echo "Testing home endpoint..."
                    curl -f http://localhost:5000/ || exit 1
                    
                    echo "Stopping test container..."
                    docker stop test-container
                    docker rm test-container
                    """
                }
            }
        }
        
        stage('Success') {
            steps {
                echo "Pipeline completed successfully!"
                echo "Docker image built: ${env.DOCKER_IMAGE}"
                echo "API endpoints available:"
                echo "  GET  /health"
                echo "  GET  /"
                echo "  POST /process"
            }
        }
    }
    
    post {
        always {
            sh 'docker stop test-container || true'
            sh 'docker rm test-container || true'
            cleanWs()
        }
        failure {
            echo "Pipeline failed! Check the logs above."
        }
    }
}
