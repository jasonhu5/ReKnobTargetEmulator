# ReKnobTargetEmulator

* ### [Installation](#installation-1)
* ### [Preparation before use](#preparation-before-use-1)
* ### [How to use](#how-to-use)
  * ##### [MAC or Linux](#mac-or-linux-1)
  * ##### [Windows](#windows-1)
* ### [Explaining the programs](#explaining-the-programs)

---

### Installation
* clone or download this repository

---

### Preparation before use
* Make sure the Python library __keyboard__ is installed
  * e.g. by `pip install keyboard`
* Change the Unity program accordingly:
  * Change the IP for connection
    * In ___UDPDataLoader.cs___ file => `LoadUDPData()` => (add following lines before returning the udpData)
  ```
  udpData.receiveIPAddress = "127.0.0.1";
  udpData.sendIPAddress = "127.0.0.1"
  ```
  * Increase UDP socket buffer size if necessary
    * In ___ReHapticKnob.cs___ file => `Connect (UDPData udpData)` function => (change following lines)
    ```
    // from
    // motorValues.SetReceiveBuffer(1);
    // safety.SetReceiveBuffer(1);
    // to
    motorValues.SetReceiveBuffer(1023);
    safety.SetReceiveBuffer(1023);
    ```
  * [Optional] To emulate color pad input with keyboard
    * In ___InputManager.cs___ file => `Update()` function => (replace original color pad input with)
    ```
    if (Input.GetKeyDown(KeyCode.Y)) {
        if (OnYellowDown != null) {
          OnYellowDown();
        }
        if (OnColorDown != null) {
          OnColorDown(0);
        }
    }
    if (Input.GetKeyDown(KeyCode.B)) {
        if (OnBlueDown != null) {
          OnBlueDown();
        }
        if (OnColorDown != null) {
          OnColorDown(1);
        }
    }
    if (Input.GetKeyDown(KeyCode.R)) {
        if (OnRedDown != null) {
          OnRedDown();
        }
        if (OnColorDown != null) {
          OnColorDown(2);
        }
    }
    if (Input.GetKeyDown(KeyCode.G)) {
        if (OnGreenDown != null) {
          OnGreenDown();
        }
        if (OnColorDown != null) {
          OnColorDown(3);
        }
    }
    if (Input.GetKeyDown(KeyCode.W)) {
        if (OnWhiteDown != null) {
          OnWhiteDown();
        }
        if (OnColorDown != null) {
          OnColorDown(4);
        }
    }
    ```
---

### How to use
##### MAC or Linux
```
# bring up a terminal window
python UDP_conns.py

# bring up a terminal window
python UDP_safety.py

# bring up a terminal window
sudo python UDP_motorValues.py

# start the Unity game
# use arrow keys to emulate target machine movements
# or, input 0/1/2 at the UDP_safety.py window to alter safety condition
```
##### Windows
```
# bring up a cmd window
python UDP_conns.py

# bring up a cmd window
python UDP_safety.py

# bring up a *** admin *** cmd window
python UDP_motorValues.py

# start the Unity game
# use arrow keys to emulate target machine movements
# or, input 0/1/2 at the UDP_safety.py window to alter safety condition
```

---

### Explaining the programs
Details of the UDP connection interface, refer to the "Guides - UDP Connection" section of *Lucas Eicher*'s Master Thesis (done at *ReLab, ETH Zurich*). And this repo is emulating functions of the **target** machine.

With regard to the UPD Connection interface:
1. UDP_conns.py
  * This program emulates the following UDP connections
    * connection
    * mode
    * motorData
    * calibration
  * Program output
    * On startup, the program prints (may be in different order)
    ```
    Starting - connection
    Starting - mode
    Starting - motorData
    Starting - calibration
    ```
    * During execution, the program prints messages received or sent, for example:
      * `[connection] R 1`
        * connection interface received 1 from host
      * `[connection] S 0.0`
        * connection sent 1.0 to host
      * `[mode] R 2`
        * mode interface received 2 from host (i.e. set to RUN mode)
      * `[mode] S 2.0`
        * mode sent 2.0 to host
      * `[calibration] R {"value":2,"motor":0}`
        * calibration interface received following command json string from host:
        ```json
        {
            "value":2,
            "motor":0
        }
        ```
      * `[calibration] S 2.0`
        * calibration sent 2.0 to host
      * `[motorData] R {"motor":1,"mode":2,"jsonData":"{\"startPosition\":0.0,\"middlePosition\":1000.0,\"endPosition\":1000.0,\"forceConstant\":0.125,\"isDamper\":true}"}`
        * motorData interface received following command json string from host:
        ```json
         {
             "motor":1,
             "mode":2,
             "jsonData":"{\"startPosition\":0.0,\"middlePosition\":1000.0,\"endPosition\":1000.0,\"forceConstant\":0.125,\"isDamper\":true}"
         }
        ```
2. UDP_safety.py
  * This program emulates this UDP connection
    * safety
  * Program output
    * On startup, the program prints `Starting - safety`
    * During execution, the program prompts for input and prints messages once the input has been sent to host, for example:
      * prompt line: `[safety] <<<`
      * user type: `0` or `1` or `2`, press Enter
      * print confirmation: `[safety] S 2.0`
        * safety interface sent 2.0 to host
3. UDP_motorValues.py
  * This program emulates this UDP connection
    * motorValues
  * Program output
    * On startup, the program prints `Starting - motorValues`
    * During execution, the program constantly prints the motorValues json object that is being sent to host:
    ```json
    {
        "positionLinear": 20.0,
        "positionRotatory": 0.0,
        "velocityLinear": 0.0,
        "velocityRotatory": 0.0
    }
    ```
  * Controls
    * Press __UP__ arrow key: increase _positionLinear_
    * Press __DOWN__ arrow key: decrease _positionLinear_
    * Press __RIGHT__ arrow key: increase _positionRotatory_
    * Press __LEFT__ arrow key: decrease _positionRotatory_
