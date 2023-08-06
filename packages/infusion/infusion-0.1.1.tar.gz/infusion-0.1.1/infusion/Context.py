from functools import wraps
from typing import Callable, Dict, List
from infusion.exceptions.ContextKeyMissing import ContextKeyMissing


class Context:

    def __init__(self, definition=None):
        self.definition = definition if definition else {}

    def __inject_base(
            self,
            substituted_function: Callable[[Callable, List, List, Dict, Dict], Callable],
            *mapper_list,
            **mapper_dictionary
    ):
        def injected_with_args(func):
            try:
                parameters_dictionary = {
                    injected: self.definition[defined]
                    for injected, defined in mapper_dictionary.items()
                }

                parameters_list = list(
                    self.definition[defined] for defined in mapper_list
                )

                @wraps(func)
                def injected(*additional_list, **additional_dictionary):
                    return substituted_function(
                        func, parameters_list, list(additional_list), parameters_dictionary, additional_dictionary
                    )

                return injected
            except KeyError as key:
                raise ContextKeyMissing("Key %s missing in context definition" % key)

        return injected_with_args

    def inject(self, *mapper_list, **mapper_dictionary):
        def substituted_function(
                func: Callable,
                parameters_list: List,
                additional_list: List,
                parameters_dictionary: Dict,
                additional_dictionary: Dict
        ):
            return func(*parameters_list, *additional_list, **parameters_dictionary, **additional_dictionary)

        return self.__inject_base(substituted_function, *mapper_list, **mapper_dictionary)

    def inject_method(self, *mapper_list, **mapper_dictionary):
        def substituted_function(
            func: Callable,
            parameters_list: List,
            additional_list: List,
            parameters_dictionary: Dict,
            additional_dictionary: Dict
        ):
            return func(
                additional_list[0],
                *parameters_list,
                *additional_list[1:],
                **parameters_dictionary,
                **additional_dictionary
            )

        return self.__inject_base(substituted_function, *mapper_list, **mapper_dictionary)

    def update(self, definition):
        self.definition.update(definition)

    def register_factory(self):
        pass

    def new(self):
        pass
