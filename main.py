"""
Copyright 2021 crazygmr101

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import sys

import lib.program
import asyncio
import getopt

options = getopt.getopt(
    sys.argv[1:],
    "",
    [
        "location=",
        "domain=",
        "padding=",
        "help",
        "output="
    ]
)

opts = {}
for option in options[0]:
    opts[option[0]] = option[1]

if "--help" in opts:
    print("""
--help                View this help text
--location=<x>,<z>    Set the location that the map's center region contains
                      - Defaults to 0,0
--padding=<n>         Set the amount of 512 block regions the center region is padded by
                      - Defaults to 3
--output=<path>       Set the output image path
                      - Defaults to map.png
--domain=<url>        The root domain for your BlueMap                      
    """)
    exit(0)

if "--domain" not in opts:
    print("Domain must be specified - see python3 main.py --help")
    exit(1)
domain = opts["--domain"].strip("/")
if not domain.startswith("http"):
    domain = f"https://{domain}"

if "--location" not in opts:
    x, z = 0, 0
else:
    if opts["--location"].count(",") != 1:
        print("Location must be formatted as --location=1,2")
        exit(1)
    x, z = tuple(opts["--location"].split(","))
    try:
        x = int(x)
        z = int(z)
    except ValueError:
        print("Location must be formatted as --location=1,2")
        exit(1)

if "--padding" not in opts:
    padding = 3
else:
    try:
        padding = int(opts["--padding"])
    except ValueError:
        print("Padding must be an integer, i.e., --padding=3")
        exit(1)

output = opts.get("--output", "output.png")

print(f"Running render of {domain}, roughly centered on {x},{z}, with a padding of {padding} region files. "
      f"The output will be saved in {output} in the current directory")

asyncio.run(lib.program.main(domain, location=(x, z), padding_amount=padding, output=output))