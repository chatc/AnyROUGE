import os
from ThirdParty.ROUGE import pyrouge


def make_html_safe(s):
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    return s


def rouge(ref, hyp, log_path):
    assert len(ref) == len(hyp)
    ref_dir = os.path.join(log_path,'reference/')
    cand_dir = os.path.join(log_path,'candidate/')
    if not os.path.exists(ref_dir):
        os.mkdir(ref_dir)
    if not os.path.exists(cand_dir):
        os.mkdir(cand_dir)
    for i in range(len(ref)):
        with open(ref_dir + "%06d_reference.txt" % i, 'w', encoding='utf-8') as f:
            f.write(make_html_safe(ref[i]) + '\n')
        with open(cand_dir + "%06d_candidate.txt" % i, 'w', encoding='utf-8') as f:
            f.write(make_html_safe(hypo[i]) + '\n')

    r = pyrouge.Rouge155()
    r.model_filename_pattern = '#ID#_reference.txt'
    r.system_filename_pattern = '(\d+)_candidate.txt'
    r.model_dir = ref_dir
    r.system_dir = cand_dir
    rouge_results = r.convert_and_evaluate()
    scores = r.output_to_dict(rouge_results)
    recall = [round(scores["rouge_1_recall"] * 100, 2),
              round(scores["rouge_2_recall"] * 100, 2),
              round(scores["rouge_l_recall"] * 100, 2)]
    precision = [round(scores["rouge_1_precision"] * 100, 2),
                 round(scores["rouge_2_precision"] * 100, 2),
                 round(scores["rouge_l_precision"] * 100, 2)]
    f_score = [round(scores["rouge_1_f_score"] * 100, 2),
               round(scores["rouge_2_f_score"] * 100, 2),
               round(scores["rouge_l_f_score"] * 100, 2)]
    print("F_measure: %s Recall: %s Precision: %s\n"
          % (str(f_score), str(recall), str(precision)))

    with open(ref_dir + "rougeScore", 'w+', encoding='utf-8') as f:
        f.write("F_measure: %s Recall: %s Precision: %s\n"
                % (str(f_score), str(recall), str(precision)))
    return f_score[:], recall[:], precision[:]

def readline_aslist(path):
    data = []
    with open(path, 'r', encoding='utf-8') as file:
        for line in file:
            data.append(line.strip().replace('\n',''))
    return data


if __name__ == '__main__':
    # create a cache folder to store the intermediate results
    log_path = "./test"
    if not os.path.exists(log_path):
        os.makedirs(log_path)

    # read the hypo and target files as lists
    hypo_file_name = 'test.hypo'
    test_file_name = 'test.target'
    ref = readline_aslist("./{}".format(test_file_name))
    hypo = readline_aslist("./{}".format(hypo_file_name))

    print("source file: ", hypo_file_name)
    print("target file: ", test_file_name)

    # run the rouge evaluation
    rouge(ref, hypo, log_path)