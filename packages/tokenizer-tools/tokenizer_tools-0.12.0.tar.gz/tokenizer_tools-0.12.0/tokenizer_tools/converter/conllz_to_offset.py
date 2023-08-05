from tokenizer_tools.conllz.sentence import Sentence
from tokenizer_tools.tagset.NER.BILUO import BILUOSequenceEncoderDecoder
from tokenizer_tools.tagset.offset.sequence import Sequence


def conllz_to_offset(sentence_data: Sentence, raise_exception=False):
    decoder = BILUOSequenceEncoderDecoder()

    input_text = sentence_data.word_lines
    tags_seq = sentence_data.get_attribute_by_index(0)

    failed = False
    try:
        seq = decoder.to_offset(tags_seq, input_text)
    except:
        if not raise_exception:
            # invalid tag sequence will raise exception
            # so return a empty result
            seq = Sequence(input_text)
            failed = True
        else:
            raise

    return seq, failed
