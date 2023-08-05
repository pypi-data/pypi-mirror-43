from typing import (Any,
                    Callable,
                    List)

from hypothesis import strategies
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.schema import Column
from sqlalchemy.sql.sqltypes import (BigInteger,
                                     Boolean,
                                     Date,
                                     DateTime,
                                     Float,
                                     Integer,
                                     SmallInteger,
                                     String)

from . import enums
from .types import Strategy
from .utils import (identifiers,
                    is_column_unique)

MAX_POSTGRES_VARCHAR_LENGTH = 10485760


def string_types_factory() -> Strategy:
    string_lengths = strategies.integers(min_value=0,
                                         max_value=MAX_POSTGRES_VARCHAR_LENGTH)
    return strategies.one_of(strategies.builds(String,
                                               length=string_lengths),
                             strategies.builds(UUID,
                                               as_uuid=strategies.booleans()),
                             enums.types_factory())


def primary_keys_types_factory() -> Strategy:
    types = [SmallInteger, Integer, BigInteger]
    return strategies.one_of(*map(strategies.just, types))


def types_factory(*,
                  string_types: Strategy = string_types_factory(),
                  primary_keys_types: Strategy = primary_keys_types_factory()
                  ) -> Strategy:
    extra_types = [Float(asdecimal=True), Boolean, Date, DateTime]
    return strategies.one_of(string_types,
                             primary_keys_types,
                             *map(strategies.just, extra_types))


def non_primary_keys_factory(*,
                             names: Strategy = identifiers,
                             types: Strategy = types_factory(),
                             are_unique: Strategy = strategies.booleans(),
                             are_nullable: Strategy = strategies.booleans(),
                             are_indexed: Strategy = strategies.booleans()
                             ) -> Strategy:
    return strategies.builds(Column,
                             name=names,
                             type_=types,
                             unique=are_unique,
                             nullable=are_nullable,
                             primary_key=strategies.just(False),
                             index=are_indexed)


def primary_keys_factory(*,
                         names: Strategy = identifiers,
                         types: Strategy = primary_keys_types_factory(),
                         are_auto_incremented: Strategy = strategies.just(True)
                         ) -> Strategy:
    return strategies.builds(Column,
                             name=names,
                             type_=types,
                             autoincrement=are_auto_incremented,
                             primary_key=strategies.just(True))


def lists_factory(*,
                  primary_keys: Strategy = primary_keys_factory(),
                  non_primary_keys: Strategy = non_primary_keys_factory(),
                  max_size: int = None) -> Strategy:
    max_size = max_size - 1 if max_size is not None else max_size
    non_primary_keys_lists = strategies.lists(non_primary_keys,
                                              min_size=1,
                                              max_size=max_size)

    def list_factory(draw: Callable[[Strategy], Any]) -> List[Column]:
        primary_key = draw(primary_keys)

        def names_are_unique(columns: List[Column]) -> int:
            names = [primary_key.name]
            names += [column.name for column in columns]
            return len(names) == len(set(names))

        non_primary_keys_list = draw(non_primary_keys_lists
                                     .filter(names_are_unique))
        return [primary_key] + non_primary_keys_list

    return strategies.composite(list_factory)()


def non_all_unique_lists_factory(lists: Strategy = lists_factory()
                                 ) -> Strategy:
    def has_non_unique_column(columns: List[Column]) -> bool:
        return any(not is_column_unique(column)
                   for column in columns)

    return lists.filter(has_non_unique_column)
