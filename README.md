# autoMergeTranslation

You are now in English

[中文介绍](README.zh_CN.md)

## **About**

This is for the automation of merging msgbnd.dcx files from Elden Ring translation mods.

[Yabber](https://github.com/JKAnderson/Yabber) is used for extracting and repacking files

[ER.BDT.Tool](https://github.com/Ekey/ER.BDT.Tool) is used for extracting game data files to msgbnd files (not needed to use this program)

For user convenience, I included game msgbnd files from Elden Ring in release files.

[Demonstration Video](https://youtu.be/gDca0l99abU)

## **Usage**

1. Install [Yabber v1.3.1](https://github.com/JKAnderson/Yabber/releases/tag/1.3.1)
2. Download autoMergeTranslation.7z file from [release](https://github.com/SkpC9/autoMergeTranslation/releases) page
3. Extract the zip file, then copy the base msgbnd.dcx files of your language to basemsg folder
4. Open the autoMergeTranslation.exe. Initial open will auto create a ini config file. Follow the example to set those values according to your file paths

    * Config explanations:
        * **'Yabber_folder'** : the folder which Yabber.exe is in.
        * **'base_msg_folder'** : stores msg files extracted from base game for comparison
        * **'merged_msg_folder'** : the output folder of this program, stores merged msgbnd.dcx files.
        * In **[mod_msg_folders]** the items are sorted by mod load order(currently have to manually decide the order). Each value is a string **mod_msg_folder**, which contains mod msgbnd.dcx files.

5. Do as the program instructed. Press Enter to start. You can leave this program running in the background.
6. When finished, it says all done, the press Enter to exit.
7. Get the merged msgbnd.dcx files from merged_msg_folder(set in ini) and enjoy!
