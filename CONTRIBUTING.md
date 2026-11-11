# Contributing

Python 3.11+ and its standard library are sufficient for the current offline tooling.

```text
python -m unittest discover -s tests -v
```

Keep a clear boundary between owner-reported facts, observations from another model or unit, offline tests and hardware-verified behavior. Record firmware and board identity with each hardware claim, while removing private identifiers from public evidence.

Do not add raw firmware, credentials, packet captures, serial numbers, network addresses or account data. Check both ordinary and ignored files before sharing. Keep required software notices when reusing third-party code; this repository currently contains no copied appliance-protocol implementation.

Hardware changes need a defined test target and a recovery plan. Proposed door-lock overrides, disabled heater protections, unbounded actuator commands and arbitrary raw-resource write interfaces are outside this project's scope.
