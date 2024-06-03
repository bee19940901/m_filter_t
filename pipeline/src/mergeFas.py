import os

import re
from glob import glob
from warnings import warn
from argparse import ArgumentParser


def foo(x: str, y: list, N=0) -> str:
    """递归判断，修改序列ID 为 ID_1, ID_2, ID_3 以此类推"""
    if x in y:
        N += 1
        x = re.sub(r"_\d+$", "", x)
        x = f"{x}_{N}"
        return foo(x, y, N)
    else:
        return x


def read_fas(in_dir: str) -> dict:
    """从目录根据文件后缀信息获取fasta格式文件，并储存在字典中，重复序列id添加后缀"""
    all_files = glob(f"{in_dir}/*")
    all_fas = [i for i in all_files if re.match(r"^.+\.(fa|fas|fasta)$", i)]
    if len(all_fas) < 1:
        raise Exception(f"Can't glob any fasta file from {in_dir}")
    heads, fas = [], {}
    for fa in all_fas:
        with open(fa, "r", encoding="utf-8") as fr:
            for line in fr:
                line = line.strip()
                if line:
                    if line.startswith(">"):
                        head = re.sub(r"^>", "", line)
                        head = foo(head, heads)
                        heads.append(head)
                        fas[head] = ""
                    else:
                        fas[head] += line
    return fas


def duplicate_removal(in_fas: dict, length: int) -> dict:
    """每个靶标序列只保留前100bp, 并且去除重复的序列"""
    result, seqs = {}, []
    for k, v in in_fas.items():
        v = v[:length]
        if v in seqs:
            warn(f"\nSeq: {v} is duplicate so skipped!\n", category=Warning)
        else:
            result[k] = v
            seqs.append(v)
    return result


def write_fas(fas: dict, out_file: str) -> None:
    """将包含fasta信息的字典写入到文件中"""
    with open(out_file, "w", encoding="utf-8") as fw:
        for k, v in fas.items():
            fw.write(f">{k}\n{v}\n")


def main() -> None:
    """
    输入为一个目录包含多个需要合并的fasta格式文件 -i
    输出为合并后的fasta格式文件 -o
    每条序列默认只截取前100bp  -l default 100,
    如果序列重复则舍弃重复序列
    如果序列名重复则为序列名加上后缀，例如 _1, _2, _3
    """
    ap = ArgumentParser()
    ap.add_argument("-i", "--in_dir", required=True, help="input directory")
    ap.add_argument("-o", "--out_fa", required=True, help="output merged fasta file")
    ap.add_argument("-l", "--length", default=100, help="The length of the sequences preserved.")
    ag = ap.parse_args()
    in_dir, out_fa, length = os.path.abspath(ag.in_dir), os.path.abspath(ag.out_fa), ag.length
    all_fas = read_fas(in_dir=in_dir)
    uniq_fas = duplicate_removal(all_fas, length=length)
    write_fas(uniq_fas, out_fa)
    print(f"# ======== ALL JOBS DONE! ======== #\n")


if __name__ == "__main__":
    main()
