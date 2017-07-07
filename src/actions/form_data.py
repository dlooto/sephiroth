
from .base_action import *

@Actions.register("resultset_to_form")
class ResultSetToFormAction(BaseAction):
    """
    Convert a dict into form data
    {a:1, b:2} => data[a]=1&data[b]=2
    {{a:1, b:2}, {a:3, b:4}} => data[0][a]=1&data[0][b]=2&data[1][a]=3&data[1][b]=4
    :param key_value_attributes || list
    """

    def result_set_to_form_data(self, dict_list, key_value_attributes_map):
        result = dict()
        index = 0
        for d in dict_list:
            for key, value in d.items():
                data_key = key
                convert = ""
                if key in key_value_attributes_map:
                    attr = key_value_attributes_map[key]
                    data_key = attr[0]
                    if len(attr) > 1:
                        convert = key_value_attributes_map[key][1]
                # ["SomeKey", "", ""], if set the second empty string, 
                # it would prevend transform this field in the destination dict
                if data_key == "":
                    continue
                key = "data[%d][%s]" % (index, data_key)
                if convert == "":
                    result[key] = value
                else:
                    # TODO:
                    from convertor import Converters
                    result[key] = Converters.get(convert)(value)
            index += 1
        return result

    def execute(self, context):
        action_config = self.get_action_config()
        # Mapping of src table fields => dest table fields
        key_value_attributes = action_config['key_value_attributes']

        key_value_attributes_map = dict()
        for a in key_value_attributes:
            if len(a) == 0:
                continue
            key_value_attributes_map[a[0]] = a[1:]
        
        param0 = self.get_param_var_name()

        data = context.get_context_var(param0)
        print("ResultSet", data)
        value = self.result_set_to_form_data(data, key_value_attributes_map)
        
        # print("FormData:", value)
        return_var = self.get_return_var_name()

        context.set_context_var(return_var, value)