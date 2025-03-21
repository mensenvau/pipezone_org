FROM ubuntu:latest

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV CODE_VERSION=4.17.1
ENV WORKSPACE=/home/coder/workspace
ENV VENV_PATH=/home/coder/workspace/.venv

# Install dependencies and clean up
RUN apt-get update && apt-get install -y --no-install-recommends \
    sudo curl wget git vim unzip \
    python3 python3-pip python3-venv python-is-python3 \
    build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Java and set JAVA_HOME
RUN apt-get update && apt-get install -y openjdk-11-jdk && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set JAVA_HOME and Spark variables
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH="$JAVA_HOME/bin:$PATH"

# Ensure the environment is sourced in every session
RUN echo 'source /etc/environment' >> ~/.bashrc

# Create a non-root user (coder) with sudo privileges
RUN useradd -m coder && \
    mkdir -p $WORKSPACE && \
    chown -R coder:coder /home/coder && \
    echo "coder ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/coder

WORKDIR $WORKSPACE

# Install Python packages inside a virtual environment
RUN python3 -m venv $VENV_PATH && \
    $VENV_PATH/bin/pip install --upgrade pip && \
    $VENV_PATH/bin/pip install fastapi uvicorn pyodbc boto3 s3fs ipykernel && \
    $VENV_PATH/bin/python -m ipykernel install --user --name=venv --display-name "Python (venv)" && \
    echo "export PATH=$VENV_PATH/bin:\$PATH" >> /home/coder/.bashrc

# Install PySpark
RUN $VENV_PATH/bin/pip install pyspark

# Install code-server
RUN ARCH=$(dpkg --print-architecture) && \
    curl -fsSL https://github.com/coder/code-server/releases/download/v${CODE_VERSION}/code-server_${CODE_VERSION}_${ARCH}.deb -o code-server.deb && \
    dpkg -i code-server.deb && \
    rm -f code-server.deb

# Configure code-server
RUN mkdir -p /home/coder/.config/code-server && \
    echo "bind-addr: 0.0.0.0:9000" > /home/coder/.config/code-server/config.yaml && \
    echo "auth: password" >> /home/coder/.config/code-server/config.yaml && \
    echo "password: mysecurepassword" >> /home/coder/.config/code-server/config.yaml && \
    chown -R coder:coder /home/coder/.config

# Switch to coder user
USER coder

# Install VS Code extensions
RUN code-server --install-extension zhuangtongfa.material-theme && \
    code-server --install-extension pkief.material-icon-theme && \
    code-server --install-extension ms-python.python && \
    code-server --install-extension ms-azuretools.vscode-docker \
    code-server --install-extension ms-toolsai.jupyter && \
    code-server --install-extension ms-toolsai.jupyter-keymap && \
    code-server --install-extension ms-toolsai.jupyter-cell-tags && \
    code-server --install-extension ms-toolsai.jupyter-renderers && \
    code-server --install-extension ms-toolsai.jupyter-slide-show

# Configure VS Code settings
RUN mkdir -p /home/coder/.local/share/code-server/User && \
    echo '{ \
        "workbench.colorTheme": "One Dark Pro",  \
        "workbench.iconTheme": "material-icon-theme",  \
        "files.autoSave": "afterDelay",  \
        "editor.fontSize": 14,  \
        "window.zoomLevel": 1,  \
        "python.defaultInterpreterPath": "/home/coder/venv/bin/python3",  \
        "window.restoreWindows": "preserve",  \
        "workbench.startupEditor": "none",  \
        "code-server.openedPathsList": { "workspaces3": ["/home/coder/workspace"] }  \
    }' > /home/coder/.local/share/code-server/User/settings.json

# Expose the necessary port
EXPOSE 9000

# Start code-server
CMD ["code-server", "--config", "/home/coder/.config/code-server/config.yaml", "--user-data-dir", "/home/coder/.local/share/code-server", "--extensions-dir", "/home/coder/.local/share/code-server/extensions", "/home/coder/workspace"]
