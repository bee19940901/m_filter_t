from pathlib import Path
from re import sub

from utils import Cmds
from configs import BWA, SAMTOOLS, REF_FA


class MngsFilterVirusTarget:

    def __init__(self, in_dir: Path, out_dir: Path, cpu: int = 1, T: int = 20, B: int = 2):
        """
        初始化
        :param in_dir: 输入目录
        :param out_dir: 输出目录
        :param cpu: 使用的CPU核心数，默认为1
        :param T: 比对分数阈值，默认为20
        :param B: 错配罚分，默认为2
        """
        self.in_dir = in_dir
        self.out_dir = out_dir
        self.out_dir.mkdir(parents=True, exist_ok=True)
        self.cpu = cpu if cpu > 0 else 1
        self.T = T if T > 20 else 20
        self.B = B if B > 1 else 1
        self.shell_dir = self.out_dir.joinpath("work_sh")
        self.shell_dir.mkdir(parents=True, exist_ok=True)
        self.in_files = list(
            self.in_dir.glob("*.fq.gz")
        )
        self.samples = [
            sub(r"\.fq\.gz$", "", i.name)
            for i in self.in_files
        ]
        self.temp_dirs = [
            self.out_dir.joinpath(i)
            for i in self.samples
        ]
        _ = [
            i.mkdir(parents=True, exist_ok=True)
            for i in self.temp_dirs
        ]
        self.out_files = [
            i.joinpath(f"{s}.fa")
            for i, s in zip(self.temp_dirs, self.samples)
        ]
        self.shell_files = [
            self.shell_dir.joinpath(f"{s}.sh")
            for s in self.samples
        ]

    def run(self):
        Cmds(
            [
                f"{BWA} mem -T {self.T} -B {self.B} -t 8 {REF_FA} {in_file} | "
                f"{SAMTOOLS} fasta  -@ 8 -F 4 > {out_file}\n"
                for in_file, out_file
                in zip(self.in_files, self.out_files)
            ],
            self.shell_files
        ).multi_run(self.cpu)
