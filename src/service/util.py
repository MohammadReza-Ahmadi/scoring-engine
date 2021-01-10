import random
import string

from data.rule.rule_model import RuleModel
from infrastructure.constants import score_deliminator


def creat_rule(rule: RuleModel, code: str, min_val, max_val, score: int, desc: str):
    rule.code = code
    rule.min = min_val
    rule.max = max_val
    rule.score = score
    rule.desc = desc
    return rule


def creat_rule_by_status_code(rule: RuleModel, code: str, status_code: int, score: int, desc: str):
    rule.code = code
    rule.status_code = status_code
    rule.score = score
    rule.desc = desc
    return rule


def get_score_from_dict(scores: {}):
    return int(scores[0].split(score_deliminator)[0])


def get_score_code_from_dict(scores: {}):
    return scores[0].split(score_deliminator)[1]


def add_rule_model_to_dict(rdict: {}, r: RuleModel):
    rdict.__setitem__((str(r.score) + score_deliminator + r.code), r.max)
    return rdict


def add_rule_model_to_dict_by_rds_score(rdict: {}, r: RuleModel, rds_score: int):
    rdict.__setitem__((str(r.score) + score_deliminator + r.code), rds_score)
    return rdict


def add_item_to_dict(rdict: {}, key, value):
    rdict.__setitem__(key, value)
    return rdict


def filter_dict(dic: dict, filtered_item) -> dict:
    nd = {}
    for key, value in dic.items():
        if key != filtered_item:
            nd[key] = value
    return nd


def filter_dict_by_id(dic) -> dict:
    return filter_dict(dic, "_id")


# Random Generator Functions #
# generate random lowercase str by fix length
def get_random_lowercase_str(str_len):
    letters = string.ascii_lowercase
    # print(''.join(random.choice(letters) for i in range(10)))
    rand_str = random_choice(letters, str_len)
    return rand_str


# generate random uppercase str by fix length
def get_random_uppercase_str(str_len):
    letters = string.ascii_uppercase
    rand_str = random_choice(letters, str_len)
    return rand_str


# generate random letters str by fix length
def get_random_letters_str(str_len):
    letters = string.ascii_letters
    rand_str = random_choice(letters, str_len)
    return rand_str


# generate random digits str by fix length
def get_random_digits_str(str_len):
    letters = string.digits
    rand_digits = random_choice(letters, str_len)
    return rand_digits


# generate random punctuation str by fix length
def get_random_punctuation_str(str_len):
    letters = string.punctuation
    rand_str = random_choice(letters, str_len)
    return rand_str


def random_choice(letters, str_len):
    return ''.join(random.choice(letters) for i in range(str_len))
