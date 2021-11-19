# Copyright (c) 2021 Sultim Tsyrendashiev
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import sys
import pathlib
import zipfile
import shutil
import subprocess


FILES_TO_INCLUDE = [
    "Controls\\00-Default.ctl",
    "Controls\\00-Default.des",
    "Controls\\System",
    "Controls\\System\\Common.ctl",
    "Data\\Credits.txt",
    "Data\\Default.ifr",
    "Data\\Defaults",
    "Data\\Defaults\\WorldEditor.reg",
    "Data\\IFeel.txt",
    "Data\\Logitech.ifr",
    "Data\\NoCRC.lst",
    "Data\\SED_TipOfTheDay.txt",
    "Players\\about_this_directory.txt",
    "Scripts\\Dedicated_startup.ini",
    "Scripts\\menu",
    "Scripts\\menu\\ApplyShadowmaps.ini",
    "Scripts\\menu\\ApplyTextures.ini",
    "Scripts\\menu\\ApplyVideo.ini",
    "Scripts\\menu\\GameOptions.cfg",
    "Scripts\\menu\\RenderingOptions.cfg",
    "Scripts\\menu\\SPOptions.cfg",
    "Scripts\\NetSettings",
    "Scripts\\NetSettings\\56-normal.des",
    "Scripts\\NetSettings\\56-normal.ini",
    "Scripts\\NetSettings\\56k-quality.des",
    "Scripts\\NetSettings\\56k-quality.ini",
    "Scripts\\NetSettings\\DSLCable.des",
    "Scripts\\NetSettings\\DSLCable.ini",
    "Scripts\\NetSettings\\ISDN.des",
    "Scripts\\NetSettings\\ISDN.ini",
    "Scripts\\NetSettings\\LAN.des",
    "Scripts\\NetSettings\\LAN.ini",
    "Scripts\\NetSettings\\OldModem.des",
    "Scripts\\NetSettings\\OldModem.ini",
    "Temp\\empty",
    "LICENSE",
    "ModEXT.txt",
    "SE1_10.gro",
    "Levels\\empty",
    "OverridenTextures\\BlueNoise_LDR_RGBA_128.ktx2",
    "OverridenTextures\\WaterNormal_n.ktx2",
    "Bin\\Game.dll",
    "Bin\\libogg.dll",
    "Bin\\libvorbis.dll",
    "Bin\\libvorbisfile.dll",
    "Bin\\SeriousSamTFE.exe",
    "Bin\\Engine.dll",
    "Bin\\Entities.dll",
    "Sources\\RTGL1\\Build\\RtRaygenPrimary.rgen.spv",
    "Sources\\RTGL1\\Build\\RtRaygenDirect.rgen.spv",
    "Sources\\RTGL1\\Build\\RtRaygenIndirect.rgen.spv",
    "Sources\\RTGL1\\Build\\RtMiss.rmiss.spv",
    "Sources\\RTGL1\\Build\\RtMissShadowCheck.rmiss.spv",
    "Sources\\RTGL1\\Build\\RtClsOpaque.rchit.spv",
    "Sources\\RTGL1\\Build\\RtAlphaTest.rahit.spv",
    "Sources\\RTGL1\\Build\\CmComposition.comp.spv",
    "Sources\\RTGL1\\Build\\CmLuminanceHistogram.comp.spv",
    "Sources\\RTGL1\\Build\\CmLuminanceAvg.comp.spv",
    "Sources\\RTGL1\\Build\\Rasterizer.vert.spv",
    "Sources\\RTGL1\\Build\\Rasterizer.frag.spv",
    "Sources\\RTGL1\\Build\\RasterizerMultiview.vert.spv",
    "Sources\\RTGL1\\Build\\FullscreenQuad.vert.spv",
    "Sources\\RTGL1\\Build\\DepthCopying.frag.spv",
    "Sources\\RTGL1\\Build\\CmVertexPreprocess.comp.spv",
    "Sources\\RTGL1\\Build\\CmSVGFTemporalAccumulation.comp.spv",
    "Sources\\RTGL1\\Build\\CmSVGFEstimateVariance.comp.spv",
    "Sources\\RTGL1\\Build\\CmSVGFAtrous.comp.spv",
    "Sources\\RTGL1\\Build\\CmSVGFAtrous_Iter0.comp.spv",
    "Sources\\RTGL1\\Build\\CmASVGFMerging.comp.spv",
    "Sources\\RTGL1\\Build\\CmASVGFGradientSamples.comp.spv",
    "Sources\\RTGL1\\Build\\CmASVGFGradientAtrous.comp.spv",
    "Sources\\RTGL1\\Build\\CmBloomDownsample.comp.spv",
    "Sources\\RTGL1\\Build\\CmBloomUpsample.comp.spv",
    "Sources\\RTGL1\\Build\\CmCheckerboard.comp.spv",
]

