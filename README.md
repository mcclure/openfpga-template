# Core Template
This is a template repository for a core which contains all of the core definition JSON files and FPGA starter code.

It has been modified by agg23 to clean up the structure and add utility files, and by andi mcc to play a ~440 hz tone.

# Build

Although build invocations will vary from machine to machine, here is a sample code that works on my Linux machine. This invocation assumes quartus is installed at the given location in `~usr/` and that the [Analogue bit reverser sample program](https://www.analogue.co/developer/docs/packaging-a-core#creating-a-reversed-rbf) is installed in `../reverse`.

```
(cd src/fpga && ~/usr/intelFPGA_lite/22.1std/quartus/bin/quartus_sh --flow compile ap_core) && (rm -f dist/Cores/Developer.CoreTemplate/bitstream.rbf_r && ../reverse/a.out ./src/fpga/output_files/ap_core.rbf dist/Cores/Developer.CoreTemplate/bitstream.rbf_r)
```

Once these steps have been run, the `dist/` directory can be zipped to create a [installable zip](https://www.analogue.co/developer/docs/packaging-a-core#naming-of-the-.zip-file), as in:

```
cd dist && zip -r ../Developer.CoreTemplate_1.1.0_2023-09-11.zip .
```

Or copied to a mounted SD card:

```
rsync -avhi dist/ /media/path/to/usbmount/ && sync
```

# License

Andi McClure considers her additions to this branch trivial and non-copyrightable. For the avoidance of doubt, she releases these additions under the [Creative Commons Zero](https://creativecommons.org/publicdomain/zero/1.0/legalcode) license (public domain).

Agg23's additions to the project are in standalone files, which have their licenses stated at the top.

Analogue's original legal notice for the underlying base project is reproduced below: 

## Legal
Analogue’s Development program was created to further video game hardware preservation with FPGA technology. Analogue Developers have access to Analogue Pocket I/O’s so Developers can utilize cartridge adapters or interface with other pieces of original or bespoke hardware to support legacy media. Analogue does not support or endorse the unauthorized use or distribution of material protected by copyright or other intellectual property rights.
