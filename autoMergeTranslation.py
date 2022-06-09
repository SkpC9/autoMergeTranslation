# （判断文件是否被修改过）
# 遍历mod的所有fmg文件并解包
# 每一个fmg文件
# 先解包，然后找到对应的xml，根据base找到mod修改的text id，然后直接往merge融合
# 按照加载顺序不断重复上述过程

# Yabber 不支持自定义输出位置，默认是在输入的旁边
# dcx->folder/fmg->xml
# dcx循环+fmg循环，fmg循环内部进行每一个textid的比较与合并

from ast import mod
import xml.etree.ElementTree as ET
from tqdm import tqdm
from distutils.dir_util import copy_tree
import subprocess
import os
import filecmp
import configparser
# import time

# 先全部解包 # 先解包每一个msgbnd，再解包每一个fmg，得到xml文件


def findFileInFolder(file_name, folder):
    for root, dirs, files in os.walk(folder):
        if file_name in files:
            return os.path.join(root, file_name)


def extractMsgAndFmg(current_msg_folder, Yabber_folder):
    print('start extracting msgbnd.dcx files')
    Yabber_path = os.path.join(Yabber_folder, 'Yabber.exe')
    for root, _, files in os.walk(current_msg_folder, topdown=False):
        # delete those not endswith .csv, in case some mod put bin and csv in the same folder
        current_files = [f for f in files if f.endswith("msgbnd.dcx")]
        if len(current_files) == 0:
            continue
        for name in tqdm(current_files):
            tqdm.write('current msgbnd.dcx file: ' + name)
            # shell_command = '"' + Yabber_path + '" "' + os.path.join(root,name) + '"'
            # os.system 使用的是cmd而不是powershell
            # 好像也不是cmd？cmd里能运行但这里还是路径有问题
            # 还是用subprocess吧
            subprocess.call([Yabber_path, os.path.join(root, name)],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print('finished extracting msgbnd.dcx files')

    print('start extracting fmg files')
    for root, _, files in os.walk(current_msg_folder, topdown=False):
        # delete those not endswith .csv, in case some mod put bin and csv in the same folder
        current_files = [f for f in files if f.endswith(".fmg")]
        if len(current_files) == 0:
            continue
        for name in tqdm(current_files):
            tqdm.write('current fmg file: ' + name)
            subprocess.call([Yabber_path, os.path.join(root, name)],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print('finished extracting fmg files')

    return


# https://stackoverflow.com/questions/25338817/sorting-xml-in-python-etree
def sortChildrenBy(parent, attr):
    parent[:] = sorted(parent, key=lambda child: child.get(attr))


def main():
    config = configparser.ConfigParser()
    try:
        with open('./autoMergeTranslation.ini') as config_file:
            config.read_file(config_file)
            Yabber_folder = config['Paths']['Yabber_folder']
            base_msg_folder = config['Paths']['base_msg_folder']
            merged_msg_folder = config['Paths']['merged_msg_folder']
            temp_list = []
            for (index, mod_msg_folder) in config.items('mod_msg_folders'):
                temp_list.append(mod_msg_folder.strip())
            mod_msg_folders = temp_list
    except Exception as e:
        print('no valid ini config found. creating one with default values')
        # default value
        config.clear()
        config['Paths'] = {
            'Yabber_folder': r'G:\Games\VortexResource\Games\eldenring\tools\Yabber 1.3.1',
            'base_msg_folder': r'./basemsg',
            'merged_msg_folder': r'G:\Games\VortexResource\Games\eldenring\mods\merged_translation\mod\msg\zhocn',
        }
        config['mod_msg_folders'] = {
            0: r"G:\Games\VortexResource\Games\eldenring\mods\Grand Merchant - Standard - 1.08 Chinese Translation-969-1-08-1651367644",
            1: r"G:\Games\VortexResource\Games\eldenring\mods\chinese  ERR - Elden Ring Reforged-1400-1-10-1654734183",
        }
        with open('./autoMergeTranslation.ini', 'w') as config_file:
            config.write(config_file)
        print('Please change the values according to your file locations, then restart program')
        input("Press Enter to exit")
        return

    input("Press Enter to start")

    # 解包base
    print("extracting base")
    extractMsgAndFmg(base_msg_folder, Yabber_folder)

    # 将base copy到merged
    copy_tree(base_msg_folder, merged_msg_folder)

    # 按照顺序循环每一个mod

    print("\nmerging translations")
    for mod_index, mod_msg_folder in enumerate(mod_msg_folders):
        print("mod index = ", mod_index)
        extractMsgAndFmg(mod_msg_folder, Yabber_folder)
        print("start merging xmls")
        for root, _, files in os.walk(mod_msg_folder, topdown=False):
            # delete those not endswith .csv, in case some mod put bin and csv in the same folder
            current_files = [f for f in files if f.endswith("fmg.xml")]
            # 找mod路径中的每一个xml，进行比较与合并(要注意排除Yabber的xml)
            # 找fmg.xml就可以自动排除Yabber的xml了
            # try:
            #     current_files.remove('_yabber-bnd4.xml')
            # except ValueError:
            #     pass
            if len(current_files) == 0:
                continue
            for name in tqdm(current_files):
                tqdm.write('current xml file: ' + name)

                # file_relpath = os.path.relpath(
                #     path=os.path.join(root, name), start=mod_msg_folder)
                # current_xml_mod_path = os.path.join(mod_msg_folder, file_relpath)
                # current_xml_base_path = os.path.join(base_msg_folder, file_relpath)
                # current_xml_merged_path = os.path.join(
                #     merged_msg_folder, file_relpath)

                # 使用下面的寻找路径方式即可让msgbnd.dcx文件可被任意放置，避免Vortex中显示冲突
                current_xml_mod_path = findFileInFolder(name, mod_msg_folder)
                current_xml_base_path = findFileInFolder(name, base_msg_folder)
                current_xml_merged_path = findFileInFolder(
                    name, merged_msg_folder)
                # 首先直接判断mod与base 是否相等。若相等则跳过
                if filecmp.cmp(current_xml_mod_path, current_xml_base_path):
                    continue
                # 不相等则逐个判断每个text是否相等
                tqdm.write("file modified by mod")
                current_xml_mod = ET.parse(current_xml_mod_path).getroot()
                current_xml_base = ET.parse(current_xml_base_path).getroot()
                current_xml_merged_tree = ET.parse(current_xml_merged_path)
                current_xml_merged = current_xml_merged_tree.getroot()

                # 用字典的时候就不需要排序了
                # # 最好先给这三个xml都根据id来排个序
                # temp_time = time.time()
                # sortChildrenBy(current_xml_mod.find(".//entries"),'id')
                # sortChildrenBy(current_xml_base.find(".//entries"),'id')
                # sortChildrenBy(current_xml_merged.find(".//entries"),'id')

                # tqdm.write("sort_time : "+ str(time.time()-temp_time))
                mod_text_list = current_xml_mod.findall(".//text")
                # 字典key=id ，value=element
                base_text_dict = {}
                merged_text_dict = {}
                # temp_time = time.time()
                for base_temp_text in current_xml_base.findall(".//text"):
                    base_text_dict[base_temp_text.get('id')]=base_temp_text
                for merged_temp_text in current_xml_merged.findall(".//text"):
                    merged_text_dict[merged_temp_text.get('id')]=merged_temp_text
                # tqdm.write("init_dict_time : "+ str(time.time()-temp_time))
                # 和base不相等就直接更新merged，不判断是否和merged相等了
                temp_count = 0
                # compare_time = 0
                # search_time = 0
                # update_time = 0
                base_text_list = []
                for element_index, each_element in enumerate(mod_text_list):
                    text_id = each_element.get('id')
                    mod_text = each_element.text
                    # 如果mod_text == %null$ 则直接跳过
                    if mod_text == '%null%':
                        continue
                    # 用findall来找id太慢了，可以考虑根据现有的顺序弄一个偏移量。后来想想用字典好像也可以

                    if text_id in base_text_dict:
                        # temp_time = time.time()
                        base_text_list = [base_text_dict[text_id]]
                        # search_time += time.time()-temp_time

                        base_text = base_text_list[0].text
                        # temp_time = time.time()
                        temp_bool = base_text == mod_text
                        # compare_time += time.time()-temp_time
                        if not temp_bool:
                            # temp_time = time.time()
                            merged_text_dict[text_id].text = mod_text
                            # update_time += time.time()-temp_time
                            temp_count += 1
                    else:
                        temp_count += 1
                        # 如果在base中找不到，就去merged中找
                        # 如果merged中找到了，就直接修改
                        if text_id in merged_text_dict:
                            # temp_time = time.time()
                            merged_text_dict[text_id].text = mod_text
                            # update_time += time.time()-temp_time

                        # 如果merged中找不到，就向xml中添加一个新的node  其实应该是可以直接从mod那里复制过来的
                        else:
                            # temp_time = time.time()
                            entries = current_xml_merged.find(".//entries")
                            # search_time += time.time()-temp_time
                            temp_element = ET.Element('text', {'id': text_id})
                            temp_element.text = mod_text
                            entries.append(temp_element)

                            
                tqdm.write("number of texts updated : " + str(temp_count))
                # tqdm.write("compare_time : " + str(compare_time))
                # tqdm.write("search_time : " + str(search_time))
                # tqdm.write("update_time : " + str(update_time))
                # 在merged中按照text的id顺序进行排序。# 暂时不排序，让游戏去提取
                sortChildrenBy(current_xml_merged.find(".//entries"),'id')
                # 保存merged xml文件
                current_xml_merged_tree.write(
                    current_xml_merged_path, encoding="utf-8", xml_declaration=True)
                pass
        print("finished merging xmls")
    print('--------------')

    # 重新打包merged
    Yabber_path = os.path.join(Yabber_folder, 'Yabber.exe')
    # 需要先打包xml成fmg，再打包文件夹
    print('start packing fmg.xml files')
    for root, _, files in os.walk(merged_msg_folder, topdown=False):
        current_files = [f for f in files if f.endswith("fmg.xml")]
        if len(current_files) == 0:
            continue
        for name in tqdm(current_files):
            tqdm.write('current fmg.xml file: ' + name)
            subprocess.call([Yabber_path, os.path.join(root, name)],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print('finished packing fmg.xml files')
    # 打包文件夹msgbnd-dcx
    print('start packing msgbnd-dcx folders')
    for root, dirs, _ in os.walk(merged_msg_folder, topdown=False):
        current_dirs = [f for f in dirs if f.endswith("msgbnd-dcx")]
        if len(current_dirs) == 0:
            continue
        for name in tqdm(current_dirs):
            tqdm.write('current msgbnd-dcx dir: ' + name)
            subprocess.call([Yabber_path, os.path.join(root, name)],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print('finished packing msgbnd-dcx folders')
    print("all done")
    input("Press Enter to exit")


if __name__ == '__main__':
    main()
