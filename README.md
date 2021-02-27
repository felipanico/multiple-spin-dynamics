# Single Spin Dynamics
Simple magnetization for a single spin

# Environment (needs virtualenv)

Run in terminal: `source .venv/bin/activate`

# Install requirements

```
python -m pip install numpy
python -m pip install math
python -m pip install matplotlib
```

# Fix plot graph in wsl2

- Install xLaunch

- Disable "Native opengl"

- Enable "Disable access control"

- Run in terminal: `export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):0`

# Running program

Run in terminal `python magnetization.py`
