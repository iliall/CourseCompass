import CourseCompass.api.prereq.init as init
from CourseCompass.api.prereq.init import Token, TokenType
from tokenize import Tokenize
from CourseCompass.api.prereq.clean import Clean

from test import Node, NodeType
from CourseCompass.api.prereq.api import API
from sqlalchemy import create_engine, text

class parse:
    def parse(tokens: list[Token]) -> Node:
        return Node()
