# Universal Home Assistant

Self-hosted smart home automation platform. Control and automate your lights, climate, devices, and appliances from a single dashboard, with support for thousands of device integrations.

## Getting started

Docker is the recommended way to run it:

```
docker run -d --name universal-home-assistant --restart=unless-stopped \
  -v /path/to/config:/config -p 8123:8123 ghcr.io/yashhasan570/universal-home-assistant:latest
```

The dashboard is then available at http://localhost:8123.

## Contact

Telegram: [@johnconstantine570](https://t.me/johnconstantine570)
