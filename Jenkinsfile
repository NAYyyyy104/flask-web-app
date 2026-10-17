pipeline {
    agent any

    environment {
        // 本机 Python 路径（macOS，用 which python3 查到）
        PYTHON_PATH = '/Library/Frameworks/Python.framework/Versions/3.13/bin/python3'
        // 虚拟环境放在 Jenkins 工作区内，不污染系统 Python
        VENV = "${WORKSPACE}/.venv"
    }

    stages {
        stage('Verify Python Path') {
            steps {
                sh '''
                    echo "使用的 Python 路径: $PYTHON_PATH"
                    "$PYTHON_PATH" --version
                '''
            }
        }

        stage('Checkout') {
            steps {
                // Pipeline script from SCM 会自动拉取代码，这里打印确认
                sh 'git log --oneline -3 && ls -la'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    "$PYTHON_PATH" -m venv "$VENV"
                    "$VENV/bin/pip" install --upgrade pip
                    "$VENV/bin/pip" install -r requirements.txt
                    "$VENV/bin/pip" install pytest==8.4.1 flake8==7.1.1
                '''
            }
        }

        stage('Lint') {
            steps {
                sh '"$VENV/bin/flake8" src/ tests/'
            }
        }

        stage('Test') {
            steps {
                sh '"$VENV/bin/pytest" tests/ -v --junitxml=test-results.xml'
            }
            post {
                always {
                    // 在 Jenkins 页面展示测试结果
                    junit 'test-results.xml'
                }
            }
        }

        stage('Build') {
            steps {
                // 简单打包：把源码打成 tar.gz 作为构建产物
                sh '''
                    mkdir -p dist
                    tar -czf dist/flask-web-app.tar.gz src requirements.txt
                    ls -lh dist
                '''
                archiveArtifacts artifacts: 'dist/*.tar.gz', fingerprint: true
            }
        }

        stage('Deploy') {
            steps {
                // 本地冒烟部署：后台启动应用，访问首页验证后关闭
                // 5000 端口在 macOS 上被 AirPlay 占用，这里用 5001
                sh '''
                    "$VENV/bin/python" -c "from src.app import app; app.run(host='127.0.0.1', port=5001)" &
                    APP_PID=$!
                    sleep 3
                    curl -fs http://127.0.0.1:5001/
                    echo
                    kill $APP_PID
                    echo "Deploy 验证通过"
                '''
            }
        }
    }

    post {
        success {
            echo 'CI/CD pipeline completed successfully!'
        }
        failure {
            echo 'CI/CD pipeline failed!'
        }
    }
}