DEFAULT_SS_FOLDER_NAME = "../Serious-Engine-RT"
DEFAULT_OUTPUT_FOLDER_NAME = "../SSRT-TFE"

COPY_FROM_WORKING_FOLDER_SOURCE_FILE = "SSRT_TFE_Readme.txt"
COPY_FROM_WORKING_FOLDER_DESTINATION_FILE = "README.txt"

CREATE_EMPTY_FILE = "Scripts\\PersistentSymbols.ini"

TEXTURES_SS_FOLDER_SOURCE_FILE = "OverridenTextures\\OverridenTextures.zip"
TEXTURES_SS_FOLDER_DESTINATION_FILE = "TFE_RT_Textures.zip"

TEXTURES_UPDATE_SCRIPT_WORKING_FOLDER = "OverridenTextures"
TEXTURES_UPDATE_SCRIPT = "UpdateTextureZIP.bat"

OUTPUT_ZIP_BIN_FILE_NAME = "TFE_RT_Bin.zip"


def mrCopyFile(srcPath, dstPath):
    print("Copying " + str(dstPath.name))
    # need to create directory before copying
    pathlib.Path(dstPath).parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(srcPath, dstPath)


def printHelp():
    print("Usage: MakeReleaseVersion.py <-b> <output folder (optional)> <SeriousSam folder (optional)>")
    print("")
    print("  <-b> : only update zip file with binaries")


def main():
    outputFolderPath = pathlib.Path(DEFAULT_OUTPUT_FOLDER_NAME)
    ssFolderPath = pathlib.Path(DEFAULT_SS_FOLDER_NAME)

    args = sys.argv[1:]

    if '--help' in args or '-help' in args or '--h' in args or '-h' in args:
        printHelp()
        return

    onlyBinUpdate = '-b' in args
    if onlyBinUpdate:
        args.remove('-b')

    if len(args) == 1:
        outputFolderPath = pathlib.Path(args[0])
    elif len(args) == 2:
        outputFolderPath = pathlib.Path(args[0])
        ssFolderPath = pathlib.Path(args[1])
    elif len(args) > 2:
        printHelp()
        return

    if not ssFolderPath.exists():
        print("Folder " + str(ssFolderPath) + " doesn't exist")
        return

    if not onlyBinUpdate and outputFolderPath.exists():
        print("Folder " + str(outputFolderPath) + " must not exist. Specify a new one")
        return

    if ssFolderPath == outputFolderPath:
        print("Input and output must not be same")
        return

    if not onlyBinUpdate:
        while True:
            print("Update \"" + TEXTURES_SS_FOLDER_DESTINATION_FILE + "\" before copying? (Y/N)")
            answer = input()
            if answer == 'Y' or answer == 'y':
                r = subprocess.run(
                    TEXTURES_UPDATE_SCRIPT,
                    capture_output=True,
                    shell=True,
                    cwd=ssFolderPath / pathlib.Path(TEXTURES_UPDATE_SCRIPT_WORKING_FOLDER))
                if r.returncode != 0:
                    print("Updating textures error. Aborting.")
                    return
                break
            elif answer == 'N' or answer == 'n':
                break

        mrCopyFile(
            pathlib.Path(COPY_FROM_WORKING_FOLDER_SOURCE_FILE),
            outputFolderPath / pathlib.Path(COPY_FROM_WORKING_FOLDER_DESTINATION_FILE)
        )

        mrCopyFile(
            ssFolderPath / pathlib.Path(TEXTURES_SS_FOLDER_SOURCE_FILE),
            outputFolderPath / pathlib.Path(TEXTURES_SS_FOLDER_DESTINATION_FILE)
        )

    with zipfile.ZipFile(outputFolderPath / pathlib.Path(OUTPUT_ZIP_BIN_FILE_NAME), 'w') as outputZip:
        for f in FILES_TO_INCLUDE:
            srcFilePath = pathlib.Path(f)
            srcPath = ssFolderPath / srcFilePath

            if not srcPath.exists():
                print("Source file " + str(srcPath) + " doesn't exist. Aborting.")
                return

            print("Adding " + str(srcFilePath))
            outputZip.write(filename=srcPath, arcname=str(srcFilePath))
        # also write an empty file
        outputZip.writestr(zinfo_or_arcname=CREATE_EMPTY_FILE, data=bytes(0))


    print("\nDone.")

    if onlyBinUpdate:
        print(str(outputFolderPath.name) + " formed.")
    else:
        print(OUTPUT_ZIP_BIN_FILE_NAME + " updated.")


if __name__ == '__main__':
    main()
