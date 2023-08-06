# imgsplit

Utility to split an image file into multiple segement files by
removing runs of null or zero bytes.

Flashing just the non-null segments of an embedded firmware can be
substantially faster than flashing the entire image.

## Install

```pip3 install imgsplit```

## Usage

```
imgsplit input.img


imgsplit input output_segment_at_%d.img`
```

```
$ imgsplit --help
Usage:
    imgsplit (--version|--help)
    imgsplit [--bs BS] [--minskip MINSKIP] [--outdir OUTDIR] <image> [<outpattern>]

Arguments:
    --bs BS            Block size in bytes. Segments are aligned to this size. [default: 512]
    --minskip MINSKIP  Minimum number of zero blocks to skip. [default: 1024]
    --outdir OUTDIR    Directory to put the image segments in. [default: ./]
    <image>            Image file to split.
    <outpattern>       Pattern to expand with segment offset to name the segment files, e.g., `image_%08x.img`.
```

## Contributing

Please submit bugs, questions, suggestions, or (ideally) contributions
as issues and pull requests on Github.

### Authors
**David R. Bild**

+ [https://www.davidbild.org](https://www.davidbild.org)
+ [https://github.com/drbild](https://github.com/drbild)

## License
Copyright 2019 David R. Bild

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this work except in compliance with the License. You may obtain a copy of the
License from the LICENSE.txt file or at

[http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
