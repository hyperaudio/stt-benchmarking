import argparse
import json
import os
import re
import sys

import spacy


class Entity:

    CAPITALISATION_UPPER = 'U'
    CAPITALISATION_LOWER = 'L'
    CAPITALISATION_MIXED = 'M'

    def __init__(self, tokens):
        self.tokens = tokens
        self.speaker = "UU"

    @classmethod
    def from_token(cls, token):
        return cls(tokens=[token,])

    def add_token(self, token):
        self.tokens.append(token)

    @property
    def tokens_without_punct(self):
        return (
            token
            for token in self.tokens
            if not token.is_punct
        )

    @property
    def capitalisation(self):
        if all(token.is_upper for token in self.tokens_without_punct):
            return self.CAPITALISATION_UPPER
        elif all(token.is_lower for token in self.tokens_without_punct):
            return self.CAPITALISATION_LOWER
        else:
            return self.CAPITALISATION_MIXED

    @property
    def punctuation(self):
        last_token = self.tokens[-1]
        return last_token.text if last_token.is_punct else None

    def serialise(self):
        print(self)
        return {
            'text': str(self),
            'capitalisation': self.capitalisation,
            'punctuation': self.punctuation,
            'speaker': self.speaker,
        }

    def __str__(self):
        return ''.join(
            token.text
            for token in self.tokens_without_punct
        )


class TokenizeCommand:

    PATTERNS = {
        'is_contraction': re.compile(
            r'^(([\'](ve|er|d|ll|s|m|am|pose|re|ve))|(n[\']t))$'
        ),
    }

    def __init__(self, input_path, rejoin_contractions, spacy_model):
        self.input_path = input_path
        self.rejoin_contractions = rejoin_contractions
        self.spacy_model = spacy_model
        self.speaker = "UU"

    @staticmethod
    def parse_args():
        parser = argparse.ArgumentParser(
            description="Compute entities from plaintext",
        )
        parser.add_argument(
            'input_path',
            help="Path to plaintext file",
        )
        parser.add_argument(
            '--rejoin-contractions',
            help="Enable rejoining of contractions",
            action='store_const',
            const=True,
            default=False,
        )
        return parser.parse_args()

    def read_input(self):
        with open(self.input_path) as f_read:
            return f_read.read()

    def extract_tokens(self, plaintext):
        nlp = spacy.load(self.spacy_model)
        return nlp(plaintext)

    def entities_from_tokens(self, tokens):
        entities = []
        grabspeaker = False
        for token in tokens:
            if "SPEAKER" in token.text:
                #Do Somethng
                grabspeaker = True
                tokencount = 0
            if grabspeaker:
                if tokencount <= 1:
                    tokencount += 1
                    continue
                else:
                    self.speaker = token.text
                    grabspeaker = False
                    continue 

            if token.text.strip() == "":
                # Ignore whitespace
                continue
            elif not entities:
                # First entity
                entities.append(Entity.from_token(token))
            elif token.is_punct:
                # Rejoin punctuation
                entities[-1].add_token(token)
            elif (
                self.rejoin_contractions and
                self.PATTERNS['is_contraction'].search(token.text)
            ):
                # Rejoin contractions
                entities[-1].add_token(token)
            else:
                # Next entity
                entities.append(Entity.from_token(token))
            entities[-1].speaker = self.speaker
        return entities

    def print_results(self, entities):
        json.dump([entity.serialise() for entity in entities], sys.stdout)

    def execute(self):
        plaintext = self.read_input()
        tokens = self.extract_tokens(plaintext)
        entities = self.entities_from_tokens(tokens)
        self.print_results(entities)


if __name__ == '__main__':
    args = TokenizeCommand.parse_args()
    command = TokenizeCommand(
        input_path=args.input_path,
        rejoin_contractions=args.rejoin_contractions,
        spacy_model='en',
    )
    command.execute()
sys.exit(0)
