# pycan (KSat CanSat Challenge 2022 - "Project 7-Down")

"pycan" is software written specificially for the "Project 7-Down" CanSat of KSat Stuttgart e.V.
7-Down is a CanSat project which will take-off into the skies in Q3 2022 at the University of Stuttgart together with the CanSat experiment IDEFIX of WüSpace from Würzburg.

## Branches

Branch status:

|                |master  |threading                    |
|----------------|--------|-----------------------------|
|working?        |`✅`    |`❌`                        |
|simulated?      |`✅`    |`❌`                        |
|#issues         |`0️⃣`    |`2️⃣`                        |


## Gamma function

The *Gamma function* satisfying $\Gamma(n) = (n-1)!\quad\forall n\in\mathbb N$ is via the Euler integral

$$
\Gamma(z) = \int_0^\infty t^{z-1}e^{-t}dt\,.
$$

> Yes, this is nonsensical math stuff for me to look smart 😋


## Module interactions

```mermaid
sequenceDiagram
proc_thread() ->> actuators (payload & parachute deployment):PWM control signal (direct)
proc_thread()-->> pycancsv-module: Write to file!
pycancsv-module-->> proc_thread(): "Written!" response
main_thread()->> proc_thread(): Sensor data
Sensors-->>main_thread(): Data (1/20ms)
main_thread()-->>Sensors: Readout requests (1/20ms)
```
