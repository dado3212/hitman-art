<h1 align="center">
  <img src="/output/166.png?raw=true" alt=""/>
  <p align="center">Hitman Art</p>
</h1>

<table>
  <tr>
    <td><img src="/output/187.png?raw=true" alt="" width="175"/></td>
    <td><img src="/output/300.png?raw=true" alt="" width="175"/></td>
    <td><img src="/output/231.png?raw=true" alt="" width="175"/></td>
    <td><img src="/output/185.png?raw=true" alt="" width="175"/></td>
    <td><img src="/output/37.png?raw=true" alt="" width="175"/></td>
  </tr>
   <tr>
    <td><img src="/output/128.png?raw=true" alt="" width="175"/></td>
    <td><img src="/output/114.png?raw=true" alt="" width="175"/></td>
    <td><img src="/output/163.png?raw=true" alt="" width="175"/></td>
    <td><img src="/output/211.png?raw=true" alt="" width="175"/></td>
    <td><img src="/output/340.png?raw=true" alt="" width="175"/></td>
  </tr>
</table>


Throughout Hitman there are multiple pieces of art that hang on the wall. I wanted high-res versions
of some of them, so I wrote this code to extract them.

If you just want to see the art, the raw files from the matching files for `(paintings|wallart|graffiti|street_art|mural|drawings).*diffuse` are in the uploads folder (a previous version lived at https://imgur.com/a/dWKFRll).

## Running

Clone the repo. Run `python3 setup.py` which will download rpkg and run some one-off code.

Open `main.py` and change the directory folder to wherever your Hitman 3 installation is.
You can change the pattern you want to search for (`pattern = re.compile("(paintings|wallart|graffiti|street_art|mural|drawings).*diffuse")`).

Then just run `python3 main.py` and it will automatically find the relevant textures (diffuse is the color part),
extract them from the .RPKG files, and convert them into PNG.

## Testing

You can run some simple tests with `python3 tests.py`. For speedup checking, profile with `python3 -m cProfile -s time main.py`.

## Thanks

This relies heavily on PRKG-Tool (https://notex.app/rpkg/), both directly
(this directly runs the CLI) and indirectly in the code that I ported to Python.
A HUGE thanks to the author of the original repo, available at 
https://github.com/glacier-modding/RPKG-Tool.

## What's Next?

I think the guess_name function might be able to resolve some of the missing
hash names. As an example of this, I think I can probably find the names for the
textures that compose hotel_room_thai_a_decal in chunk24.rpkg.

---

# Licenses

RPKG
Copyright (c) 2020+, REDACTED
All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice, this
  list of conditions and the following disclaimer in the documentation and/or
  other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
