import os
import hgtk

from tensor2tensor.data_generators import problem
from tensor2tensor.data_generators import text_problems
from tensor2tensor.utils import registry
from tensor2tensor.models.transformer import transformer_base_v1


FIRST_exHANGUL_UNICODE = ord('')
LAST_exHANGUL_UNICODE = ord('')


def  is_hangul_ex(char):



def sep_to_pho(line):
    result = []
    for char in line:
        if hgtk.checker.is_hangul(char):
            sep = list(hgtk.letter.decompose(char))
            if sep[0] == 'ㅇ':
                sep = sep[1:]
        else:
            if char == ' ':
                sep = ['#']
            else:
                sep = [char]
        result += sep
    if result[0] == '#':
        result = result[1:]
    return ''.join(result)


class Reader(object):
    def __init__(self, file_list, shuffle=True, total=None):
        self.file_list = file_list
        self.total = total  # if not total -> 무제
        self.counter = 0

    def generate(self):
        breaker = False
        for file in self.file_list:
            if breaker:
                break
            with open(file, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    l = line.split('\t')

                    input_data = sep_to_pho(l[1])
                    target_data = sep_to_pho(l[0])

                    if self.total:
                        self.total -= 1
                        if not self.total:
                            breaker = True
                            break
                    self.counter +=1
                    print(self.counter)
                    yield {'inputs': input_data, 'targets': target_data}


@registry.register_hparams('hparam_transformer_t2t')
def hparam_transformer_t2t():
    hp = transformer_base_v1()
    hp.summarize_vars = True
    return hp


@registry.register_problem('transformer_t2t')
class transformer_t2t(text_problems.Text2TextProblem):
    @property
    def dataset_splits(self):
        return [{
            "split": problem.DatasetSplit.TRAIN,
            "shards": 100,
        }, {
            "split": problem.DatasetSplit.EVAL,
            "shards": 20,
        }]

    @property
    def is_generate_per_split(self):
        return True

    @property
    def approx_vocab_size(self):
        return 2**15

    def generate_samples(self, data_dir, tmp_dir, dataset_split):
        data_file_list = [os.path.join(data_dir, file) for file in os.listdir(data_dir) if file.endswith('.txt')]
        div = 'train'
        total = None
        reader = Reader(
            file_list=data_file_list,
            shuffle=True,
            total=total
        )
        for data in reader.generate():
            yield data
