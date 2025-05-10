from pathlib import Path
from typing import Callable
from dataclasses import dataclass

@dataclass()
class PathNameMapping:
    obj: Path
    current_name: str
    new_name: str | None

class PathListEditor:
    def __init__(
            self,
            *extensions: str,
            search_path: str = r'./'
    ):
        self.__extensions = tuple(
            ext if ext.startswith('.') else f'.{ext}' for ext in extensions
        )
        self.__search_path= search_path
        self.__path_list_files: list[Path] = []
        self.__path_obj_list_current_new_names: list[PathNameMapping] = []
        self.__list_current_new_names: list[list[str | None]] = []


    def __prepare_path_name_mapping(self) -> None:
        for path_file in self.__path_list_files:
            obj = PathNameMapping(
                obj=path_file,
                current_name=path_file.stem,
                new_name=None
            )
            self.__path_obj_list_current_new_names.append(obj)

    def extract_from_path_obj_list_current_new_names(self) -> list[list[str | None]]:
        if not self.__path_obj_list_current_new_names:
            self.__create_path_list_files(*self.__extensions, search_path=self.__search_path)

        for obj in self.__path_obj_list_current_new_names:
            current_name_value = getattr(obj, 'current_name', None)
            new_name_value = getattr(obj, 'new_name', None)
            self.__list_current_new_names.append([current_name_value, new_name_value])
        return self.__list_current_new_names

    def __create_path_list_files(
            self,
            *extensions: str,
            search_path: str = r'./'
    ) -> None:
        """
            List files in the script's directory (default) filtered by extensions.
            :param extensions: Tuple of file extensions to filter (e.g., '.txt', '.py').
            :param search_path:
        """
        self.__path_list_files = []

        directory = Path(search_path)
        for file_path in directory.rglob("*"):
            if file_path.is_file() and (not extensions or file_path.suffix in extensions):
                self.__path_list_files.append(file_path)
        self.__prepare_path_name_mapping()


    def get_path_list_files(self) -> list[Path]:
        self.__create_path_list_files(*self.__extensions, search_path=self.__search_path)
        return self.__path_list_files


    def get_path_obj_list_current_new_names(self) -> list[PathNameMapping]:
        self.__create_path_list_files(*self.__extensions, search_path=self.__search_path)
        return self.__path_obj_list_current_new_names

    def __rename_files(
            self,
            dry_run: bool = True,
            rename_function: Callable[[Path], str] | None = None,
            new_extension: str | None = None
    ) -> None:
        """
        Rename files using a custom renaming function and optional new extension.
        :param dry_run: If True, just print changes without applying them.
        :param rename_function: Function that takes a Path and returns the new filename as string (no path).
        example:
        def my_renamer(path: Path) -> str:
            return f"renamed_{path.stem}"
        :param new_extension: Optional new extension (e.g., '.md', '.bak').
        """
        for file_path in self.__path_list_files:
            if rename_function:
                new_name = rename_function(file_path)
            else:
                new_name = file_path.stem  # default: keep original name

            ext = new_extension if new_extension else file_path.suffix
            new_file_path = file_path.with_name(f"{new_name}{ext}")

            if dry_run:
                print(f"Would rename: {file_path} -> {new_file_path}")
            else:
                print(f"Renaming: {file_path} -> {new_file_path}")
                file_path.rename(new_file_path)


# if __name__ == '__main__':
#     tool = PathListEditor()
#     tool.create_path_list_files('.txt')
#     file_list = tool.get_path_list_files()
#     file_list1 = tool.get_path_obj_list_current_new_names()
#     print(file_list)
#     print(file_list1)