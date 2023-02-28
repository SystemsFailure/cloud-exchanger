from google.cloud import storage
from src.mutations.metadata import get_all_metadata_by_bucket
from src.controllers.files_controller import download_as_file, LocalStoreInstance, upload_as_file_with_progress
import typer
from src.commands import console_commands

global_app = typer.Typer(rich_markup_mode='rich')

global_app.add_typer(console_commands.app, name='cloud')


def main(name: str = typer.Argument(..., help='The name by user is greet..'), age: int = typer.Option(..., prompt='Write yuor age', confirmation_prompt=True, hide_input=True)):
    print("hello : {} ".format(name))


# point by in
if __name__ == '__main__':
    global_app()