from transformers import GPT2LMHeadModel, GPT2Tokenizer
from torch import Tensor


class NeuralKant:
    """
    Class for generating text with pretrained ruGPT3

    ...

    Attributes
    ----------
    __tokenizer: GPT2Tokenizer
        Tokenizer for input text
    __model: GPT2LMHeadModel
        Trained a neural network to generate text
    __mode: bool
        Current state of the model. Turned on/off the generation of the text on the received message
    __max_length : int
        Maximum length of generated text
    __repetition_penalty : float
        Used to punish words that have already been created or belong to the context
    __top_k : int
        In Top-K sampling, the K most likely next words are filtered and the probability mass is redistributed
            among only those K next words.
    __top_p : float
        Top-p sampling chooses from the smallest possible set of words whose cumulative probability exceeds
            the probability p. The probability mass is then redistributed among this set of words.
    __temperature: float
        increasing the likelihood of high probability words and decreasing the likelihood of low probability words
            by lowering the so-called temperature of the softmax.

    Methods
    -------
    generate_text(text)
        Generates a continuation for the given text
    __repr__()
        Displays information about the current state of the text generation parameters
    get_mode()
        Returns the current state of the attribute __mode
    set_mode
        Sets a new value for attribute mode
    set_temperature
        Sets a new value for attribute mode
    set_max_length
        Sets a new value for attribute max length
    set_top_k
        Sets a new value for attribute top_k
    set_top_p
        Sets a new value for attribute top_p
    set_default
        Sets options for generating default text
    """

    def __init__(self, max_length: int = 200, repetition_penalty: float = 5.0, top_k: int = 10,
                 top_p: float = 0.95, temperature: float = 1) -> None:
        self.__tokenizer: GPT2Tokenizer = GPT2Tokenizer.from_pretrained("../models/essays")
        self.__model: GPT2LMHeadModel = GPT2LMHeadModel.from_pretrained("../models/essays")
        self.__model.cuda()
        self.__mode = False
        self.__max_length = max_length
        self.__repetition_penalty = repetition_penalty
        self.__top_k = top_k
        self.__top_p = top_p
        self.__temperature = temperature

    def generate_text(self, text: str) -> str:
        input_token: Tensor = self.__tokenizer.encode(text, return_tensors="pt", )
        output_text: Tensor = self.__model.generate(input_token.cuda(), max_length=self.__max_length, do_sample=True,
                                                    repetition_penalty=self.__repetition_penalty, top_k=self.__top_k,
                                                    top_p=self.__top_p, temperature=self.__temperature)
        output_text: str = self.__tokenizer.decode(output_text[0]).replace('\xa0—', ' ').replace('\n', ' ')

        return output_text

    def __repr__(self) -> str:
        return f'Максимальная длина текста - {self.__max_length}\n' \
               f'Число наиболее вероятных следующих слов - {self.__top_k}\n' \
               f'Совокупная вероятность для следующих слов - {self.__top_p}\n' \
               f'Вероятность появления слов с большой вероятностью - {self.__temperature}\n'

    def get_mode(self):
        return self.__mode

    def set_mode(self, new_mode: bool) -> None:
        self.__mode = new_mode

    def set_temperature(self, new_temperature: float) -> None:
        self.__temperature = new_temperature

    def set_max_length(self, new_max_length: int) -> None:
        self.__max_length = new_max_length

    def set_top_k(self, new_top_k: int) -> None:
        self.__top_k = new_top_k

    def set_top_p(self, new_top_p: float) -> None:
        self.__top_p = new_top_p

    def set_default(self) -> None:
        self.__max_length = 200
        self.__top_k = 10
        self.__top_p = 0.95
        self.__temperature = 1
