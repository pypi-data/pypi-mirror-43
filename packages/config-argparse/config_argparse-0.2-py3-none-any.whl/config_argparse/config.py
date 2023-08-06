from __future__ import annotations

from typing import Optional, Callable, List, Any, TypeVar, Union, Generic, Set, Sequence, cast, Iterable, Tuple, Type
import argparse
import copy
import builtins
import sys
from .argparse_action import NoOpAction

T = TypeVar('T')
basic_types = (str, int, float)


class Value(Generic[T]):

    def __init__(
        self,
        default: T = None,
        *,
        type: Callable[[str], T] = None,
        choices: Sequence[T] = None,
        required: bool = False,
        nargs: Union[int, str] = None,
        help: str = None,
        metavar: Union[str, Tuple[str, ...]] = None
    ) -> None:

        # infer type
        if type is None:
            if default is not None:
                if isinstance(default, (list, tuple)):
                    if len(default) > 0:
                        type = builtins.type(default[0])
                else:
                    type = builtins.type(default)
            elif choices is not None:
                if len(choices) > 0:
                    type = builtins.type(choices[0])

        if type is None:
            raise Exception(
                'failed to infer type ({} {})'.format(default, choices)
            )

        # set nargs
        if nargs is None:
            if isinstance(default, (list, tuple)):
                nargs = '+'

        # check
        if type == bool and default is not False:
            raise Exception('bool type only supports store_true action.')

        self.default = default
        self.type = type
        self.choices = choices
        self.required = required
        self.nargs = nargs
        self.help = help
        self.metavar = metavar

    def add_argument(
        self,
        parser: argparse._ActionsContainer,
        name: str,
        dest: str = None,
    ) -> None:
        kwards = {
            "default": self.default,
            "required": self.required,
            "help": self.help,
            "dest": dest,
        }
        if self.type == bool:
            kwards["action"] = cast(
                argparse.Action, argparse._StoreTrueAction
                if self.default is False else argparse._StoreFalseAction
            )
        else:
            kwards["type"] = self.type
            kwards["nargs"] = self.nargs
            kwards["choices"] = self.choices
            kwards["metavar"] = self.metavar

        parser.add_argument(name, **kwards)

    def __repr__(self) -> str:
        res = str(self.default) if not self.required else 'required'
        if self.choices is not None:
            res += ', one of [{}]'.format(
                ', '.join(list(map(str, self.choices)))
            )
        return '{}({})'.format(self.__class__.__name__, res)


class Config:

    def __init__(self):
        self._copy_class_variables(self)

    def parse_known_args(
        self,
        args: List[str],
        prefix='',
        namespace=None,
    ) -> Tuple[object, List[str]]:
        if namespace is None:
            namespace = type(self)()

        def is_name(s):
            return s.startswith('--')

        left_args: Set[str] = set(filter(is_name, args))
        parser = argparse.ArgumentParser(
            self.__class__.__name__, allow_abbrev=False
        )
        self._add_arguments(parser, prefix, namespace)
        if '--' + prefix + 'help' in args:
            parser.print_help()
            parser.exit()
        _, left = parser.parse_known_args(args, namespace=namespace)
        left_args = left_args & set(filter(is_name, left))
        left_args = left_args & self._parse_config(args, prefix, namespace)

        return namespace, list(left_args)

    def parse_args(self, *args, **kwards) -> Config:
        namespace, left_args = self.parse_known_args(*args, **kwards)
        if len(left_args) > 0:
            raise Exception('unknown arguments: {}'.format(left_args))
        return namespace

    def _add_arguments(
        self,
        parser: argparse._ActionsContainer,
        prefix: str,
        namespace: Config,
    ):
        for class_variable in filter(self.is_class_variable, vars(self)):
            name = '--' + prefix + class_variable
            value = getattr(self, class_variable)
            if isinstance(value, Config):
                parser.add_argument(
                    name,
                    action=NoOpAction,
                    dest=class_variable,
                )
            elif isinstance(value, DynamicConfig):
                parser.add_argument(
                    name,
                    action=NoOpAction,
                    dest=class_variable,
                )
            elif isinstance(value, Value):
                value.add_argument(parser, name, class_variable)
            else:
                Value(value).add_argument(parser, name, class_variable)

            if isinstance(getattr(namespace, class_variable, None), Value):
                setattr(
                    namespace, class_variable,
                    getattr(namespace, class_variable).default
                )

    def _parse_config(
        self,
        args: List[str],
        prefix: str,
        namespace: Config,
    ) -> Set[str]:
        left = set(filter(lambda s: s.startswith('--'), args))
        for class_variable in filter(self.is_class_variable, vars(self)):
            dest = prefix + class_variable
            name = '--' + dest
            val = getattr(self, class_variable)

            if isinstance(val, Config):
                sub_namespace = getattr(namespace, class_variable, None)
                sub_namespace, l = val.parse_known_args(
                    args,
                    prefix=dest + '.',
                    namespace=sub_namespace,
                )
                setattr(namespace, class_variable, sub_namespace)
                left = left & set(l)
            elif isinstance(val, DynamicConfig):
                sub_namespace = getattr(namespace, class_variable, None)
                if isinstance(sub_namespace, DynamicConfig):
                    sub_namespace = None
                sub_namespace, l, _ = val.parse_args(
                    namespace,
                    args,
                    prefix=dest + '.',
                    namespace=sub_namespace,
                )
                setattr(namespace, class_variable, sub_namespace)
                left = left & set(l)
        return left

    def __repr__(self):
        res = ['{}:'.format(self.__class__.__name__)]
        for class_variable in filter(self.is_class_variable, vars(self)):
            txt = str(getattr(self, class_variable)).replace('\n', '\n\t')
            res.append('\t{} = {}'.format(class_variable, txt))
        return '\n'.join(res)

    @classmethod
    def is_class_variable(cls, name: str) -> bool:
        return hasattr(
            cls, name
        ) and not name.startswith('_') and not callable(getattr(cls, name))

    @classmethod
    def _copy_class_variables(cls, cls_instance):
        ''' assign instance variables by copying all class variables to instance '''

        for base in filter(lambda c: issubclass(c, Config), cls.__bases__):
            base._copy_class_variables(cls_instance)

        # may be overwritten by child
        for class_variable in filter(cls.is_class_variable, vars(cls)):
            val = getattr(cls, class_variable)
            setattr(cls_instance, class_variable, copy.deepcopy(val))


class DynamicConfig:

    def __init__(self, config_factory: Callable[[Config], Config]):
        self.config_factory = config_factory

    def parse_args(
        self,
        parent_config: Config,
        args: List[str],
        prefix: str,
        namespace: Config,
    ) -> Tuple[Config, Set[str], Type[Config]]:
        config: Config = self.config_factory(parent_config)
        if not isinstance(config, Config):
            raise Exception(
                'DynamicConfig: config_factory should return instance of Config, but returned {}'
                .format(config)
            )
        namespace, left_args = config.parse_known_args(
            args, prefix, namespace=namespace
        )
        return namespace, left_args, config
