# pup.py
An API controlled car that looks much more like bomb disposal robot than a puppy


## Overview

I think that the v1.0 will be a car that can be remotely controlled and viewed
from a web browser. To this end, the following tasks are needed:

- [ ] Pi running web server accessible via conor.ooo
- [ ] Stream video on website
- [ ] Basic web UI for controlling the car
- [ ] Power Pi from car


## Technologies

For technologies, I want to be able to easily run and push changes on ARM, so
Docker is a sensible choice. I want to use `uv` for management, and not require
any pyproject or similar until necessary. Docker compose with watchtowerrr will
be sufficient for pulling changes onto the Pi, and FastAPI for the server. Open
questions about the technology to use for the web UI (whatever works easily and
minimally with FastAPI - hopefully React, Vue, or Alpine?), and what to use for
the camera processing (Maybe OpenCV? Too heavy? Something lightweight...)

