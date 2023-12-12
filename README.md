# Core Template
This is a template repository for a core which contains all of the core definition JSON files and FPGA starter code.

It has been modified by agg23 to clean up the structure and add utility files, and by andi mcc to display a "screen test" image. On firmware 1.2, this "screen test" will fit itself exactly to the size of the screen in both docked and handheld mode. See [info.txt](dist/Cores/Developer.CoreTemplate/info.txt).

# Build

Although build invocations will vary from machine to machine, here is a sample code that works on my Linux machine. This invocation assumes quartus is installed at the given location in `~usr/` and that the [Analogue bit reverser sample program](https://www.analogue.co/developer/docs/packaging-a-core#creating-a-reversed-rbf) is installed in `../reverse`.

```
(cd src/fpga && ~/usr/intelFPGA_lite/22.1std/quartus/bin/quartus_sh --flow compile ap_core) && (rm -f dist/Cores/Developer.CoreTemplate/bitstream.rbf_r && ../reverse/a.out ./src/fpga/output_files/ap_core.rbf dist/Cores/Developer.CoreTemplate/bitstream.rbf_r)
```

Once these steps have been run, the `dist/` directory can be zipped to create a [installable zip](https://www.analogue.co/developer/docs/packaging-a-core#naming-of-the-.zip-file), as in:

```
cd dist && zip -r ../Developer.CoreTemplate_1.2.0_2023-12-12.zip .
```

Or copied to a mounted SD card:

```
rsync -avhi dist/ /media/path/to/usbmount/ && sync
```

# License

Modifications in this directory by Andi McClure (mostly in core_top.sv) are available under the MIT license:

> Copyright (c) 2023 Andi McClure
>
> Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
>
> The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
>
> THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

If this license is too restrictive for some reason, feel free to contact me.

Agg23's additions to the project are in standalone files, which have their licenses stated at the top. As of this commit, none of these additions are linked in.

Analogue's original legal notice for the underlying base project is reproduced below: 

## Legal
Analogue’s Development program was created to further video game hardware preservation with FPGA technology. Analogue Developers have access to Analogue Pocket I/O’s so Developers can utilize cartridge adapters or interface with other pieces of original or bespoke hardware to support legacy media. Analogue does not support or endorse the unauthorized use or distribution of material protected by copyright or other intellectual property rights.
