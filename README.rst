==========
cluey
==========

.. start-badges

|pypi badge| |testing badge| |coverage badge| |docs badge| |black badge| |git3moji badge| |cluey badge|

.. |pypi badge| image:: https://img.shields.io/pypi/v/cluey?color=blue
   :alt: PyPI - Version
   :target: https://pypi.org/project/cluey/

.. |cluey badge| image:: https://img.shields.io/badge/cluey-B1230A.svg
    :target: https://rbturnbull.github.io/cluey/

.. |testing badge| image:: https://github.com/rbturnbull/cluey/actions/workflows/testing.yml/badge.svg
    :target: https://github.com/rbturnbull/cluey/actions

.. |docs badge| image:: https://github.com/rbturnbull/cluey/actions/workflows/docs.yml/badge.svg
    :target: https://rbturnbull.github.io/cluey
    
.. |black badge| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    
.. |coverage badge| image:: https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/rbturnbull/b84e24e6b58498cfcdd7f19388e111ad/raw/coverage-badge.json
    :target: https://rbturnbull.github.io/cluey/coverage/

.. |git3moji badge| image:: https://img.shields.io/badge/git3moji-%E2%9A%A1%EF%B8%8F%F0%9F%90%9B%F0%9F%93%BA%F0%9F%91%AE%F0%9F%94%A4-fffad8.svg
    :target: https://robinpokorny.github.io/git3moji/

.. end-badges

**Cluey - Command Line Utility for Engineers & You**

Build clever, class-based command line apps with minimal boilerplate

Documentation at https://rbturnbull.github.io/cluey/

.. start-quickstart

Installation
=======================

The software can be installed using ``pip``

.. code-block:: bash

    pip install cluey

To install the latest version from the repository, you can use this command:

.. code-block:: bash

    pip install git+https://github.com/rbturnbull/cluey.git


Your first Cluey CLI
=======================

Here is a minimal example of a Cluey CLI app:

.. code-block:: Python

    import cluey

    class GreetCLI(cluey.Cluey):
        """A minimal Cluey CLI app"""

        @cluey.main
        def greet(self, name: str = cluey.Option(..., help="")):
            """Greet a person by name"""
            print(f"Hello, {name}!")


    if __name__ == "__main__":
        GreetCLI().main()


Then you can run this:

.. code-block:: bash

    python greet.py --help

Which will display:

.. code-block:: bash

    Usage: greet.py [OPTIONS]                                                               
                                                                                            
    Greet a person by name                                                                  
                                                                                            
    ╭─ Options ─────────────────────────────────────────────────────────────────────────────╮
    │ *  --name        TEXT  The name of the person to greet [required]                     │
    │    --help              Show this message and exit.                                    │
    ╰───────────────────────────────────────────────────────────────────────────────────────╯

To run the app,

.. code-block:: bash

    python cluey/examples/greet.py --name Alice

This will display:

.. code-block:: bash

    Hello, Alice!

Adding a flag
=================

.. code-block:: python

    import cluey

    class GreetCLI(cluey.Cluey):
        """A minimal Cluey CLI app"""

        @cluey.main
        def greet(self, name: str = cluey.Option(..., help="The name of the person to greet")):
            """Greet a person by name"""
            print(f"Hello, {name}!")

        @cluey.flag(shortcut="-v")
        def version(self) -> str:
            """Show the version of this CLI"""
            return "GreetCLI version 0.1.0"


    if __name__ == "__main__":
        GreetCLI().main()    


To display the version of the app, run:

.. code-block :: bash

    python greet.py --version
    # OR
    python greet.py -v


Adding a second command
=======================



.. end-quickstart

Credits
=======================

.. start-credits

Cluey was created created by `Robert Turnbull <https://robturnbull.com>`_ with contributions from Wytamma Wirth and Ashkan Pakzad.

.. end-credits