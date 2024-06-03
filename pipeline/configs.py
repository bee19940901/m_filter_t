from pathlib import Path

SCRIPT = Path(__file__).absolute()
PIPELINE = SCRIPT.parent
PROJECT = PIPELINE.parent
DATABASE = PROJECT.joinpath("database")
SOFTWARE = PROJECT.joinpath("software")
WORKSPACE = PROJECT.joinpath("workspace")

# software 
PYTHON3 = SOFTWARE.joinpath('bin', 'python3')
SAMTOOLS = SOFTWARE.joinpath('bin', 'samtools')
BWA = SOFTWARE.joinpath('bin', 'bwa')

# database
REF_FA = DATABASE.joinpath("targets", "ref.fa")