from FilesTools import PathListEditor
from AI_agent_create_new_names import generate_new_filenames
if __name__ == '__main__':
    # change name with AI
    # create obj with ext and path
    path_list_editor_tool = PathListEditor('txt', search_path='./test')
    # create list for AI_agent
    list_for_AI_agent = path_list_editor_tool.extract_from_path_obj_list_current_new_names()
    # generate new names and return it
    x = generate_new_filenames(list_for_AI_agent)
    # update list[PathNameMapping]
    path_list_editor_tool.update_path_name_mapping(x)
