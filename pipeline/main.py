from argparse import ArgumentParser
from pathlib import Path

# mNGS 过滤 tNGS 靶标污染
from src import MngsFilterVirusTarget


class Pipeline:

    def __init__(self):

        ap = ArgumentParser()
        ap.add_argument("-id", "--in_dir", type=str, required=True)
        ap.add_argument("-od", "--out_dir", type=str, required=True)
        ap.add_argument("-c", "--cpu", type=int, default=1)

        self.args = ap.parse_args()
        self.in_dir = Path(self.args.in_dir).absolute()
        self.out_dir = Path(self.args.out_dir).absolute()
        self.out_dir.mkdir(parents=True, exist_ok=True)
        self.cpu = self.args.cpu if self.args.cpu > 0 else 1

    def m_filter_t(self):
        """
        mNGS 流程 过滤 tNGS 污染的靶标序列
        :return:
        """
        (
            # 初始化
            MngsFilterVirusTarget(
                # 输入目录
                in_dir=self.in_dir.joinpath("raw_fqs"),
                # 输出目录
                out_dir=self.out_dir.joinpath("filtered_fqs"),
                # 并行数
                cpu=8,
                # 比对分数阈值
                T=20,
                # 错配罚分
                B=2
            )
            # 运行命令行
            .run()
        )


if __name__ == "__main__":
    pipeline = Pipeline()
    pipeline.m_filter_t()
