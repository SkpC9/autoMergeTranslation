# autoMergeTranslation

你现在在使用中文

[English_Description](README.md)

## **简介**

用于自动化合并艾尔登法环的翻译模组（mod）提供的msgbnd.dcx文件

[Yabber](https://github.com/JKAnderson/Yabber) 被用来解包和打包文件

[ER.BDT.Tool](https://github.com/Ekey/ER.BDT.Tool) 被用来从游戏本体中解包得到msgbnd文件。（使用此程序不需要安装ER.BDT.Tool）

为了使用方便，我在release中包含了游戏本体的msgbnd.dcx文件

[演示视频](https://www.bilibili.com/video/BV1RL4y1K7Qh/)

## **使用说明**

1. 安装 [Yabber v1.3.1](https://github.com/JKAnderson/Yabber/releases/tag/1.3.1)
2. 从 [release](https://github.com/SkpC9/autoMergeTranslation/releases) 页面下载 autoMergeTranslation.7z 文件
3. 解压文件，然后复制你语言对应的从游戏本体解包出来的msgbnd.dcx文件到 basemsg 文件夹
4. 打开 autoMergeTranslation.exe。初次打开将自动创建 ini 配置文件。按照配置文件中的示例根据你的文件路径设置这些值

    * 配置项说明:
        * **'Yabber_folder'** : Yabber.exe 所在的文件夹
        * **'base_msg_folder'** : 存储从游戏本体解包得到的msgbnd.dcx文件
        * **'merged_msg_folder'** : 此程序的输出文件夹，合并后的文件将存放到此处
        * 在 **[mod_msg_folders]** 中，各条目按照模组加载顺序排序（目前只能人工决定加载顺序）。每一个值都是一个字符串 **mod_msg_folder**，里面包含各个模组提供的msgbnd.dcx文件

5. 按照程序的指示操作. 按 Enter 开始。在程序运行时可以继续使用电脑
6. 合并完成，程序会显示 all done。然后按 Enter 退出程序
7. 从 merged_msg_folder(在ini文件中配置过) 中获取合并后的msgbnd.dcx文件，然后 enjoy!
