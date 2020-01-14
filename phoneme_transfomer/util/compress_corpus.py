import re
import sys
import os


def main(corpora, output):
    for corpus in os.listdir(corpora):
        file = os.path.join(corpora, corpus)

        with open(file, 'r', encoding='utf-16') as text:
            stopwords = [
                re.compile('--'),
                re.compile('구술|녹음|웃음'),
            ]

            corpus = text.read().splitlines()
            corpus = ''.join(corpus)
            isspeech = re.compile('\d{6}[^(-)]+[(][^(-)]+[)]')

            in_bracket = re.compile('[(][^(-)]+[)]')
            in_text = re.compile('(@|#)[^(-)]+[(]')

            if not os.path.exists(output):
                os.makedirs(output)
                target = open(os.path.join(output, 'koje_par.txt'), mode='w')
                target.close()
            target = open(os.path.join(output, 'koje_par.txt'), mode='a')
            for speech in isspeech.finditer(corpus):
                line = speech.group()
                if stopwords[0].search(line) or stopwords[1].search(line):
                    continue
                else:
                    jeju = in_text.search(line)
                    stan = in_bracket.search(line)
                    if jeju and stan:
                        target.write(stan.group()[1:-1]+'\t'+jeju.group()[2:-1])
                        target.write('\n')
                    else:
                        continue
            target.close()


if __name__ == '__main__':
    args = sys.argv[1:]
    main(*args)
