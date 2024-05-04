from typing import Annotated

from fastapi import Depends

from utils.kai_parser.base import KaiParserBase
from utils.kai_parser.providers import get_kai_parser


KaiParserDep = Annotated[KaiParserBase, Depends(get_kai_parser)]
