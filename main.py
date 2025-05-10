from FilesTools import PathListEditor
from AI_agent_create_new_names import generate_new_filenames
if __name__ == '__main__':
    path_list_editor_tool = PathListEditor('txt', search_path='./test')
    list_for_AI_agent = path_list_editor_tool.extract_from_path_obj_list_current_new_names()
    print(list_for_AI_agent)
    x = generate_new_filenames(list_for_AI_agent)
    print(x)


