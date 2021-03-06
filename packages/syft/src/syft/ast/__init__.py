"""Syft's Abstract Syntax Tree (AST) submodule is responsible for remote call executions.

   An AST is a tree that maps function calls to their exact path,
   and knows what to do with that node in tree.

 Example: Suppose we want to append an object to a List. This means that we need to
 know where we could find the `append` method, so we need to know the following chain:

                globals  <- the global scope or the entry point of execution (hidden)
                   |
                  syft   <- the syft module
                   |
                  lib   <- a submodule of syft
                   |
                  List <- the class we were looking for
                   |
                append <- the method we were looking for

When performing remote execution, this lookup path has to be resolved as well. This is where
the AST submodule comes in handy. AST is responsible for:

A. Remote execution.
B. Local execution.

A. Remote Execution
Remote execution can be performed only when an AST has been constructed with a client. Check
syft/core/node to be familiar with the roles of clients and nodes. Each valid action on the AST
triggers an Action (GetSetStaticAttributeAction, GetSetPropertyAction, etc). This kind of actions
requires: The path on resolving the required node (on the above example, the path is
`syft.lib.List.append`), the object on which to perform it (given by the `__self` attribute and from
`id_at_location` if executed on a pointer) and the attributes if needed.

B. Local Execution
After a call has been made, the remote execution starts. For this, we need a local handler for the result
of the remote execution through a `Pointer`. The AST is responsible for generating all the permitted methods
and attributes on a `Pointer` and the return type of the performed action.


The existing types of nodes are:
* a `Globals`, which is the entry point of an execution, from which point on we can only access Modules.

* a `Callable`, which can be a node for a method, a static method, a function, or a constructor.
This node can no longer have any attributes.

* a `Class`, which is a node that represents a Python Class. This node can contain methods - Callable,
static methods - Callable, class methods - Callable, slot attributes - StaticAttribute, properties - Property,
enum attributes - EnumAttribute.

* a `Module`, which represents a Python file/module. This node can have attributes such as global
variables - StaticAttribute, global functions - Callable and classes - Klass.

* a `StaticAttribute` - represents attribute of a Class or of a Module. This node cannot have any attributes.
This can be remotely get and set.

* a `Property` - represents a @property object of a class. This node cannot have any attributes, which means
that this node is essentially a "leaf". This node can perform get and set remotely.

* an `EnumAttribute` - represents the fields generated by an `Enum`. This node cannot have any attributes,
meaning that this node is essentially a "leaf". This node can perform get remotely.
"""

# stdlib
from typing import Any as TypeAny
from typing import List as TypeList
from typing import Tuple as TypeTuple
from typing import Union

# relative
from . import attribute  # noqa: F401
from . import callable  # noqa: F401
from . import dynamic_object  # noqa: F401
from . import enum  # noqa: F401
from . import globals  # noqa: F401
from . import klass  # noqa: F401
from . import module  # noqa: F401
from . import property  # noqa: F401
from . import static_attr  # noqa: F401


def get_parent(
    path: str, root: Union[attribute.Attribute, globals.Globals, module.Module]
) -> Union[module.Module, klass.Class]:
    """Return the parent of a given path.

    Args:
        path: The full path to an object.
        root: The collection of frameworks held in the global namespace.

    Returns:
        The parent module or class.

    Raises:
        ValueError: If parent is not a class or module

    Examples:
        For instance, given the syft project root directory, the parent to the path `syft.lib.python.Int` is `python`.
    """
    parent = root
    for step in path.split(".")[:-1]:
        if step in parent.attrs:
            parent = parent.attrs[step]

    if not isinstance(parent, (module.Module, klass.Class)):
        raise ValueError(f"Expected (Module, Class), but got {type(parent)}")

    return parent


def add_modules(
    ast: globals.Globals,
    modules: Union[TypeList[str], TypeList[TypeTuple[str, TypeAny]]],
) -> None:
    """Parse a list of modules and register each module to its corresponding parent object in the AST path.

    Args:
        ast: The global AST.
        modules: A list of modules, either a path in string format or a tuple of the path in string and a reference.
    """
    for mod in modules:
        # In case reference is present
        if isinstance(mod, tuple):
            target_module, ref = mod
        else:
            target_module, ref = mod, None

        parent = get_parent(target_module, ast)
        attr_name = target_module.rsplit(".", 1)[-1]
        parent.add_attr(
            attr_name=attr_name,
            attr=module.Module(
                path_and_name=target_module,
                object_ref=ref,
                return_type_name="",
                client=ast.client,
            ),
        )


def add_classes(
    ast: globals.Globals,
    paths: TypeList[TypeTuple[str, str, TypeAny]],
) -> None:
    """Parse a list of classes and register each class to its corresponding parent object in the AST path.

    Args:
        ast: The global AST.
        paths: A list of classes, each of which is a tuple of the path, the return type, and its reference.
    """
    for path, return_type, ref in paths:
        parent = get_parent(path, ast)
        attr_name = path.rsplit(".", 1)[-1]
        parent.add_attr(
            attr_name=attr_name,
            attr=klass.Class(
                path_and_name=path,
                object_ref=ref,
                return_type_name=return_type,
                client=ast.client,
                parent=parent,
            ),
        )


def add_methods(
    ast: globals.Globals,
    paths: TypeList[TypeTuple[str, str]],
) -> None:
    """Parse a list of methods and register each method to its corresponding parent object in the AST path.

    Args:
        ast: The global AST.
        paths: A list of methods, each of which is a tuple of the method's path and its return type.
    """
    for path, return_type in paths:
        parent = get_parent(path, ast)
        path_list = path.split(".")
        parent.add_path(
            path=path_list,
            index=len(path_list) - 1,
            return_type_name=return_type,
        )


def add_dynamic_objects(
    ast: globals.Globals, paths: TypeList[TypeTuple[str, str]]
) -> None:
    for path, return_type in paths:
        parent = get_parent(path, ast)
        parent.add_dynamic_object(path_and_name=path, return_type_name=return_type)
