"""环境变量工具类实现"""
import json
import os
from enum import Enum
from typing import Any, Callable, Optional, Type, TypeVar

__all__ = ["Env"]

T = TypeVar("T")
ENUM = TypeVar("ENUM", bound=Enum)


class Env:
    """环境变量工具类，用于从环境变量中加载配置"""

    @classmethod
    def general_loader(
        cls: Type["Env"],
        name: str,
        loader: Callable[[str], T],
        default: T,
        description: Optional[str] = None,
        contains_secret: bool = False,
    ) -> T:
        """Load value from environment variable. This is a general loader that does not check for None values. If it's None it will return the default value

        Args:
                cls: Type [ Env ] The class to use for this loader
                name: Name of the environment variable to load from the environment
                loader: Callable [ str ] The loader to use to load the value
                default: Default value to return if the value isn't found
                description: Description of the load_env action. Used in log messages
                contains_secret: Whether or not the value contains secret

        Returns:
                The value loaded from the environment or default if not found.
        """
        value_str: Optional[str] = os.getenv(name, None)
        value: T = loader(value_str) if value_str is not None else default

        log_value = value
        if contains_secret:
            if log_value and isinstance(log_value, str) and len(log_value) > 10:
                log_value = log_value[:4] + "**" + log_value[-4:]
            else:
                log_value = "**"
        return value

    @classmethod
    def int(
        cls: Type["Env"],
        name: str,
        default: int = 0,
        description: Optional[str] = None,
        contains_secret: bool = False,
    ) -> int:
        """Load an integer from the environment.

        Args:
                cls: The environment to load from.
                name: The name of the value to load.
                default: The default value to return if the value is not found.
                description: A description of the value that will be shown in the help message.
                contains_secret: Whether or not the value contains a secret.

        Returns:
                The value loaded from the environment or default if not found.
        """
        return cls.general_loader(
            name=name,
            loader=lambda v: int(v),
            default=default,
            description=description,
            contains_secret=contains_secret,
        )

    @classmethod
    def float(
        cls: Type["Env"],
        name: str,
        default: float = 0.0,
        description: Optional[str] = None,
        contains_secret: bool = False,
    ) -> float:
        """Load a float from the environment.

        Args:
                cls: Environment to load from.
                name: Name of the variable to load. It must be a string and cannot contain spaces.
                default: Default value to use if the variable is not found.
                description: Description of the variable. If None no description will be displayed.
                contains_secret: Whether or not the variable contains secret values.

        Returns:
                Instance of the loaded variable or None if not found ( default is 0.0 ) or no value
        """
        return cls.general_loader(
            name=name,
            loader=lambda v: float(v),
            default=default,
            description=description,
            contains_secret=contains_secret,
        )

    @classmethod
    def json(
        cls: Type["Env"],
        name: str,
        default: Optional[Any] = None,
        description: Optional[str] = None,
        contains_secret: bool = False,
    ) -> Any:
        """Load a JSON value from the environment.

        Args:
                cls: Environment to load from.
                name: Name of the value to load.
                default: Default value to use if the value is not found.
                description: Description of the value. Used in error messages.
                contains_secret: Whether or not the value contains secret data.

        Returns:
                An instance of dict.
        """
        return cls.general_loader(
            name=name,
            loader=lambda v: json.loads(v),
            default=default,
            description=description,
            contains_secret=contains_secret,
        )

    @classmethod
    # rename to not shadowing built-in str()
    def string(
        cls: Type["Env"],
        name: str,
        default: str = "",
        description: Optional[str] = None,
        contains_secret: bool = False,
    ) -> str:
        """Load a string variable from the environment.

        Args:
                cls: Environment to load variable from
                name: Name of variable to load ( must be unique )
                default: Default value to use if variable is not found
                description: Description of variable ( may be None ).
                contains_secret: Whether or not the variable contains secret ( True ) or not ( False ).

        Returns:
                Value loaded from environment or default value if not found or not a string ( str ).
        """
        return cls.general_loader(
            name=name,
            loader=lambda v: str(v),
            default=default,
            description=description,
            contains_secret=contains_secret,
        )

    @classmethod
    def enum(
        cls: Type["Env"],
        name: str,
        enum_class: Type[ENUM],
        default: ENUM,
        description: Optional[str] = None,
        contains_secret: bool = False,
    ) -> ENUM:
        """Load an enum from a type. It is possible to specify a type without having to know the type of the enum.

        Args:
                cls: The class to load from.
                name: The name of the enum. This will be used as the key in the config file and the loader will use this as the value for the option.
                enum_class: The type of the enum.
                default: The default value to be returned if no value is found.
                description: A description of the enum. If None no description will be displayed.
                contains_secret: Whether or not the enum contains secret values.

        Returns:
                A loader for enumerated values of the enum_class.
        """
        return cls.general_loader(
            name=name,
            loader=lambda v: enum_class(enum_class.mro()[1](v)),
            default=default,
            description=description,
            contains_secret=contains_secret,
        )

    @classmethod
    # rename to not shadowing built-in bool()
    def boolean(
        cls: Type["Env"],
        name: str,
        default: bool = False,
        description: Optional[str] = None,
        contains_secret: bool = False,
    ) -> bool:
        """Load a boolean from the environment.

        Args:
                cls: Environment to load boolean from.
                name: Name of the boolean as it appears in the config file
                default: Default value to use if the boolean is not set
                description: Description of the boolean.
                contains_secret: Whether or not the boolean contains secret values.

        Returns:
                True if the boolean is set False otherwise.
        """
        return cls.general_loader(
            name=name,
            loader=lambda v: v.lower() in {"true", "1", "yes"},
            default=default,
            description=description,
            contains_secret=contains_secret,
        )

    @classmethod
    def auto_load(
        cls: Type["Env"], name: Optional[None] = None, settings: Any = None
    ) -> None:
        """自动从环境变量中加载配置, e.g. bigshared2__db__settings__db_conn_str => bigshared2.db.settings.db_conn_str
        Autoload settings module and return instance of it. This is a class method that can be used to auto - load settings module.

        Args:
            cls: class to use for auto - loading.
            name (str, optional): settings package, e.g. "bigshared2.settings"
            settings (Any, optional): settings package, e.g. globals()
        """
        if name is None or settings is None:
            import inspect

            stack = inspect.stack()
            try:
                f_locals = stack[1][0].f_locals
                if name is None:
                    name = f_locals["__name__"]
                if settings is None:
                    settings = f_locals
            finally:
                del stack

        if "." not in str(name):
            raise Exception(
                f"Invalid settings module name {name}. Please import it with full package name"
            )

        sep = "__"
        settings_prefix = str(name).replace(".", sep)
        # print('load settings from env for %s' % settings_prefix)
        for key, value in os.environ.items():
            if not key.startswith(settings_prefix):
                continue
            key = key[len(settings_prefix) + len(sep) :]
            if not key or sep in key:
                continue
            if (
                key in settings
                and settings[key] is not None
                and not isinstance(settings[key], str)
            ):
                try:
                    value = json.loads(value)
                except Exception:
                    import ast

                    value = ast.literal_eval(value)

            settings[key] = value
