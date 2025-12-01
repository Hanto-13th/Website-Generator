#the entrypoint to launch the main func manually and launch server (8888 port)

python3 src/main.py
cd docs && python3 -m http.server 8888