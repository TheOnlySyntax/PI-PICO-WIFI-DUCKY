# PicoWDucky
Setup for Raspberry Pi Pico W to make a Wifi Duck.

# This project is only working for Raspberry Pi Pico W!

# What is Wifi Ducky?
USB Rubber Ducky where you can run payloads from iternet

# Key Features
- Minimal Setup.
- Simple and clean webpage for type mnemonics.
- Run Button - Run typed mnemonics.
- Schedule - Schedule run.
- Store on Pico - Store payloads on Pico
- Upload Button - Upload .txt files which contain mnemonics to run.
- Save Button - Save typed mnemonics on the system.
- Clear Button - Clears the text area.

# OS Support
- Windows 10
- Android

# Installation and Setup of Circuit Python
1. Download Latest Circuit Python `.uf2` file for Raspberry P i Pico W - [here](https://circuitpython.org/board/raspberry_pi_pico_w/)
   - Latest version is **9.1.0**.
2. Connect Raspberry Pi Pico W with a USB cable.
3. Press and hold the `BOOTSEL` button and connect to the PC/Laptop.
   - When it connects, then Raspberry Pi Pico W show as a removable storage device named `RPI-RP2`.
   - When `RPI-RP2` is showing, then release the `BOOTSEL` button.
4. Copy the `.uf2` file in the `RPI-RP2`.
   - When it is copied, then it disconnects automatically and reconnect as `CIRCUITPY`.
   - Means circuit python is successfully flashed in the Raspberry Pi Pico W.
5. Done! Now, Raspberry Pi Pico W is ready to use as a Wifi Duck.

# CIRCUITPY Directory Structure
- **CIRCUITPY/**
  - **lib/**
      - `adafruit_hid`
      - `adafruit_httpserver`
  - `code.py`
  - `index.html`

# Mnemonic Table
| Mnemonics | Description | Example  |
|-----------|-------------|----------|
| DELAY      | It add time in the code.<br>Time is in milliseconds.<br>1000 ms = 1 second. | WAIT 1000 |
| STRING      | It add text want to type in the code. | TYPE Hello World! |
| LOOP      | It runs commands for a certain number of times.<br> Synatx is `LOOP number-of-times commands` | LOOP 3<br>TYPE Hello World!<br>EXIT<br><br>LOOP 4<br>TAB<br>EXIT<br><br>LOOP 1<br>CTRL S<br>EXIT<br><br>LOOP 1<br>CTRL SHIFT N<br>EXIT<br> |
| INF       | It run commans infinitely.<br>Syntax is `INF commands` | INF<br>TYPE Hello World!<br>EXIT<br><br>INF<br>TAB<br>EXIT<br> |
| REM       | (#)
| STRING_DELAY| 
| HOLD       |
| RELASE     |
| END_LOOP   |
| DEFINE     |
| VAR        |
| REPEAT     |
| IF         |
| ELSE       |
| END_IF     |
| CALL       |

# Supported Mnemonics
## Alphabet Keys
`A` `B` `C` `D` `E` `F` `G` `H` `I` `J` `K` `L` `M` `N` `O`
`P` `Q` `R` `S` `T` `U` `V` `W` `X` `Y` `Z`
## Function Keys
`F1` `F2` `F3` `F4` `F5` `F6` `F7` `F8` `F9` `F10` `F11` `F12`
## Navigation Keys
`LEFT` `UP` `RIGHT` `DOWN` `TAB` `HOME` `END` `PGUP` `PGDN`
## Lock Keys
`CAPS` `NUM` `SCROLL`
## System and GUI Keys
`GUI` `ESC` `PRTSCR` `PAUSE`
## Editing Keys
`INSERT` `DEL` `BKSP` `ENTER`
## Modifier Keys
`CTRL` `SHIFT` `ALT`
## ASCII Characters
`` ` `` `!` `@` `#` `$` `%` `^` `&` `*` `(` `)` `-` `=` `[` `]` `\` `;` 
`'` `,` `.` `/` `SPACE` `~` `_` `+` `{` `}` `|` `:` `"` `<` `>` `?` `0`
`1` `2` `3` `4` `5` `6` `7` `8` `9`

# Install and Run
1. Download or Clone the Repository.
2. Open the folder.
3. Copy all files in the `CIRCUITPY`.
   - It ask for replacement of `code.py` file, then replace it.
   - It will overwrite in the `code.py` file.
   - After 2-3 minutes, an Access Point is created named `PicoWQuack` whose password is `picowquack`.
6. Connect to that access point.
7. When connected successfully, open your browser and type the following IP - `192.168.4.1`.
8. Hit enter.
   - A webpage opens 
9. Type your script and click on `Run` button.
    - The script executes!

> [!TIP]
>  Start your code with `DELAY` so that board get time to initiate.<br>
>  While using `LOOP` use only one command.


# Examples
## Open notepad and type Hello World!

```
DELAY 1000
GUI R
DELAY 1000
STRING notepad
DELAY 1000
ENTER
DELAY 1000
STRING Hello World!
```
