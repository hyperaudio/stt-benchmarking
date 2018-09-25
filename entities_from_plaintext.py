import argparse
import json
import os
import re
import sys

import enum
import spacy

import sclite_parser

class Capitalisation(enum.Enum):
    upper = "U"
    lower = "L"
    mixed = "M"

class Entity:
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
            if not token.is_punct or token.text == "-"
        )

    @property
    def capitalisation(self):
        if all(token.is_upper for token in self.tokens_without_punct):
            return Capitalisation.upper
        elif all(token.is_lower for token in self.tokens_without_punct):
            return Capitalisation.lower
        else:
            return Capitalisation.mixed

    @property
    def punctuation(self):
        last_token = self.tokens[-1]
        return last_token.text if last_token.is_punct and last_token.text != "-" else None

    def serialise(self):
        return {
            'text': str(self).lower(),
            'capitalisation': self.capitalisation.value,
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

    def __init__(self, input_path, sclite_output, spacy_model):
        self.input_path = input_path
        self.sclite_output = sclite_output
        self.spacy_model = spacy_model
        self.speaker = "Will Williams"

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
            '--sclite-output',
            help="Enable output to be in trn format (preferred by sclite)",
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
        grab_hyphen_text = False
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
            if grab_hyphen_text:
                entities[-1].add_token(token)
                grab_hyphen_text = False
            elif token.is_punct:
                if token.text == "-":
                    grab_hyphen_text = True
                # Rejoin punctuation
                entities[-1].add_token(token)
            elif self.PATTERNS['is_contraction'].search(token.text):
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
        if self.sclite_output:
            serialised_entities = [entity.serialise() for entity in entities]
            sclite_parser.parse_to_sclite(serialised_entities)
        else:
            self.print_results(entities)


if __name__ == '__main__':
    args = TokenizeCommand.parse_args()
    command = TokenizeCommand(
        input_path=args.input_path,
        sclite_output = args.sclite_output,
        spacy_model='en',
    )
    command.execute()
sys.exit(0)
