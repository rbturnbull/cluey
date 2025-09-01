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